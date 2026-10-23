import { initializeTheme } from './theme.mjs?v=20261023-atlas';
import { initializeLanguage } from './language.mjs?v=20261023-preference';
import { bindCopyButton } from './copy.mjs?v=20261023-i18n';

initializeLanguage(window, document.documentElement.lang === 'zh-CN' ? 'zh' : 'en');

initializeTheme(window, document.documentElement, document.querySelector('#theme'));

bindCopyButton(
  document.querySelector('#copy-commands'),
  document.querySelector('#install-commands'),
  document.querySelector('#copy-feedback'),
  navigator.clipboard,
  document.querySelector('#copy-feedback').dataset,
);
