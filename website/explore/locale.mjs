import en from './locales/en.json?v=aic04-host-1' with {type:'json'};
import zh from './locales/zh.json?v=aic04-host-1' with {type:'json'};
import metadata from './skill-metadata.json?v=aic04-host-1' with {type:'json'};
const dictionaries={en,zh};
export const locale=globalThis.document?.documentElement.lang==='en'?'en':'zh';
function select(language){if(!Object.hasOwn(dictionaries,language))throw Error(`Unknown locale: ${language}`);return dictionaries[language];}
export const dictionary=select(locale);
export function getCopy(language,key,args=[]){
 const ui=select(language).ui;
 if(!Object.hasOwn(ui,key))throw Error(`Unknown copy key: ${key}`);
 return ui[key].replace(/\{(\d+)\}/g,(_,index)=>{if(index>=args.length)throw Error(`Missing copy argument: ${key}/${index}`);return String(args[index]);});
}
export const t=(key,args=[])=>getCopy(locale,key,args);
export function getSkillGuidance(id,language=locale){
 const record=select(language).skills;
 if(!Object.hasOwn(record,id)||!Object.hasOwn(metadata.skills,id))throw Error(`Unknown skill: ${id}`);
 return structuredClone({...record[id],entry:metadata.skills[id].entry,sourceHash:metadata.skills[id].sourceHashes[`skills/${id}/SKILL.md`]});
}
export function validateLocales(left,right){
 function compare(a,b,path='locale'){
  if(a===null||b===null){if(a!==b)throw Error(`Invalid locale null: ${path}`);return;}
  if(Array.isArray(a)){if(!Array.isArray(b)||a.length!==b.length)throw Error(`Missing locale array: ${path}`);a.forEach((v,i)=>compare(v,b[i],`${path}.${i}`));return;}
  if(a!==null&&typeof a==='object'){
   if(!b||typeof b!=='object'||Array.isArray(b)||JSON.stringify(Object.keys(a).sort())!==JSON.stringify(Object.keys(b).sort()))throw Error(`Missing locale field: ${path}`);
   for(const key of Object.keys(a))compare(a[key],b[key],`${path}.${key}`);return;
  }
  if(typeof a!==typeof b)throw Error(`Invalid locale field: ${path}`);
  if(typeof a==='string'){
   const placeholders=value=>[...value.matchAll(/\{\d+\}/g)].map(m=>m[0]).sort().join();
   if(placeholders(a)!==placeholders(b))throw Error(`Invalid locale placeholders: ${path}`);
   if((/\.(skills|recommended)\.\d+$|\.(id|from|to|entry|kind|href|path|source|sourceHash|owner|exampleId|example|operation)$/.test(path))&&a!==b)throw Error(`Locale identity drift: ${path}`);
  }else if(a!==b)throw Error(`Locale typed identity drift: ${path}`);
 }
 compare(left,right);
 for(const record of [left,right])for(const id of Object.keys(metadata.skills))for(const key of ['name','purpose','when','provide','use','result'])if(typeof record.skills?.[id]?.[key]!=='string'||!record.skills[id][key].trim())throw Error(`Missing locale skill field: ${id}/${key}`);
 return true;
}

// Validate the shipped pair once at its data boundary; never substitute another language.
validateLocales(zh,en);
