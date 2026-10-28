const supported = value => value === 'en' || value === 'zh';
const storageKey = 'ai-cortex.language';

export function initializeLanguage(env, pageLanguage, routes = {en:'/',zh:'/zh.html'}) {
  for (const locale of ['en', 'zh']) {
    if (typeof routes?.[locale] !== 'string' || !/^\/(?![\/\\])[^?#\\]*$/.test(routes[locale])) throw new Error('Invalid language route map');
  }
  const url = new URL(env.location.href);
  const explicit = url.searchParams.get('lang');
  let stored;
  try { stored = env.localStorage.getItem(storageKey); } catch { /* Storage is optional. */ }

  const browser = (env.navigator.languages?.length ? env.navigator.languages : [env.navigator.language])
    .map(value => value?.toLowerCase().split('-')[0])
    .find(supported);
  const selected = supported(explicit) ? explicit : supported(stored) ? stored : browser || 'en';

  if (supported(explicit)) {
    try { env.localStorage.setItem(storageKey, explicit); } catch { /* The URL retains this choice. */ }
  }
  if (selected !== pageLanguage) {
    url.pathname = routes[selected];
    env.location.replace(url.href);
  }
  return selected;
}
