import { test } from 'node:test';
import assert from 'node:assert/strict';
import { initializeLanguage } from '../../website/language.mjs';

function browser({ url = 'https://example.test/', languages = ['en-US'], stored, blocked = false } = {}) {
  const writes = [];
  const redirects = [];
  const env = {
    navigator: { languages },
    location: { href: url, replace: value => redirects.push(value) },
    get localStorage() {
      if (blocked) throw new Error('Storage disabled');
      return { getItem: () => stored, setItem: (key, value) => writes.push([key, value]) };
    },
  };
  return { env, writes, redirects };
}

test('first visit chooses the first supported browser language, defaulting to English', () => {
  for (const [languages, expected] of [[['zh-TW', 'en'], 'zh'], [['fr', 'en-GB', 'zh-CN'], 'en'], [['fr', 'zh-CN'], 'zh'], [[], 'en'], [['de'], 'en']]) {
    const b = browser({ languages });
    assert.equal(initializeLanguage(b.env, 'en'), expected);
    assert.equal(b.redirects.length, expected === 'zh' ? 1 : 0);
    assert.deepEqual(b.writes, []);
  }
});

test('stored manual preference wins over browser language in either direction', () => {
  for (const [stored, languages, page] of [['en', ['zh-CN'], 'zh'], ['zh', ['en-US'], 'en']]) {
    const b = browser({ stored, languages });
    assert.equal(initializeLanguage(b.env, page), stored);
    assert.equal(b.redirects.length, 1);
  }
});

test('explicit language choice replaces the stored preference without redirecting back', () => {
  const b = browser({ url: 'https://example.test/?lang=en', stored: 'zh', languages: ['zh-CN'] });
  assert.equal(initializeLanguage(b.env, 'en'), 'en');
  assert.deepEqual(b.writes, [['ai-cortex.language', 'en']]);
  assert.deepEqual(b.redirects, []);
});

test('blocked storage still honors a manual choice and browser detection', () => {
  const b = browser({ url: 'https://example.test/zh?lang=zh', blocked: true });
  assert.equal(initializeLanguage(b.env, 'zh'), 'zh');
  assert.deepEqual(b.redirects, []);
  const first = browser({ languages: ['zh-CN'], blocked: true });
  assert.equal(initializeLanguage(first.env, 'en'), 'zh');
});

test('redirect preserves query and fragment and settles on its destination', () => {
  const b = browser({ url: 'https://example.test/?campaign=docs#start', stored: 'zh' });
  initializeLanguage(b.env, 'en');
  assert.equal(b.redirects[0], 'https://example.test/zh.html?campaign=docs#start');
  const next = browser({ url: b.redirects[0], stored: 'zh' });
  initializeLanguage(next.env, 'zh');
  assert.deepEqual(next.redirects, []);
});

test('invalid preferences cannot produce unsupported destinations', () => {
  const b = browser({ url: 'https://example.test/?lang=evil', stored: 'fr', languages: ['zh-CN'] });
  assert.equal(initializeLanguage(b.env, 'en'), 'zh');
  assert.equal(new URL(b.redirects[0]).pathname, '/zh.html');
  assert.deepEqual(b.writes, []);
});
