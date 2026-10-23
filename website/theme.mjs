const supported = value => ['system', 'light', 'dark'].includes(value);
const storageKey = 'ai-cortex.theme';

export function initializeTheme(env, root, select) {
  let stored;
  try { stored = env.localStorage.getItem(storageKey); } catch { /* Storage is optional. */ }
  const selected = supported(stored) ? stored : 'system';
  root.dataset.theme = selected;
  select.value = selected;
  select.addEventListener('change', () => {
    if (!supported(select.value)) return;
    root.dataset.theme = select.value;
    try { env.localStorage.setItem(storageKey, select.value); } catch { /* Keep this page usable. */ }
  });
  select.closest('label').hidden = false;
}
