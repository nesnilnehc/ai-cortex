// Reviewed provenance is a static projection; recommendations never enter this boundary.
const categories=new Set(['native','third_party_original','third_party_adapted']);
const fail=()=>{throw new Error('Invalid or incomplete provenance catalogue');};
function keys(value,expected){return value&&typeof value==='object'&&!Array.isArray(value)&&JSON.stringify(Object.keys(value).sort())===JSON.stringify([...expected].sort());}
function safeEvidence(value,revision,preview){
 if(typeof value!=='string'||/[\\\u0000-\u0020]/u.test(value))return false;
 const prefix=preview?'/provenance-evidence/':`https://github.com/nesnilnehc/ai-cortex/blob/${revision}/`;
 if(!value.startsWith(prefix))return false;
 const path=value.slice(prefix.length).split('#')[0];
 if(!path||path.includes('?'))return false;
 try{return path.split('/').every(part=>{const decoded=decodeURIComponent(part);return decoded&&decoded!=='.'&&decoded!=='..'&&!/[\/\\\u0000-\u001f]/u.test(decoded);});}catch{return false;}
}
function validSources(record){
 if(!Array.isArray(record.sources)||(record.classification==='native'?record.sources.length!==0:record.sources.length===0))return false;
 return record.sources.every(source=>{
  if(!keys(source,['title','url'])||typeof source.title!=='string'||!source.title.trim()||typeof source.url!=='string'||/[\\\u0000-\u0020]/u.test(source.url))return false;
  try{const url=new URL(source.url);return url.protocol==='https:'&&!url.username&&!url.password;}catch{return false;}
 });
}
export function validateProjection(data,ids,{allowPreview=false}={}){
 const preview=allowPreview&&data?.delivery_ready===false&&data?.source_revision===null;
 if(!keys(data,preview?['schema_version','source_revision','delivery_ready','skills']:['schema_version','source_revision','skills'])||data.schema_version!==2||(!preview&&(typeof data.source_revision!=='string'||!/^[a-f0-9]{40}$/.test(data.source_revision))))fail();
 if(!keys(data.skills,ids)||new Set(ids).size!==ids.length)fail();
 for(const record of Object.values(data.skills)){
  if(!keys(record,['classification','evidence','sources'])||!categories.has(record.classification)||!validSources(record)||!Array.isArray(record.evidence)||!record.evidence.length||!record.evidence.every(url=>safeEvidence(url,data.source_revision,preview)))fail();
 }
 return data;
}
export function getProvenance(data,id,copy){
 const record=Object.hasOwn(data.skills,id)&&data.skills[id];
 if(!record||!categories.has(record.classification)||!validSources(record)||typeof copy.labels?.[record.classification]!=='string'||!Array.isArray(record.evidence)||!record.evidence.length||!record.evidence.every(url=>safeEvidence(url,data.source_revision,data.delivery_ready===false&&data.source_revision===null)))fail();
 return {classification:record.classification,label:copy.labels[record.classification],evidence:[...record.evidence],sources:record.sources.map(source=>({...source}))};
}
export function frameSkill(control,id,data,copy,doc=globalThis.document){
 const record=getProvenance(data,id,copy),frame=doc.createElement('div');frame.className='provenance-entry';
 if(record.classification!=='native'){
  const link=(source,text)=>{const node=doc.createElement('a');node.href=source.url;node.target='_blank';node.rel='noopener';node.textContent=text;return node;};
  let badge;
  if(record.sources.length===1)badge=link(record.sources[0],record.label);
  else{
   badge=doc.createElement('details');const summary=doc.createElement('summary');summary.textContent=record.label;
   const list=doc.createElement('ul');for(const source of record.sources){const item=doc.createElement('li');item.append(link(source,source.title));list.append(item);}badge.append(summary,list);
  }
  badge.className='provenance-badge';badge.setAttribute('data-provenance',record.classification);frame.append(badge);
 }
 frame.append(control);return frame;
}

let activeProjection=null;
export async function initializeProvenance({manifest,ids,copy,fetcher=globalThis.fetch,reportError=()=>{},previewHost=false,signalFactory=()=>AbortSignal.timeout(10000)}){
 activeProjection=null;
 // The old bundle remains usable during the explicitly planned schema migration.
 // Delivery readiness requires a provenanceRevision and all reviewed records.
 if(!manifest.provenanceRevision&&!manifest.provenancePreview)return true;
 let stage='configuration';
 try{
  if(manifest.provenancePreview&&!previewHost)fail();
  stage='fetch';
  const response=await fetcher(new URL('./skill-provenance.json?v=aic08-provenance-3',import.meta.url),{signal:signalFactory()});
  if(!response.ok)fail();
  stage='parse';
  const payload=await response.json();
  stage='projection';
  const data=validateProjection(payload,ids,{allowPreview:manifest.provenancePreview===true&&previewHost});
  stage='revision';
  if(!manifest.provenancePreview&&data.source_revision!==manifest.provenanceRevision)fail();
  activeProjection=data;return true;
 }catch{
  reportError(copy.unavailable,{operation:'provenance.load',outcome:'failed',code:'PROVENANCE_LOAD_FAILED',stage});return false;
 }
}
export function decorateSkill(control,id,copy,doc=globalThis.document){
 return activeProjection?frameSkill(control,id,activeProjection,copy,doc):control;
}
