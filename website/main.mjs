import {initializeNavigation} from './site-navigation.mjs?v=rename-session-0-1-1-20261124';
import { initializeTheme } from './theme.mjs?v=rename-session-0-1-1-20261124';
import { initializeLanguage } from './language.mjs?v=rename-session-0-1-1-20261124';
import { bindCopyButton } from './copy.mjs?v=rename-session-0-1-1-20261124';

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

import './explore/explorer-host.mjs?v=rename-session-0-1-1-20261124';
