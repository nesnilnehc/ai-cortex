import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {catalog} from './workflow.mjs';
import {getSkillGraph,getSkillNeighborhood} from './skill-graph.mjs';
test('the expanded graph contains every current skill once in its work context',()=>{
 const graph=getSkillGraph(),ids=graph.groups.flatMap(group=>group.skills.map(skill=>skill.id));
 assert.deepEqual(ids.sort(),catalog.map(skill=>skill.id).sort());assert.equal(new Set(ids).size,ids.length);
 assert.equal(graph.groups.length,10);
});
test('every displayed relationship has distinct known endpoints and an inspected defining source',()=>{
 const graph=getSkillGraph(),ids=new Set(catalog.map(skill=>skill.id)),seen=new Set();
 for(const edge of graph.edges){
  assert.ok(ids.has(edge.from)&&ids.has(edge.to));assert.notEqual(edge.from,edge.to);
  assert.ok(!seen.has(edge.id));seen.add(edge.id);
  const source=readFileSync(new URL(edge.source,import.meta.url),'utf8');
  assert.ok(source.includes(edge.quote),`${edge.id}: source changed`);assert.ok(edge.label&&edge.condition);
  if(edge.kind==='call'||edge.kind==='method')assert.ok(edge.source.includes(`/${edge.from}/`));
 }
});
test('selection exposes all and only direct relations, without fabricating a mandatory sequence',()=>{
 const graph=getSkillGraph();for(const {id} of catalog){
  const actual=getSkillNeighborhood(id),expected=graph.edges.filter(edge=>edge.from===id||edge.to===id);
  assert.deepEqual(actual.edges,expected);
  assert.deepEqual(new Set(actual.related),new Set(expected.map(edge=>edge.from===id?edge.to:edge.from)));
 }
 assert.equal(getSkillNeighborhood('manage-secret').edges.length,0);
 assert.ok(graph.edges.some(edge=>edge.from==='orchestrate-roadmap-planning'&&edge.to==='update-roadmap'&&edge.kind==='suggest'));
 assert.ok(!graph.edges.some(edge=>edge.from==='commit-work'&&edge.to==='publish-release'));
 assert.throws(()=>getSkillNeighborhood('unknown'));
});
test('graph snapshots and neighborhoods are isolated from readers',()=>{
 const graph=getSkillGraph();graph.groups[0].skills[0].purpose='changed';graph.edges[0].label='changed';
 assert.notEqual(getSkillGraph().groups[0].skills[0].purpose,'changed');assert.notEqual(getSkillGraph().edges[0].label,'changed');
});

test('routed arrows enter their target from the reserved outside boundary',async()=>{
 const {routeSkillConnection}=await import('./skill-graph.mjs');
 const left={left:20,right:120,top:40,height:60},right={left:160,right:260,top:40,height:60},below={...left,top:160};
 for(const [from,to] of [[left,right],[right,left],[left,below]]){
  const points=routeSkillConnection(from,to,{left:0,top:0});
  const nearLeft=to.left>=from.right+12;assert.deepEqual(points.at(-1),[nearLeft?to.left:to.right,to.top+to.height/2]);
  assert.ok(nearLeft?points.at(-2)[0]<points.at(-1)[0]:points.at(-2)[0]>points.at(-1)[0]);
 }
 assert.deepEqual(routeSkillConnection(left,right,{left:10,top:10})[0],[110,60]);
});

test('work grouping puts roadmap review with planning and requirement repair with document work',()=>{
 const groups=getSkillGraph().groups;
 assert.ok(groups.find(group=>group.id==='planning').skills.some(skill=>skill.id==='review-roadmap'));
 assert.ok(groups.find(group=>group.id==='design').skills.some(skill=>skill.id==='orchestrate-repair-requirements-loop'));
});

test('orthogonal skill routes stay in dedicated gutters and cross above all nodes',async()=>{
 const {routeSkillConnection}=await import('./skill-graph.mjs');
 const origin={left:0,top:0};
 const a={left:10,right:200,top:50,height:40},b={left:10,right:200,top:150,height:40},c={left:300,right:490,top:250,height:40};
 assert.deepEqual(routeSkillConnection(a,b,origin),[[200,70],[216,70],[216,170],[200,170]]);
 assert.deepEqual(routeSkillConnection(a,c,origin),[[200,70],[250,70],[250,270],[300,270]]);
 assert.deepEqual(routeSkillConnection(c,a,origin),[[300,270],[250,270],[250,70],[200,70]]);
});

test('different relationship meanings have separate routing lanes',async()=>{
 const {routeSkillConnection}=await import('./skill-graph.mjs');
 const a={left:0,right:100,top:30,height:40},b={...a,top:130},origin={left:0,top:0};
 assert.equal(routeSkillConnection(a,b,origin,'call')[1][0],116);
 assert.equal(routeSkillConnection(a,b,origin,'input')[1][0],124);
 assert.equal(routeSkillConnection(a,b,origin,'suggest')[1][0],128);
 assert.throws(()=>routeSkillConnection(a,b,origin,'unknown'),/Unknown relationship/);
});

test('cross-column routes choose a nearby clear horizontal gap rather than the top of the whole graph',async()=>{
 const {routeSkillConnection}=await import('./skill-graph.mjs');
 const a={left:10,right:200,top:50,height:40},b={left:300,right:490,top:250,height:40};
 const obstacles=[a,b,{left:300,right:490,top:30,height:80},{left:230,right:270,top:0,height:300}];
 const route=routeSkillConnection(a,b,{left:0,top:0},'call',obstacles);
 assert.equal(route[2][1],304);assert.equal(route[3][1],304);
});

test('relationship-based forests keep every skill once and give branch links defining evidence',async()=>{
 const {getSkillForest}=await import('./skill-graph.mjs');
 for(const group of getSkillGraph().groups){
  const forest=getSkillForest(group.id),seen=[];
  function visit(nodes){for(const node of nodes){seen.push(node.skill.id);if(node.via){assert.equal(node.via.to,node.skill.id);assert.ok(node.via.source&&node.via.condition);}visit(node.children);}}
  visit(forest.roots);assert.deepEqual(seen.sort(),group.skills.map(skill=>skill.id).sort());
  assert.equal(new Set(seen).size,seen.length);
 }
 const quality=getSkillForest('quality');
 assert.ok(quality.roots.some(node=>node.skill.id==='orchestrate-code-review'));
 const review=quality.roots.find(node=>node.skill.id==='orchestrate-code-review');assert.equal(review.children.length,20);
 assert.ok(getSkillForest('research').roots.some(node=>node.skill.id==='deep-research'),'shared method has no exclusive parent');
 const release=getSkillForest('release').roots.find(node=>node.skill.id==='prepare-release');
 assert.ok(release.children.some(node=>node.skill.id==='publish-release'&&node.via.kind==='input'));
 assert.ok(release.children.some(node=>node.skill.id==='changelog-video'&&node.via.kind==='call'));
 assert.throws(()=>getSkillForest('unknown'));
});

test('a branch connection enters the near side of a child without looping around it',async()=>{
 const {routeSkillConnection}=await import('./skill-graph.mjs');
 const parent={left:10,right:200,top:50,height:40},child={left:300,right:490,top:150,height:40};
 const route=routeSkillConnection(parent,child,{left:0,top:0});
 assert.deepEqual(route.at(-1),[300,170]);assert.ok(route.at(-2)[0]<300);
});
