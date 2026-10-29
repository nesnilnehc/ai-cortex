import {test} from 'node:test';
import assert from 'node:assert/strict';
import {getSkillGraph,getSkillForest,getSkillNeighborhood} from '../../website/explore/skill-graph.mjs';
import {getGlobalTopicGraph,routeTopicRelationship} from '../../website/explore/global-topic-graph.mjs';
import {getNodeDetails,getNodeForSkill,validateCatalog} from '../../website/explore/panel-model.mjs';
import {createTopicState} from '../../website/explore/topic-map.mjs';
import {readFileSync} from 'node:fs';
const dictionary=JSON.parse(readFileSync(new URL('../../website/explore/locales/zh.json',import.meta.url)));
const canonical=[...readFileSync(new URL('../../skills/INDEX.md',import.meta.url),'utf8').matchAll(/\]\(\.\/([^/]+)\/SKILL\.md\)/g)].map(m=>m[1]).sort();

// Covers: AIC-REQ-04#A11; related A3/A5/A6.
test('the single map owns each current skill once and preserves nonlinear topic semantics',()=>{
 const graph=getSkillGraph(),global=getGlobalTopicGraph();
 assert.deepEqual(graph.groups.flatMap(g=>g.skills.map(s=>s.id)).sort(),canonical);
 assert.equal(new Set(graph.groups.flatMap(g=>g.skills.map(s=>s.id))).size,canonical.length);
 assert.equal(global.nodes.length,10);assert.equal(global.edges.length,13);assert.equal(global.loops.length,2);
 assert.equal(global.hub,undefined);assert.equal(global.edges.some(e=>e.kind==='feedback'&&e.from==='quality'&&e.to==='planning'),true);
 assert.equal(global.edges.some(e=>e.kind==='support'&&e.from==='foundation'&&e.to==='planning'),true);
 for(const group of graph.groups)for(const skill of group.skills){assert.equal(getNodeForSkill(skill.id),group.id);assert.deepEqual(getNodeDetails(group.id).skills.map(s=>s.id).sort(),group.skills.map(s=>s.id).sort());}
 const copy=getGlobalTopicGraph();copy.edges.length=0;assert.equal(getGlobalTopicGraph().edges.length,13);
});
// Covers: AIC-REQ-04#A11; related A3/A5/A6.
test('canonical membership rejects omissions, duplicates and unknown skills',()=>{
 const records=canonical.map(id=>({id}));assert.equal(validateCatalog(records,canonical),true);
 assert.throws(()=>validateCatalog(records.slice(1),canonical),/Missing/);
 assert.throws(()=>validateCatalog([...records,records[0]],canonical),/Duplicate/);
 assert.throws(()=>validateCatalog([...records,{id:'not-a-skill'}],canonical),/Unknown/);
});
// Covers: AIC-REQ-04#A11; related A3/A5/A6.
test('topic disclosure retains at most one owner and rejects invalid identifiers',()=>{
 const state=createTopicState();assert.deepEqual(state.expanded(),[]);
 state.reveal('planning');state.reveal('planning');assert.deepEqual(state.expanded(),['planning']);
 state.toggle('quality');assert.deepEqual(state.expanded(),['quality']);state.toggle('quality');assert.deepEqual(state.expanded(),[]);
 assert.throws(()=>state.reveal('__proto__'),/Unknown/);assert.deepEqual(state.expanded(),[]);
 for(const f of [getNodeDetails,getNodeForSkill,getSkillNeighborhood,getSkillForest])assert.throws(()=>f('not-a-node'),/Unknown/);
});
// Covers: AIC-REQ-04#A11; related A3/A5/A6.
test('local forests are placement aids and retain canonical edge identities',()=>{
 const graph=getSkillGraph(),edges=new Set(graph.edges.map(e=>e.id));
 for(const group of graph.groups){const forest=getSkillForest(group.id);assert.equal(forest.connections.every(e=>edges.has(e.id)),true);assert.equal(forest.connections.every(e=>group.skills.some(s=>s.id===e.from)&&group.skills.some(s=>s.id===e.to)),true);}
 assert.deepEqual(new Set(getSkillNeighborhood('prepare-release').edges.map(e=>e.id)),new Set(['prepare-release__build-project','prepare-release__changelog-video','prepare-release__publish-release']));
 for(const id of canonical)assert.ok(dictionary.skills[id].purpose);
});
// Covers: AIC-REQ-04#A11; related A3/A5/A6.
test('topic routing remains clear with every possible expanded topic',()=>{
 const graph=getGlobalTopicGraph(),origin={left:0,top:0,right:1200,bottom:1100};
 for(const active of graph.nodes){
  const heights=[1,2,3].map(row=>graph.nodes.some(n=>n.row===row&&n.id===active.id)?420:120),tops=[30,30+heights[0]+90,30+heights[0]+90+heights[1]+90];
  const rects=new Map(graph.nodes.map(n=>[n.id,{left:20+(n.column-1)*300,right:220+(n.column-1)*300,top:tops[n.row-1],bottom:tops[n.row-1]+(n.id===active.id?420:120),width:200,height:n.id===active.id?420:120}]));
  for(const edge of graph.edges){const route=routeTopicRelationship(edge,rects,origin);for(let i=1;i<route.points.length;i++){const a=route.points[i-1],b=route.points[i];for(let t=.01;t<1;t+=.01){const x=a[0]+(b[0]-a[0])*t,y=a[1]+(b[1]-a[1])*t;for(const [id,r] of rects)assert.ok(!(x>r.left+.5&&x<r.right-.5&&y>r.top+.5&&y<r.bottom-.5),`${active.id}: ${edge.id} crosses ${id}`);}}}
 }
 assert.throws(()=>routeTopicRelationship({id:'unknown'},new Map(),origin),/Unknown/);
});
// Covers: AIC-REQ-04#A11; related A3/A5/A6.
test('topic names and purpose have one locale owner across map and panel',()=>{
 for(const [id,topic] of Object.entries(dictionary.topics)){
  assert.equal(Object.hasOwn(dictionary.contexts[id],'title'),false,'Duplicate editable topic name');
  assert.equal(Object.hasOwn(dictionary.contexts[id].help,'point'),false,'Duplicate editable topic purpose');
  assert.equal(getNodeDetails(id).title,topic.name);
  assert.equal(getNodeDetails(id).help.point,topic.purpose);
 }
});
