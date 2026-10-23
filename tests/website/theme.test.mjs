import { test } from 'node:test';
import assert from 'node:assert/strict';
import { initializeTheme } from '../../website/theme.mjs';

function setup(stored, blocked = false) {
  const writes = [];
  let change;
  const root = { dataset: {} };
  const label = { hidden: true };
  const select = { value: '', closest: () => label, addEventListener: (_, fn) => { change = fn; } };
  const env = { get localStorage() {
    if (blocked) throw new Error('Storage unavailable');
    return { getItem: () => stored, setItem: (key, value) => writes.push([key, value]) };
  } };
  initializeTheme(env, root, select);
  return { root, select, label, writes, change };
}

test('theme defaults to system without persisting an inferred choice', () => {
  const ui = setup(null);
  assert.equal(ui.root.dataset.theme, 'system');
  assert.equal(ui.select.value, 'system');
  assert.equal(ui.label.hidden, false);
  assert.deepEqual(ui.writes, []);
});

test('restores each supported manual theme', () => {
  for (const value of ['light', 'dark', 'system']) {
    const ui = setup(value);
    assert.equal(ui.root.dataset.theme, value);
    assert.equal(ui.select.value, value);
  }
});

test('manual selection changes appearance and persists, including return to system', () => {
  const ui = setup('dark');
  for (const value of ['light', 'system', 'dark']) {
    ui.select.value = value;
    ui.change();
    assert.equal(ui.root.dataset.theme, value);
    assert.deepEqual(ui.writes.at(-1), ['ai-cortex.theme', value]);
  }
});

test('storage denial does not disable the selector', () => {
  const ui = setup(null, true);
  ui.select.value = 'dark';
  ui.change();
  assert.equal(ui.root.dataset.theme, 'dark');
  assert.equal(ui.label.hidden, false);
});

test('invalid stored values fall back to system and invalid input is ignored', () => {
  const ui = setup('invalid');
  assert.equal(ui.root.dataset.theme, 'system');
  ui.select.value = 'invalid';
  ui.change();
  assert.equal(ui.root.dataset.theme, 'system');
  assert.deepEqual(ui.writes, []);
});
