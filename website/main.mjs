import {initializeNavigation} from './site-navigation.mjs?v=artifact-sources-20261104';
import { initializeTheme } from './theme.mjs?v=artifact-sources-20261104';
import { initializeLanguage } from './language.mjs?v=artifact-sources-20261104';
import { bindCopyButton } from './copy.mjs?v=artifact-sources-20261104';

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

import './explore/explorer-host.mjs?v=artifact-sources-20261104';
