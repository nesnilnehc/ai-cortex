import {initializeNavigation} from './site-navigation.mjs?v=version-notes-refinement-20261105';
import { initializeTheme } from './theme.mjs?v=version-notes-refinement-20261105';
import { initializeLanguage } from './language.mjs?v=version-notes-refinement-20261105';
import { bindCopyButton } from './copy.mjs?v=version-notes-refinement-20261105';

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

import './explore/explorer-host.mjs?v=version-notes-refinement-20261105';
