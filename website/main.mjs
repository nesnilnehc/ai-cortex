import {initializeNavigation} from './site-navigation.mjs?v=upgrade-dependencies-1-0-0-20261127';
import { initializeTheme } from './theme.mjs?v=upgrade-dependencies-1-0-0-20261127';
import { initializeLanguage } from './language.mjs?v=upgrade-dependencies-1-0-0-20261127';
import { bindCopyButton } from './copy.mjs?v=upgrade-dependencies-1-0-0-20261127';

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

import './explore/explorer-host.mjs?v=upgrade-dependencies-1-0-0-20261127';
