"""Render reviewed provenance artifacts and isolated, non-deliverable previews."""
from html import escape
import json
import os
import re
from pathlib import Path
import shutil
import tempfile
from urllib.parse import quote

import skill_provenance_v2 as provenance

START = '<!-- provenance:start -->'
END = '<!-- provenance:end -->'
PAGES = ('website/index.html', 'website/zh.html', 'website/explore/index.html', 'website/explore/zh.html')


def fallback(root, projection, language, legacy=False):
    base = root / 'website/explore'
    copy = provenance.read_json(base / 'locales' / f'{language}.json')
    groups = provenance.read_json(base / 'classification.json')['groups']
    manifest = provenance.read_json(base / 'source-manifest.json') if (base / 'source-manifest.json').exists() else {}
    revision = manifest.get('assetsRevision', 'main')
    sections = []
    for group in groups:
        title = copy['classification'][group['id']]
        entries = []
        for name in group['skillIds']:
            skill, record = copy['skills'][name], projection['skills'][name]
            label = copy['provenance']['labels'][record['classification']]
            source = f'https://github.com/nesnilnehc/ai-cortex/blob/{revision}/skills/{quote(name, safe="")}/SKILL.md'
            badge = f'<span class="provenance-badge" data-provenance="{record["classification"]}">{escape(label)}</span>'
            if record['classification'] == 'native':
                badge = ''
            entries.append(f'<li class="provenance-entry">{badge}<a class="classification-skill" data-class-skill="{escape(name, quote=True)}" href="{escape(source, quote=True)}"><span>{escape(skill["name"])}</span><code>{escape(name)}</code><small>{escape(skill["purpose"])}</small></a></li>')
        sections.append(f'<details class="classification-card" id="{escape(group["id"], quote=True)}"><summary><strong>{escape(title["name"])}</strong><small>{escape(title["purpose"])}</small><span>{len(entries)}</span></summary><div class="classification-body"><ul>{"".join(entries)}</ul></div></details>')
    body = ''.join(sections)
    return f'<div id="classification-view">{body}</div>' if not legacy else f'<section aria-label="Skill catalogue">{body}</section>'


def replace_region(source, content, *, region=None):
    start = START if region is None else f'<!-- provenance:{region}:start -->'
    end = END if region is None else f'<!-- provenance:{region}:end -->'
    provenance.require(source.count(start) == source.count(end) == 1 and source.index(start) < source.index(end), 'missing or duplicate managed provenance markers')
    before, rest = source.split(start)
    _, after = rest.split(end)
    return before + start + content + end + after


def render_directory(root, projection, language):
    base = root / 'website/explore'
    copy = provenance.read_json(base / 'locales' / f'{language}.json')
    metadata = provenance.read_json(base / 'skill-metadata.json')['skills']
    manifest = provenance.read_json(base / 'source-manifest.json') if (base / 'source-manifest.json').exists() else {}
    revision = manifest.get('assetsRevision', 'main')
    entries = []
    for name, record in sorted(projection['skills'].items()):
        label = copy['provenance']['labels'][record['classification']]
        description = metadata[name].get('description', copy['skills'][name]['purpose'])
        badge = '' if record['classification'] == 'native' else f'<span class="provenance-badge" data-provenance="{record["classification"]}">{escape(label)}</span>'
        entries.append(f'<li class="provenance-entry" data-asset="skills/{escape(name, quote=True)}">{badge}<div><code>{escape(name)}</code><p>{escape(description)}</p></div><a class="atlas-source" href="https://github.com/nesnilnehc/ai-cortex/blob/{escape(revision, quote=True)}/skills/{quote(name, safe="")}/SKILL.md" aria-label="Inspect source: {escape(name, quote=True)}">↗</a></li>')
    return f'<details class="directory-type" id="skills"><summary>{escape(copy["provenance"]["directoryTitle"])} · {len(entries)}</summary><ul>{"".join(entries)}</ul></details>'


def preview_projection(records):
    return {'schema_version': 1, 'source_revision': None, 'delivery_ready': False,
            'skills': {name: {'classification': rec['classification'],
                             'evidence': ['/provenance-evidence/' + quote(r['path'], safe='/') + ('#' + quote(r['anchor'], safe='') if r.get('anchor') else '') for r in rec['evidence']]}
                       for name, rec in sorted(records.items())}}


def generate(root, skills, render_index, *, check=False, preview_dir=None):
    records = provenance.load(root, root / 'skills')
    provenance.validate_coverage(root, records)
    if preview_dir is not None:
        destination = Path(preview_dir).resolve()
        provenance.require(not destination.is_relative_to(root.resolve()) and not destination.exists(), 'preview destination must be new and outside repository')
        projection = preview_projection(records)
    else:
        provenance.verify_asset_revision(root)
        manifest = provenance.read_json(root / 'website/explore/source-manifest.json')
        projection = provenance.export_public(root, records, manifest.get('provenanceRevision'))
    plan = {
        'skills/INDEX.md': render_index(skills, records),
        'website/explore/skill-provenance.json': json.dumps(projection, indent=2, ensure_ascii=False) + '\n',
    }
    for relative in PAGES:
        language = 'zh' if relative.endswith('zh.html') else 'en'
        source = replace_region((root / relative).read_text(encoding='utf-8'), fallback(root, projection, language, '/explore/' in relative))
        if 'id="asset-directory"' in source:
            source = replace_region(source, render_directory(root, projection, language), region='directory')
        locale = provenance.read_json(root / 'website/explore/locales' / f'{language}.json')
        if 'ui' in locale and 'ca39d237326' in locale['ui']:
            summary = escape(locale['ui']['ca39d237326'].replace('{0}', str(len(records))))
            source = re.sub(r'(<p id="catalogue-summary">).*?(</p>)', lambda m: m[1] + summary + m[2], source, flags=re.S)
        plan[relative] = source
    if check:
        stale = [path for path, content in plan.items() if not (root / path).is_file() or (root / path).read_text(encoding='utf-8') != content]
        provenance.require(not stale, 'generated artifacts are stale: ' + ', '.join(stale), code='STALE_OUTPUT', next_action='Regenerate all provenance artifacts together.')
        return
    if preview_dir is not None:
        destination.mkdir()
        shutil.copytree(root / 'website', destination / 'website', ignore=shutil.ignore_patterns('.openai', 'README.md'))
        # A preview mirrors only public evidence, never investigation notes.
        source_manifest = destination / 'website/explore/source-manifest.json'
        preview_manifest = provenance.read_json(source_manifest) if source_manifest.exists() else {}
        preview_manifest['provenancePreview'] = True
        source_manifest.write_text(json.dumps(preview_manifest, indent=2) + '\n', encoding='utf-8')
        for name, rec in records.items():
            target = destination / 'skills' / name / 'SKILL.md'
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((root / 'skills' / name / 'SKILL.md').read_bytes())
            for reference in rec['evidence']:
                target = destination / 'website/provenance-evidence' / reference['path']
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(provenance.evidence_path(root, reference).read_bytes())
        for path, content in plan.items():
            target = destination / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding='utf-8')
        return
    temporary = []
    try:
        for relative, content in plan.items():
            target = root / relative
            provenance.require(target.parent.is_dir() and not target.is_symlink(), 'invalid generated output target', field=relative)
            fd, staging = tempfile.mkstemp(prefix='.' + target.name + '.', dir=target.parent)
            temporary.append((Path(staging), target))
            with os.fdopen(fd, 'w', encoding='utf-8') as stream:
                stream.write(content)
        for staging, target in temporary:
            staging.replace(target)
    finally:
        for staging, _ in temporary:
            staging.unlink(missing_ok=True)
