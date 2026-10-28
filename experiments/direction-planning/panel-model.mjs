import {getWorkHelp} from './work-map.mjs?v=single-map';
import {contextCopy,usageGuidance,designUsage,scenarioUsage} from './context-copy.mjs';
import {catalog,stages,getStage} from './workflow.mjs?v=topic-local-branches';
import {getScenario} from './model.mjs';
import {getChapter} from './story-model.mjs?v=topic-local-branches';
import {getPrerequisites} from './relations.mjs?v=topic-local-branches';
const directionIds=['define-mission','define-vision','define-north-star','define-strategic-pillars','design-strategic-goals'];
const labels={direction:'方向与目标',planning:'待办与计划',design:'把事情说清楚',build:'实现与运行',quality:'检查与修复',commit:'保存与整合',release:'发布给用户',research:'研究与了解问题',foundation:'文档、约定与工具',collaboration:'沟通与交换信息'};
const picks={direction:['define-mission','define-north-star','design-strategic-goals'],planning:['orchestrate-roadmap-planning','prioritize-backlog','map-item-dependencies'],design:['review-requirements','review-functional-design','review-technical-design'],quality:['orchestrate-code-review','review-implementation-alignment','orchestrate-repair-loop'],release:['prepare-release','publish-release','announce-release']};
export function getNodeDetails(id){
 if(!Object.hasOwn(labels,id))throw Error('Unknown node');
 const stage=getStage(id==='direction'?'planning':id);
 const ids=id==='direction'?directionIds:id==='planning'?stage.skills.filter(key=>!directionIds.includes(key)):stage.skills;
 const skills=ids.map(key=>catalog.find(skill=>skill.id===key));
 const chapter=['research','planning','design','build','quality','commit','release'].includes(id)?getChapter(id):null;
 const summary=id==='direction'?'方向回答为什么做，目标说明希望有什么改变。它们帮助判断哪些工作值得做，也可以根据新证据重新审视。':chapter?.body??(id==='foundation'?'按需要补文档、工作约定、自动化或个人凭据支持，让不同的人和智能体有共同依据。':'核实产品事实，整理能独立理解的表达，或按契约交换消息。可以在有需要时调用。');
 const recommended=(picks[id]??ids.slice(0,3)).map(key=>skills.find(skill=>skill.id===key)).filter(Boolean);
 return {help:getWorkHelp(id),usage:structuredClone({...usageGuidance,...scenarioUsage[id]}),relationships:structuredClone(contextCopy[id]??[]),id,title:labels[id],stage:stage.id,summary,skills,recommended,boundary:stage.boundary,prompt:id==='design'?designUsage.request:id==='direction'?getScenario('direction').prompt:stage.prompt,examples:{planning:['requirements'],design:['requirements'],build:['bug'],quality:['bug'],release:['release']}[id]??[],prerequisites:(id==='commit'?['commit']:id==='release'?['publish','announce']:[]).map(operation=>({operation,items:getPrerequisites(operation)}))};
}
export function getNodeForSkill(id){
 if(directionIds.includes(id))return 'direction';
 const stage=stages.find(stage=>stage.skills.includes(id));if(!stage)throw Error('Unknown skill');return stage.id;
}
/* Verification boundary for a reviewed display snapshot, not runtime registry discovery. */
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
