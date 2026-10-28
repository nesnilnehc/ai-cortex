import {getSkillGraph} from './skill-graph.mjs';
const graph=getSkillGraph();
const owner=id=>graph.groups.find(group=>group.skills.some(skill=>skill.id===id)).id;
const loopSource={path:'../../skills/orchestrate-repair-loop/SKILL.md',quote:'4. **Repeat** — rerun every gate affected by the repair until both pass or a stop condition is reached.'};
export function getTopicMap(){
 const cross=graph.edges.filter(edge=>owner(edge.from)!==owner(edge.to));
 const summarize=(id,from,to,kind,label,condition)=>{const evidence=cross.filter(edge=>owner(edge.from)===from&&owner(edge.to)===to);return {id,from,to,kind,label,condition,evidence:evidence.map(edge=>edge.id),sources:evidence.map(edge=>({path:edge.source,quote:edge.quote})).concat(kind==='loop'?[loopSource]:[])};};
 return structuredClone({regions:[
  {id:'basis',kind:'pair',title:'目标为取舍提供依据',topics:['direction','planning'],edge:'goal-basis'},
  {id:'feedback',kind:'pair',title:'发现问题，就回去修复再核对',topics:['quality','build'],edge:'repair-feedback'},
  {id:'delivery',kind:'pair',title:'交付动作各自核对条件',topics:['commit','release'],edge:'conditional-commit'},
  {id:'clarity',kind:'independent',title:'说明有缺口，可以在这里反复修订',topics:['design']},
  {id:'support',kind:'support',title:'随时取用的支持',note:'需要核实事实、统一约定或沟通时取用；不必等其他主题完成。每项操作仍有自己的输入与授权条件。',topics:['research','foundation','collaboration']}
 ],edges:[
  summarize('goal-basis','direction','planning','input','目标作依据','规划使用已有目标判断候选工作；不要求每次重新制定目标。'),
  summarize('repair-feedback','quality','build','loop','修复 ↔ 复核','发现问题后定向修复，再运行受影响的工程与功能检查；检查通过才收敛，遇到停止条件就暂停。'),
  summarize('conditional-commit','release','commit','call','按需调用提交','仅当发布工具没有自行提交时，才调用提交技能；提交不等于发布，也不是每次发布都重复提交。')
 ],loops:[
  {id:'requirement-loop',from:'design',to:'design',kind:'loop',label:'审查 → 修订 → 再审查',condition:'针对一份已有需求，依据发现的问题定向修订，再审查；不表示所有设计技能必须轮流执行。',sources:[{path:'../../skills/orchestrate-repair-requirements-loop/SKILL.md',quote:'Converge one existing requirement through review, evidence-grounded repair and'}]},
  {id:'quality-loop',from:'quality',to:'quality',kind:'loop',label:'检查 → 定向修复 → 重新检查',condition:'只重跑修复可能影响的检查，直到收敛或达到停止条件。',sources:[loopSource]}
 ]});
}
export function createTopicState(){
 const valid=new Set(graph.groups.map(group=>group.id)),open=new Set();
 const check=id=>{if(!valid.has(id))throw new Error(`Unknown topic: ${id}`);};
 return {expanded:()=>[...open],toggle(id){check(id);if(open.has(id))open.delete(id);else {open.clear();open.add(id);}},reveal(id){check(id);open.clear();open.add(id);},collapseAll(){open.clear();}};
}
