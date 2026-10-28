import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {catalog,stages,getStage,findSkills,getGateState} from './workflow.mjs';
test('every registered skill is represented exactly once in the global stages',()=>{
 const index=readFileSync(new URL('../../skills/INDEX.md',import.meta.url),'utf8');
 const ids=[...index.matchAll(/^- \[([^\]]+)\]/gm)].map(x=>x[1]).sort();
 assert.deepEqual(catalog.map(x=>x.id).sort(),ids);
 const members=stages.flatMap(stage=>stage.skills);
 assert.equal(new Set(members).size,members.length);
 assert.deepEqual(members.sort(),ids);
});
test('commit, integration and publication have separate boundaries',()=>{
 assert.deepEqual(getStage('commit').skills,['commit-work','deliver-feature','integrate-branches']);
 assert.ok(getStage('release').skills.includes('publish-release'));
 assert.ok(!getStage('commit').skills.includes('publish-release'));
});
test('review path keeps engineering, functional and execution evidence separate',()=>{
 const stage=getStage('quality');
 assert.ok(stage.skills.includes('review-implementation-alignment'));
 assert.ok(stage.skills.includes('orchestrate-code-review'));
 assert.ok(stage.skills.includes('orchestrate-repair-loop'));
 assert.equal(getGateState('pass').mayProceed,true);
 assert.equal(getGateState('fail').mayProceed,false);
 assert.equal(getGateState('missing').mayProceed,false);
 assert.throws(()=>getGateState('unknown'));
});
test('search is case insensitive and supports Chinese purposes across stages',()=>{
 assert.ok(findSkills({query:' COMMIT-WORK '}).some(x=>x.id==='commit-work'));
 assert.ok(findSkills({query:'提交'}).some(x=>x.id==='commit-work'));
 assert.deepEqual(findSkills({stage:'release'}).map(x=>x.id).sort(),getStage('release').skills.toSorted());
 assert.equal(findSkills({query:'nonexistent-capability-xyz'}).length,0);
 assert.throws(()=>findSkills({stage:'unknown'}));
});
test('stages and catalog are snapshots, not shared mutable state',()=>{
 const stage=getStage('quality');stage.skills.length=0;
 assert.ok(getStage('quality').skills.length>0);
});
test('catalog purposes and definitions remain grounded in source snapshots',()=>{
 const index=readFileSync(new URL('../../skills/INDEX.md',import.meta.url),'utf8');
 // Localized purposes are reviewed against definitions; public-site copy is not authority.
 const localPurposes={...Object.fromEntries(catalog.map(x=>[x.id,x.purpose]))};
 for(const skill of catalog){
  assert.ok(index.includes(`- [${skill.id}](./${skill.id}/SKILL.md) — ${skill.description}`));
  const definition=readFileSync(new URL(`../../skills/${skill.id}/SKILL.md`,import.meta.url),'utf8');
  assert.ok(definition.includes(`name: ${skill.id}`));
  assert.ok(localPurposes[skill.id].trim().length>0);
  assert.equal(findSkills({query:skill.id}).find(x=>x.id===skill.id).purpose,localPurposes[skill.id]);
 }
});

test('roadmap definition purpose permits structure-only and content-only requests',()=>{
 // Independent translation of define-roadmap's scoped alternatives, not an execution sequence.
 assert.equal(findSkills({query:'define-roadmap'})[0].purpose,'设计路线图结构，或在既定结构中填充计划');
});
