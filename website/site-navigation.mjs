import navigation from './site-navigation.json?v=aic04-host-1' with {type:'json'};
const languages=['en','zh'];
// Static hosting may canonicalize .html URLs before the document executes.
const pathAliases=new Map([['/zh','/zh.html'],['/index','/index.html'],['/explore/zh','/explore/zh.html'],['/explore/index','/explore/index.html']]);
const normalizeSitePath=pathname=>pathAliases.get(pathname)??pathname;
const homePaths=new Set(['/','/index.html','/zh.html']);
const overviewPaths=new Set(['/explore/','/explore/index.html','/explore/zh.html']);
export function getSiteDestination(id,locale){
 if(!Object.hasOwn(navigation.destinations,id)||!languages.includes(locale))throw Error('Unknown destination or locale');
 const record=navigation.destinations[id];return {label:record.labels[locale],href:record.routes[locale]};
}
export function getActiveDestination(pathname,hash=''){
 pathname=normalizeSitePath(pathname);
 if(overviewPaths.has(pathname))return 'overview';
 if(!homePaths.has(pathname))throw Error('Unknown site path');
 const section=hash.replace(/^#/,'');return Object.hasOwn(navigation.sectionOwners,section)?navigation.sectionOwners[section]:'home';
}
export function getAlternateDestination(pathname,hash,locale,view){
 const id=getActiveDestination(pathname,hash),base=getSiteDestination(id,locale).href;
 const section=hash.replace(/^#/,'');
 const target=new URL(Object.hasOwn(navigation.sectionOwners,section)?base.split('#')[0]+hash:base,'https://local.invalid');if(['classification','relations'].includes(view))target.searchParams.set('view',view);return target.pathname+target.search+target.hash;
}
export function initializeNavigation(env,doc){
 const update=()=>{
  const {pathname,hash}=env.location,id=getActiveDestination(pathname,hash);
  for(const link of doc.querySelectorAll('[data-site-destination]')){
   if(link.dataset.siteDestination===id)link.setAttribute('aria-current',id==='home'||id==='overview'?'page':'location');else link.removeAttribute('aria-current');
  }
  for(const link of doc.querySelectorAll('[data-alternate-language]'))link.href=getAlternateDestination(pathname,hash,link.dataset.alternateLanguage,new URL(env.location.href).searchParams.get('view'));
 };
 doc.addEventListener('click',event=>{const link=event.target.closest('a');if(!link||event.defaultPrevented||event.button!==0||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey||link.target||link.hasAttribute('download'))return;const target=new URL(link.href),current=new URL(env.location.href),pathname=normalizeSitePath(target.pathname);if(target.origin!==current.origin||!homePaths.has(pathname)||((pathname==='/zh.html')!==(doc.documentElement.lang==='zh-CN'))||!target.hash||target.hash==='#tools'||(target.searchParams.has('lang')&&target.searchParams.get('lang')!==(doc.documentElement.lang==='zh-CN'?'zh':'en')))return;if(!Object.hasOwn(navigation.sectionOwners,target.hash.slice(1)))return;event.preventDefault();if(!target.searchParams.has('view')&&current.searchParams.has('view')&&!target.hash.startsWith('#map-'))target.searchParams.set('view',current.searchParams.get('view'));env.history.pushState(null,'',target.href);env.dispatchEvent(new Event('hashchange'));const node=doc.getElementById(target.hash.slice(1));if(node?.tagName==='DETAILS')node.open=true;node?.scrollIntoView({block:'start'});});
 update();env.addEventListener('explorerviewchange',update);env.addEventListener('hashchange',update);env.addEventListener('popstate',update);
}
