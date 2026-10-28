import classificationData from './classification.json?v=aic04-host-1' with {type:'json'};
import rawEdges from './skill-edges.json?v=aic04-host-1' with {type:'json'};
import metadata from './skill-metadata.json?v=aic04-host-1' with {type:'json'};
import {dictionary} from './locale.mjs?v=aic04-host-1';
export const classification=structuredClone(classificationData);
export const relationships=rawEdges.map(e=>({...e,...dictionary.skillEdges[e.id]}));
export function validateSequences(edges){
 for(const scenario of new Set(edges.map(e=>e.scenarioId))){
  const selected=edges.filter(e=>e.scenarioId===scenario),seen=new Set();
  function visit(id,stack){if(stack.has(id))throw Error('Contradictory sequence');if(seen.has(id))return;for(const e of selected.filter(e=>e.from===id))visit(e.to,new Set([...stack,id]));seen.add(id);}
  for(const e of selected)visit(e.from,new Set());
 }
 return true;
}
validateSequences(relationships.filter(e=>e.kind==='sequence'));
export function getMembers({view,groupId}){
 if(view==='classification'){const group=classification.groups.find(g=>g.id===groupId);if(!group)throw Error('Unknown category');return [...group.skillIds];}
 if(view==='relations'&&metadata.groupOrder.includes(groupId))return Object.values(metadata.skills).filter(s=>s.owner===groupId).map(s=>s.id);
 throw Error('Unknown group/view');
}
export function getCallHierarchy(query){
 const ids=getMembers(query),inside=new Set(ids),parents=new Map(),children=[],references=[];
 for(const edge of relationships.filter(e=>e.kind==='call'&&inside.has(e.from))){
  let id=edge.from,cycle=false;while(id){if(id===edge.to){cycle=true;break;}id=parents.get(id)?.from;}
  if(!inside.has(edge.to)||parents.has(edge.to)||cycle)references.push(edge);else{parents.set(edge.to,edge);children.push(edge);}
 }
 return {roots:ids.filter(id=>!parents.has(id)),children,references};
}
export function getSkillOrder(query){const ids=new Set(getMembers(query));return {before:relationships.filter(e=>e.kind==='sequence'&&ids.has(e.from)&&ids.has(e.to)&&(!query.scenarioId||e.scenarioId===query.scenarioId)),peers:[...ids],feedback:relationships.filter(e=>e.kind==='feedback'&&ids.has(e.from))};}

export function validateRelationships(edges){
 const seen=new Set();
 for(const e of edges){
  if(seen.has(e.id)||!Object.hasOwn(metadata.skills,e.from)||!Object.hasOwn(metadata.skills,e.to)||!['call','input','method','suggest','sequence','feedback'].includes(e.kind)||!e.source?.startsWith('skills/')||!e.quote?.trim()||!e.condition?.trim())throw Error('Invalid relationship record');seen.add(e.id);
  if(e.kind==='call'&&!['required','conditional'].includes(e.callMode))throw Error('Missing call mode');
  if(e.kind==='sequence'&&!e.scenarioId?.trim())throw Error('Missing sequence scenario');
 }
 validateSequences(edges.filter(e=>e.kind==='sequence'));return true;
}
validateRelationships(relationships);

export function validateClassification(data){
 const seen=new Set(),groups=new Set();
 if(data.groups.length!==6)throw Error('Expected six categories');
 for(const group of data.groups){if(groups.has(group.id))throw Error('Duplicate category');groups.add(group.id);for(const id of group.skillIds){if(!Object.hasOwn(metadata.skills,id)||seen.has(id))throw Error('Unknown or duplicate primary skill');seen.add(id);}}
 if(seen.size!==Object.keys(metadata.skills).length)throw Error('Missing primary skill');return true;
}
validateClassification(classification);
