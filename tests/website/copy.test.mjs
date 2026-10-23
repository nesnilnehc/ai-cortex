import { test } from 'node:test';
import assert from 'node:assert/strict';
import { bindCopyButton } from '../../website/copy.mjs';

const commands = 'mkdir -p ~/.local/share\ngit clone --depth 1 https://github.com/nesnilnehc/ai-cortex.git ~/.local/share/ai-cortex\n~/.local/share/ai-cortex/bin/cortex install';

function setup(clipboard, text = commands) {
  let click;
  const button = {
    hidden: true,
    disabled: false,
    addEventListener(event, handler) {
      assert.equal(event, 'click');
      click = handler;
    },
  };
  const feedback = { textContent: '' };
  bindCopyButton(button, { textContent: text }, feedback, clipboard);
  return { button, feedback, click: () => click() };
}

test('copies the complete rendered commands and reports completed success', async () => {
  let actual;
  const ui = setup({ writeText: async (value) => { actual = value; } });
  assert.equal(ui.button.hidden, false);
  await ui.click();
  assert.equal(actual, commands);
  assert.equal(ui.feedback.textContent, 'Commands copied. Paste them into your terminal.');
  assert.equal(ui.button.disabled, false);
});

test('a denied clipboard write gives recovery and permits a successful retry', async () => {
  let calls = 0;
  const ui = setup({ writeText: async () => {
    calls += 1;
    if (calls === 1) throw new Error('permission denied');
  } });
  await ui.click();
  assert.equal(ui.feedback.textContent, 'Copy unavailable. Select and copy the commands below.');
  assert.equal(ui.button.disabled, false);
  await ui.click();
  assert.match(ui.feedback.textContent, /^Commands copied/);
});

test('an unavailable clipboard keeps manual recovery available', async () => {
  const ui = setup(undefined);
  await ui.click();
  assert.equal(ui.feedback.textContent, 'Copy unavailable. Select and copy the commands below.');
  assert.equal(ui.button.disabled, false);
});

test('pending writes do not report success or start duplicate writes', async () => {
  let complete;
  let writes = 0;
  const ui = setup({ writeText: () => {
    writes += 1;
    return new Promise((resolve) => { complete = resolve; });
  } });
  const pending = ui.click();
  assert.equal(ui.button.disabled, true);
  assert.equal(ui.feedback.textContent, 'Copying commands…');
  await ui.click();
  assert.equal(writes, 1);
  complete();
  await pending;
  assert.equal(ui.button.disabled, false);
  assert.match(ui.feedback.textContent, /^Commands copied/);
});

test('empty commands never create a successful clipboard operation', async () => {
  let writes = 0;
  const ui = setup({ writeText: async () => { writes += 1; } }, ' \n ');
  await ui.click();
  assert.equal(writes, 0);
  assert.equal(ui.feedback.textContent, 'Commands unavailable. Open the installation guide below.');
  assert.equal(ui.button.disabled, false);
});

test('uses the supplied language for pending, success and recovery', async () => {
  const messages = { copying: '正在复制', success: '已复制', unavailable: '请手动复制', empty: '命令不可用' };
  let click;
  let finish;
  const button = { addEventListener: (_, handler) => { click = handler; } };
  const feedback = { textContent: '' };
  bindCopyButton(button, { textContent: commands }, feedback, { writeText: () => new Promise(resolve => { finish = resolve; }) }, messages);
  const pending = click();
  assert.equal(feedback.textContent, messages.copying);
  finish();
  await pending;
  assert.equal(feedback.textContent, messages.success);
  bindCopyButton(button, { textContent: commands }, feedback, undefined, messages);
  await click();
  assert.equal(feedback.textContent, messages.unavailable);
  bindCopyButton(button, { textContent: '' }, feedback, undefined, messages);
  await click();
  assert.equal(feedback.textContent, messages.empty);
});
