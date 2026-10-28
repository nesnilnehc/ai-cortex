import {test} from 'node:test';
import assert from 'node:assert/strict';
import {getNodeDetails,getNodeForSkill} from './panel-model.mjs';
import {catalog} from './workflow.mjs';
test('direction and backlog nodes have distinct explanations and skill scopes',()=>{
 const direction=getNodeDetails('direction'),planning=getNodeDetails('planning');
 assert.equal(direction.title,'方向与目标');
 assert.ok(direction.skills.some(x=>x.id==='define-mission'));
 assert.ok(!direction.skills.some(x=>x.id==='prioritize-backlog'));
 assert.ok(planning.skills.some(x=>x.id==='prioritize-backlog'));
 assert.notEqual(direction.prompt,planning.prompt);
});
test('every registered skill resolves to a selectable node with its own request',()=>{
 for(const skill of catalog){
  const node=getNodeForSkill(skill.id),detail=getNodeDetails(node);
  assert.ok(detail.skills.some(x=>x.id===skill.id),skill.id);
  assert.ok(detail.prompt&&detail.summary&&detail.title);
 }
 assert.throws(()=>getNodeForSkill('unknown'));
 assert.throws(()=>getNodeDetails('unknown'));
});
test('only relevant examples appear inside each node detail',()=>{
 assert.deepEqual(getNodeDetails('quality').examples,['bug']);
 assert.deepEqual(getNodeDetails('design').examples,['requirements']);
 assert.deepEqual(getNodeDetails('release').examples,['release']);
 assert.deepEqual(getNodeDetails('foundation').examples,[]);
});
test('publication and announcement prerequisites stay separate in the same panel',()=>{
 const conditions=getNodeDetails('release').prerequisites;
 assert.equal(conditions.length,2);
 assert.equal(conditions[0].operation,'publish');
 assert.equal(conditions[1].operation,'announce');
 assert.ok(conditions[1].items.includes('实际发布结果'));
});

test('planning explains definition, priority, promotion and maintenance as separate work',()=>{
 const detail=getNodeDetails('planning');
 assert.ok(detail.relationships.some(x=>x.title==='安排到路线图'));
 const text=detail.relationships.map(x=>x.body).join(' ');
 for(const meaning of ['优先级','依赖','不一定','维护','Now'])assert.ok(text.includes(meaning),meaning);
 assert.ok(getNodeDetails('direction').relationships.length>=3);
 assert.ok(getNodeDetails('quality').relationships.some(x=>x.title==='实际验收'));
});

test('catalog parity rejects missing, unknown and duplicate entries without mutating fixtures',async()=>{
 const {validateCatalog}=await import('./panel-model.mjs');
 const {readFileSync}=await import('node:fs');
 const index=readFileSync(new URL('../../skills/INDEX.md',import.meta.url),'utf8');
 const ids=[...index.matchAll(/^- \[([^\]]+)\]/gm)].map(x=>x[1]);
 assert.equal(validateCatalog(catalog,ids),true);
 for(let repeat=0;repeat<2;repeat++){
  assert.throws(()=>validateCatalog(catalog.slice(1),ids),/Missing/);
  assert.throws(()=>validateCatalog([...catalog,{id:'unknown'}],ids),/Unknown/);
  assert.throws(()=>validateCatalog([...catalog,catalog[0]],ids),/Duplicate/);
 }
 assert.equal(validateCatalog(catalog,ids),true);
});

test('work context distinguishes ordinary agent help from optional Cortex assets',()=>{
 const detail=getNodeDetails('design');
 assert.match(detail.usage.ordinary,/直接/);
 assert.match(detail.usage.ordinary,/追问|补充/);
 assert.match(detail.usage.cortex,/统一|复核/);
 assert.match(detail.usage.adopted,/已采用/);
 assert.deepEqual(detail.usage.assets.map(x=>x.kind),['Skill','Spec','Rule','Protocol']);
 assert.ok(detail.usage.assets.every(x=>x.href&&x.purpose));
 assert.match(detail.prompt,/直接/);
 for(const id of ['direction','planning','quality','commit','release','research','build','foundation','collaboration'])assert.ok(getNodeDetails(id).usage.ordinary);
});

test('asset picker defaults to a relevant skill and contains every context skill exactly once',async()=>{
 const {getNodeSkillSelection}=await import('./panel-model.mjs');
 const seen=[];
 for(const id of ['direction','planning','design','build','quality','commit','release','research','foundation','collaboration']){
  const detail=getNodeDetails(id),selection=getNodeSkillSelection(id);
  assert.equal(selection.selected.id,detail.recommended[0].id);
  assert.deepEqual(selection.skills.map(x=>x.id).sort(),detail.skills.map(x=>x.id).sort());
  assert.equal(new Set(selection.skills.map(x=>x.id)).size,selection.skills.length);
  seen.push(...selection.skills.map(x=>x.id));
  for(const skill of selection.skills)assert.equal(getNodeSkillSelection(id,skill.id).selected.id,skill.id);
 }
 assert.deepEqual(seen.sort(),catalog.map(x=>x.id).sort());
 assert.throws(()=>getNodeSkillSelection('planning','commit-work'),/does not belong/);
 assert.throws(()=>getNodeSkillSelection('unknown'));
 const sample=getNodeSkillSelection('commit');sample.selected.purpose='changed';
 assert.notEqual(getNodeSkillSelection('commit').selected.purpose,'changed');
});
