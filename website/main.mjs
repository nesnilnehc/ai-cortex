import {initializeNavigation} from './site-navigation.mjs?v=build-artifacts-20261101';
import { initializeTheme } from './theme.mjs?v=build-artifacts-20261101';
import { initializeLanguage } from './language.mjs?v=build-artifacts-20261101';
import { bindCopyButton } from './copy.mjs?v=build-artifacts-20261101';

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

import './explore/explorer-host.mjs?v=build-artifacts-20261101';
