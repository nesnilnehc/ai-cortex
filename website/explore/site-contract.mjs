import {getSiteDestination} from '../site-navigation.mjs?v=upgrade-dependencies-1-0-0-20261127';
export const explorerLanguageRoutes=Object.freeze(Object.fromEntries(['en','zh'].map(locale=>[locale,getSiteDestination('overview',locale).href.split('?')[0]])));
export function getExplorerRoutes(locale){
 const home=getSiteDestination('home',locale).href,other=locale==='en'?'zh':'en';
 return {home,entry:explorerLanguageRoutes[locale],alternate:getSiteDestination('overview',other).href};
}
