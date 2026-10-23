import { bindCopyButton } from './copy.mjs';

const theme = document.querySelector('#theme');
theme.addEventListener('change', () => { document.documentElement.dataset.theme = theme.value; });
theme.closest('label').hidden = false;

bindCopyButton(
  document.querySelector('#copy-commands'),
  document.querySelector('#install-commands'),
  document.querySelector('#copy-feedback'),
  navigator.clipboard,
);
