#!/usr/bin/env node
/**
 * Verify Raw GitHub links for key project files.
 * Non-blocking: network failures yield warning, not exit 1.
 * Usage: node scripts/verify-links.mjs [baseUrl]
 * Default baseUrl: https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main
 */
const BASE =
  process.argv[2] || 'https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main';
const FILES = [
  'README.md',
  'AGENTS.md',
  'manifest.json',
  'skills/INDEX.md',
];

const FETCH_TIMEOUT_MS = 10_000;

/**
 * @param {string} url
 * @returns {Promise<{ url: string; status: number | null; ok: boolean; error?: string }>}
 */
async function check(url) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), FETCH_TIMEOUT_MS);
  try {
    const res = await fetch(url, {
      method: 'HEAD',
      signal: controller.signal,
    });
    clearTimeout(timeout);
    return { url, status: res.status, ok: res.ok };
  } catch (e) {
    clearTimeout(timeout);
    const error =
      e.name === 'AbortError' ? 'timeout' : e.message ?? String(e);
    return { url, status: null, ok: false, error };
  }
}

async function main() {
  console.log(`Checking Raw links (base: ${BASE})\n`);
  let failed = 0;
  for (const file of FILES) {
    const url = `${BASE}/${file}`;
    const r = await check(url);
    const icon = r.ok ? '✓' : '✗';
    const status = r.status ?? r.error ?? '—';
    console.log(`  ${icon} ${file} — ${status}`);
    if (!r.ok) failed++;
  }
  console.log('');
  if (failed > 0) {
    console.log(`Warning: ${failed} link(s) unavailable (network or 404).`);
    process.exit(0); // non-blocking per QG-1
  } else {
    console.log('All Raw links OK.');
  }
}

main();
