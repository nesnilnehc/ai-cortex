import records from './support-scopes.json?v=aic06-build-release-1' with {type:'json'};
import {dictionary,locale as currentLocale} from './locale.mjs?v=aic06-build-release-1';
import en from './locales/en.json?v=aic06-build-release-1' with {type:'json'};
import zh from './locales/zh.json?v=aic06-build-release-1' with {type:'json'};
export function validateSupportScopes(items){
 if(!Array.isArray(items)||items.length!==2||new Set(items.map(i=>i.providerTopicId)).size!==2)throw Error('Missing support providers');
 const seen=new Set(),topics=new Set(Object.keys(dictionary.topics));
 for(const item of items){
  if(seen.has(item.id)||!['foundation','collaboration'].includes(item.providerTopicId)||!item.targets.length)throw Error('Invalid support provider');seen.add(item.id);
  const targets=new Set();
  for(const target of item.targets){
   if(!topics.has(target.topicId)||targets.has(target.topicId)||!target.sources?.length)throw Error('Invalid support target');targets.add(target.topicId);
   for(const d of [en,zh])if(!d.supportScopes[item.labelKey]?.label||!d.supportScopes[target.conditionKey]?.condition)throw Error('Missing support condition');
   for(const source of target.sources)if(!/^skills\/[a-z0-9-]+\/SKILL\.md$/.test(source.path)||!source.quote?.trim())throw Error('Invalid support source');
  }
 }
 return true;
}
validateSupportScopes(records);
export function getSupportScopes(providerTopicId,locale=currentLocale){
 if(!Object.hasOwn(dictionary.topics,providerTopicId)||!['en','zh'].includes(locale))throw Error('Unknown support provider or locale');
 const d=locale==='en'?en:zh;
 return records.filter(r=>r.providerTopicId===providerTopicId).map(r=>({id:r.id,label:d.supportScopes[r.labelKey].label,targets:r.targets.map(t=>({...structuredClone(t),condition:d.supportScopes[t.conditionKey].condition}))}));
}
