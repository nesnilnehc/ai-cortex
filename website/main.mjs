import {initializeNavigation} from './site-navigation.mjs?v=product-requirement-skills-20261111';
import { initializeTheme } from './theme.mjs?v=product-requirement-skills-20261111';
import { initializeLanguage } from './language.mjs?v=product-requirement-skills-20261111';
import { bindCopyButton } from './copy.mjs?v=product-requirement-skills-20261111';

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

import './explore/explorer-host.mjs?v=product-requirement-skills-20261111';
