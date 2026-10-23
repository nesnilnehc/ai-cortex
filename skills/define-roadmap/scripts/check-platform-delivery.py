#!/usr/bin/env python3
"""Read-only checks of captured remote roadmap delivery evidence; no network I/O."""

import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import tarfile
from urllib.parse import unquote, urljoin, urlsplit, urlunsplit


class Document(HTMLParser):
    """Inspect captured Lake/HTML without rewriting platform markup."""

    def __init__(self, lake):
        super().__init__(convert_charrefs=True)
        self.ids, self.anchors, self.links, self.cards, self.text = set(), set(), [], {}, []
        self.feed(lake)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            if attrs['id'] in self.ids:
                raise ValueError('duplicate anchor ID: ' + attrs['id'])
            self.ids.add(attrs['id'])
            if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a') or attrs.get('data-lake-id') == attrs['id']:
                self.anchors.add(attrs['id'])
        if tag == 'a' and attrs.get('href'):
            self.links.append(attrs['href'])
        if tag == 'card':
            raw = attrs.get('value', '')
            if not raw.startswith('data:'):
                raise ValueError('card lacks a readable data payload')
            value = json.loads(unquote(raw[5:]))
            if not isinstance(value, dict):
                raise ValueError('card payload is not an object')
            key = str(value.get('id') or attrs.get('name', 'card') + ':' + str(len(self.cards)))
            if key in self.cards:
                raise ValueError('duplicate card identity: ' + key)
            self.cards[key] = (attrs.get('name'), value, {k: v for k, v in attrs.items() if k != 'value'})

    def handle_data(self, data):
        self.text.append(data)


def index(pages):
    if not isinstance(pages, list) or not pages:
        raise ValueError('nonempty document snapshots required')
    result = {}
    for page in pages:
        if not isinstance(page, dict) or type(page.get('id')) not in (str, int) or not str(page['id']):
            raise ValueError('document identity required')
        key = str(page['id'])
        if key in result:
            raise ValueError('duplicate document identity: ' + key)
        for field in ('url', 'title', 'lake', 'updated_at'):
            if not isinstance(page.get(field), str) or not page[field].strip():
                raise ValueError('missing document field: ' + key + ': ' + field)
        url = urlsplit(page['url'])
        if url.scheme not in ('https', 'http') or not url.netloc or url.fragment:
            raise ValueError('absolute page URL without fragment required')
        result[key] = page
    if len({p['url'] for p in result.values()}) != len(result):
        raise ValueError('duplicate document URL')
    return result


def preflight(expected, current):
    """Compare the initial read with a fresh read immediately before writing."""
    try:
        before, now = index(expected), index(current)
        if before.keys() != now.keys():
            return ['document set changed before write']
        return ['concurrent change: ' + key for key in before if any(
            before[key][field] != now[key][field] for field in ('url', 'title', 'lake', 'updated_at'))]
    except (ValueError, TypeError, KeyError) as exc:
        return [str(exc)]


def normalized(text):
    return re.sub(r'\s+', '', text.replace('\u200b', ''))


def reference(base, href):
    """Resolve a link and compare fragment semantics without decoding path separators."""
    parts = urlsplit(urljoin(base, href))
    return urlunsplit((parts.scheme, parts.netloc, parts.path, parts.query, '')), unquote(parts.fragment)


def recovery_findings(root, inventory, archive):
    """Compare inventoried originals with a tar backup without extracting/deleting.

    This proves byte recovery only; semantic migration review and cleanup
    authorization remain separate prerequisites owned by the calling skill.
    """
    try:
        root = Path(root).resolve(strict=True)
        if not isinstance(inventory, list) or not inventory or len(set(inventory)) != len(inventory):
            raise ValueError('nonempty unique retirement inventory required')
        with tarfile.open(archive, 'r:*') as backup:
            members = backup.getmembers()
            seen = set()
            for name in inventory:
                relative = Path(name)
                if relative.is_absolute() or '..' in relative.parts:
                    raise ValueError('retired path must stay within the selected root')
                original = root / relative
                if original in seen:
                    raise ValueError('retirement inventory aliases the same file')
                seen.add(original)
                if original.resolve(strict=True) != original or not original.is_file():
                    raise ValueError('retired source must be a regular file without aliases')
                matching = [m for m in members if m.name == relative.as_posix()]
                if len(matching) != 1 or not matching[0].isfile():
                    raise ValueError('backup member missing, duplicated or nonregular: ' + name)
                with backup.extractfile(matching[0]) as saved:
                    if saved.read() != original.read_bytes():
                        raise ValueError('backup differs from current source: ' + name)
        return []
    except (OSError, ValueError, TypeError, tarfile.TarError) as exc:
        return [str(exc)]


def verify(baseline, readback, contract):
    """Check protected platform structure plus explicit source-derived assertions.

    Passing proves consistency with supplied observations, not their live provenance
    or the truth/completeness of business sources. This tool never authorizes deletion.
    """
    findings, unchecked = [], set()
    try:
        before, after = index(baseline), index(readback)
        checks = contract.get('documents') if isinstance(contract, dict) else None
        if not isinstance(checks, list) or not checks or not all(isinstance(c, dict) for c in checks):
            raise ValueError('nonempty per-document acceptance checks required')
        checked = {str(c['id']): c for c in checks}
        if len(checked) != len(checks) or checked.keys() != after.keys() or before.keys() != after.keys():
            raise ValueError('snapshot and acceptance document sets differ')
        immutable = contract.get('immutable_docs', [])
        changed = contract.get('changed_cards', {})
        if (not isinstance(immutable, list) or any(str(k) not in before for k in immutable)
                or not isinstance(changed, dict) or any(k not in after for k in changed)
                or any(not isinstance(v, list) or not all(isinstance(k, str) for k in v) for v in changed.values())):
            raise ValueError('invalid history/card preservation scope')
        parsed = {key: Document(p['lake']) for key, p in after.items()}
        stored_ids = {key: page.ids | (Document(after[key]['html']).ids if after[key].get('html') else set())
                      for key, page in parsed.items()}
        urls = {p['url']: key for key, p in after.items()}
        referenced = {key: set() for key in after}
        for pages in (before, after):
            for page in pages.values():
                for href in Document(page['lake']).links:
                    parts = urlsplit(urljoin(page['url'], href))
                    target = urlunsplit((parts.scheme, parts.netloc, parts.path, parts.query, ''))
                    if target in urls and parts.fragment:
                        referenced[urls[target]].add(unquote(parts.fragment))
        for key, page in after.items():
            old, new, check = Document(before[key]['lake']), parsed[key], checked[key]
            inspection = check.get('inspection', 'content')
            if inspection not in ('content', 'metadata'):
                raise ValueError('unknown inspection mode')
            if inspection == 'metadata' and not check.get('visual_checks'):
                raise ValueError('metadata inspection requires named title/directory observations')
            if inspection == 'metadata' and before[key]['lake'] != page['lake']:
                findings.append(key + ': metadata-only operation changed body')
            if before[key]['url'] != page['url']:
                findings.append(key + ': stable URL changed')
            if not isinstance(check.get('title'), str) or check['title'] != page['title']:
                findings.append(key + ': unexpected display title')
            protected = check.get('protected_anchors', [])
            if not isinstance(protected, list) or not all(isinstance(a, str) and a for a in protected):
                raise ValueError('invalid protected anchor list')
            retained = old.anchors | referenced[key] | set(protected)
            if before[key].get('html'):
                retained |= Document(before[key]['html']).anchors
            stored = stored_ids[key]
            if not retained <= stored:
                findings.append(key + ': stored anchors lost')
            observed = page.get('rendered_ids')
            if inspection == 'content' and (not isinstance(observed, list)
                    or not all(isinstance(i, str) for i in observed)
                    or not (retained | new.anchors) <= set(observed)):
                findings.append(key + ': rendered anchors missing or unobserved')
            if key in {str(i) for i in immutable} and page['lake'] != before[key]['lake']:
                findings.append(key + ': historical original changed')
            for card_id, card in old.cards.items():
                if card_id not in new.cards or (card[0], card[2]) != (new.cards[card_id][0], new.cards[card_id][2]):
                    findings.append(key + ': card identity/type lost: ' + card_id)
                elif card_id not in changed.get(key, []) and new.cards[card_id] != card:
                    findings.append(key + ': unrelated card changed: ' + card_id)
            if any(i not in old.cards for i in changed.get(key, [])):
                findings.append(key + ': unknown authorized card replacement')
            content = normalized(' '.join(new.text))
            for field in ('required_text', 'forbidden_text', 'visual_checks'):
                values = check.get(field, [])
                if not isinstance(values, list) or not all(isinstance(v, str) and v for v in values):
                    raise ValueError('invalid acceptance list: ' + field)
                for value in values:
                    if field == 'visual_checks':
                        if page.get('visual_checks', {}).get(value) is not True:
                            findings.append(key + ': visual check failed or unobserved: ' + value)
                    elif (normalized(value) in content) != (field == 'required_text'):
                        findings.append(key + ': content assertion failed: ' + value)
            required_links = check.get('required_links', [])
            if not isinstance(required_links, list) or not all(isinstance(h, str) and h for h in required_links):
                raise ValueError('invalid required link list')
            actual_links = {reference(page['url'], href) for href in new.links}
            for href in required_links:
                if reference(page['url'], href) not in actual_links:
                    findings.append(key + ': required link lost or retargeted: ' + href)
            for kind, card, _attrs in new.cards.values():
                if kind == 'image' and inspection == 'content':
                    images = page.get('images', [])
                    if not any(i.get('src') == card.get('src') and type(i.get('natural_width')) is int
                               and i['natural_width'] > 0 for i in images):
                        findings.append(key + ': image not visibly loaded')
            for href in new.links:
                absolute = urljoin(page['url'], href)
                parts = urlsplit(absolute)
                target = urlunsplit((parts.scheme, parts.netloc, parts.path, parts.query, ''))
                if target in urls:
                    if parts.fragment and unquote(parts.fragment) not in stored_ids[urls[target]]:
                        findings.append(key + ': broken internal link: ' + href)
                else:
                    unchecked.add(absolute)
    except (ValueError, TypeError, KeyError, AttributeError) as exc:
        findings.append('invalid or incomplete evidence: ' + str(exc))
    return dict(passed=not findings, findings=findings, unchecked_external_links=sorted(unchecked),
                scope='Captured structure, explicit assertions and reported rendering only; no live source certification')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('evidence', type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.evidence.read_text())
        result = verify(data['baseline'], data['readback'], data['contract'])
    except (OSError, ValueError, KeyError, TypeError) as exc:
        result = dict(passed=False, findings=[str(exc)])
    print(json.dumps(result, indent=2))
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
