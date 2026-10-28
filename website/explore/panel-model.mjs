import {dictionary} from './locale.mjs?v=aic08-provenance-2';
import {catalog} from './workflow.mjs?v=aic08-provenance-2';
import metadata from './skill-metadata.json?v=aic08-provenance-2' with {type:'json'};
export function getNodeDetails(id){
 if(!Object.hasOwn(dictionary.contexts,id))throw Error('Unknown node');
 const detail=structuredClone(dictionary.contexts[id]);
 detail.title=dictionary.topics[id].name;detail.help.point=dictionary.topics[id].purpose;
 detail.skills=detail.skills.map(key=>catalog.find(skill=>skill.id===key));
 detail.recommended=detail.recommended.map(key=>detail.skills.find(skill=>skill.id===key));
 return detail;
}
export function getNodeForSkill(id){if(!Object.hasOwn(metadata.skills,id))throw Error('Unknown skill');return metadata.skills[id].owner;}
export function validateCatalog(records,canonicalIds){
 const canonical=new Set(canonicalIds),seen=new Set();
 for(const record of records){
  if(!canonical.has(record.id))throw Error(`Unknown skill: ${record.id}`);
  if(seen.has(record.id))throw Error(`Duplicate skill: ${record.id}`);
  seen.add(record.id);
 }
 for(const id of canonical)if(!seen.has(id))throw Error(`Missing skill: ${id}`);
 return true;
}

// The fixed picker exposes every skill in the selected context without scrolling the narrative.
export function getNodeSkillSelection(nodeId,skillId=null){
 const detail=getNodeDetails(nodeId),preferred=detail.recommended.map(skill=>skill.id);
 const skills=[...detail.skills].sort((a,b)=>{
  const left=preferred.indexOf(a.id),right=preferred.indexOf(b.id);
  return (left<0?preferred.length:left)-(right<0?preferred.length:right);
 });
 const selected=skillId===null?skills[0]:skills.find(skill=>skill.id===skillId);
 if(!selected)throw new Error(`Skill ${skillId} does not belong to ${nodeId}`);
 return structuredClone({skills,selected});
}
