import {initializeNavigation} from './site-navigation.mjs?v=manage-secret-1-2-0-20261126';
import { initializeTheme } from './theme.mjs?v=manage-secret-1-2-0-20261126';
import { initializeLanguage } from './language.mjs?v=manage-secret-1-2-0-20261126';
import { bindCopyButton } from './copy.mjs?v=manage-secret-1-2-0-20261126';

initializeLanguage(window, document.documentElement.lang === 'zh-CN' ? 'zh' : 'en');

initializeTheme(window, document.documentElement, document.querySelector('#theme'));

bindCopyButton(
  document.querySelector('#copy-commands'),
  document.querySelector('#install-commands'),
  document.querySelector('#copy-feedback'),
  navigator.clipboard,
  document.querySelector('#copy-feedback').dataset,
);

initializeNavigation(window,document);

import './explore/explorer-host.mjs?v=manage-secret-1-2-0-20261126';
