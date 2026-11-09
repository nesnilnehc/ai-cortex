import {initializeNavigation} from './site-navigation.mjs?v=plan-next-17-20261109';
import { initializeTheme } from './theme.mjs?v=plan-next-17-20261109';
import { initializeLanguage } from './language.mjs?v=plan-next-17-20261109';
import { bindCopyButton } from './copy.mjs?v=plan-next-17-20261109';

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

import './explore/explorer-host.mjs?v=plan-next-17-20261109';
