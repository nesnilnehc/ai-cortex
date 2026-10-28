// Covers: AIC-REQ-04 A4/A16/A17; omission-sensitive state and semantic projection contracts.
import {test} from 'node:test';import assert from 'node:assert/strict';
test('view transitions preserve explicit target, detail mode and independent layout',async()=>{
 const {createExplorerState}=await import('../../website/explore/explorer-state.mjs');const s=createExplorerState();s.selectSkill('review-requirements');s.setDetailMode('work');s.updateViewState('classification',{expandedCategoryIds:['map-quality'],scrollByRegion:{a:71}});const before=s.snapshot();s.setView('relations');s.setView('classification');assert.deepEqual(s.snapshot(),before);s.selectRelation('define-mission__define-vision');const target=s.snapshot().detail;s.setView('relations');assert.deepEqual(s.snapshot().detail,target);assert.equal(s.snapshot().selectedSkillId,'review-requirements');assert.throws(()=>s.setDetailMode('usage'));assert.throws(()=>s.setView('bogus'));assert.throws(()=>s.selectSkill('bogus'));
});
test('both groupings cover skills once; only actual calls become parents and sequence is scenario scoped',async()=>{
 const m=await import('../../website/explore/relationship-model.mjs');const {catalog}=await import('../../website/explore/workflow.mjs');assert.equal(m.classification.groups.length,6);assert.deepEqual(m.classification.groups.flatMap(g=>g.skillIds).sort(),catalog.map(s=>s.id).sort());
 for(const group of m.classification.groups){const tree=m.getCallHierarchy({view:'classification',groupId:group.id});for(const edge of tree.children)assert.equal(edge.kind,'call');}
 const ordered=m.getSkillOrder({view:'relations',groupId:'quality',scenarioId:'engineering-gate'});assert.ok(ordered.before.some(e=>e.from==='review-security'&&e.to==='review-reliability'));assert.throws(()=>m.getCallHierarchy({view:'classification',groupId:'quality'}));
 assert.throws(()=>m.validateSequences([{from:'a',to:'b',scenarioId:'x'},{from:'b',to:'a',scenarioId:'x'}]));assert.equal(m.validateSequences([{from:'a',to:'b',scenarioId:'x'},{from:'b',to:'a',scenarioId:'y'}]),true);
});
// Covers: A16; invalid call metadata never becomes an implicit child.
test('relationship data rejects missing call mode, unknown endpoints and invalid sequence',async()=>{
 const m=await import('../../website/explore/relationship-model.mjs');const edges=structuredClone(m.relationships);const call=edges.find(e=>e.kind==='call');delete call.callMode;assert.throws(()=>m.validateRelationships(edges));
});
// Covers: A17; reject foreign layout IDs before mutation and keep work-only/none distinct.
test('invalid local layouts cannot mutate state; close and work-only selection never fabricate a skill',async()=>{
 const {createExplorerState}=await import('../../website/explore/explorer-state.mjs');const s=createExplorerState();const before=s.snapshot();assert.throws(()=>s.updateViewState('classification',{expandedCategoryIds:['bogus']}));assert.deepEqual(s.snapshot(),before);s.selectWork('planning');assert.equal(s.snapshot().selectedSkillId,null);s.setView('relations');assert.equal(s.snapshot().detail.target.kind,'work');s.closeDetail();s.setView('classification');assert.equal(s.snapshot().detail.open,false);
});
// Covers: A5/A16; primary category membership is an exact partition, independent of references.
test('classification rejects omitted, foreign and duplicate primary entries',async()=>{
 const {classification,validateClassification}=await import('../../website/explore/relationship-model.mjs');const good=structuredClone(classification);assert.equal(validateClassification(good),true);const duplicate=structuredClone(good);duplicate.groups[0].skillIds.push(duplicate.groups[0].skillIds[0]);assert.throws(()=>validateClassification(duplicate));const missing=structuredClone(good);missing.groups[0].skillIds.pop();assert.throws(()=>validateClassification(missing));
});
// Covers: A8/A16; a deep call target must use the outside gutter, never another child.
test('local relationship route clears differently indented sibling nodes',async()=>{
 const {routeSkillConnection}=await import('../../website/explore/skill-graph.mjs');const origin={left:0,top:0};const from={left:0,right:216,top:0,height:100},to={left:0,right:182,top:700,height:80},block={left:0,right:216,top:110,height:100};const points=routeSkillConnection(from,to,origin,'suggest',[from,to,block]);for(let i=1;i<points.length;i++){const a=points[i-1],b=points[i];for(let t=.01;t<1;t+=.01){const x=a[0]+(b[0]-a[0])*t,y=a[1]+(b[1]-a[1])*t;assert.ok(!(x>0&&x<216&&y>110&&y<210));}}
});
