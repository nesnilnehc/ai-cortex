import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {getGlobalTopicGraph,routeTopicRelationship} from './global-topic-graph.mjs';
import {getSkillGraph} from './skill-graph.mjs';
test('direct topic relations replace the work hub with sourced inputs, feedback and specific support',()=>{
 const graph=getGlobalTopicGraph();assert.equal(graph.hub,undefined);assert.equal(graph.associations,undefined);
 assert.deepEqual(graph.nodes.map(n=>n.id).sort(),getSkillGraph().groups.map(g=>g.id).sort());
 assert.equal(graph.edges.length,13);assert.ok(graph.edges.every(e=>e.from!==e.to&&e.from!=='current-work'&&e.to!=='current-work'));
 const reached=new Set(['direction']);for(let i=0;i<10;i++)for(const e of graph.edges)if(reached.has(e.from)||reached.has(e.to)){reached.add(e.from);reached.add(e.to);}assert.equal(reached.size,10);
 for(const edge of graph.edges){assert.ok(edge.condition);assert.ok(edge.basis);assert.ok(edge.sources.length);for(const source of edge.sources)assert.ok(readFileSync(new URL(source.path,import.meta.url),'utf8').includes(source.quote),edge.id);}
 assert.ok(graph.edges.some(e=>e.from==='quality'&&e.to==='planning'&&e.kind==='feedback'));
 assert.ok(graph.edges.some(e=>e.from==='foundation'&&e.to==='planning'&&e.kind==='support'));
 assert.ok(graph.edges.some(e=>e.from==='research'&&e.to==='collaboration'&&e.kind==='support'));
 assert.match(graph.edges.find(e=>e.id==='research-planning').condition,/不.*自动|不会.*自动/);
 const copy=getGlobalTopicGraph();copy.edges.length=0;assert.equal(getGlobalTopicGraph().edges.length,13);
});
test('desktop relation routes use actual topic ports and keep labels out of topic contents',()=>{
 const graph=getGlobalTopicGraph(),origin={left:0,top:0,right:1200,bottom:640};const nodes=new Map(graph.nodes.map(n=>[n.id,{left:20+(n.column-1)*300,right:220+(n.column-1)*300,top:30+(n.row-1)*210,bottom:150+(n.row-1)*210,width:200,height:120}]));
 for(const edge of graph.edges){const route=routeTopicRelationship(edge,nodes,origin,false);assert.ok(route.points.length>=2);assert.ok(Number.isFinite(route.label[0])&&Number.isFinite(route.label[1]));for(const rect of nodes.values())assert.ok(!(route.label[0]>rect.left&&route.label[0]<rect.right&&route.label[1]>rect.top&&route.label[1]<rect.bottom),edge.id);}
 assert.throws(()=>routeTopicRelationship({id:'unknown'},nodes,origin,false),/Unknown/);
});
test('expanded topics can grow without forcing peer cards tall or routing through their contents',()=>{
 const graph=getGlobalTopicGraph(),origin={left:0,top:0,right:1200,bottom:1100};
 for(const active of graph.nodes){
  const heights=[1,2,3].map(row=>graph.nodes.some(n=>n.row===row&&n.id===active.id)?420:120),tops=[30,30+heights[0]+90,30+heights[0]+90+heights[1]+90];
  const rects=new Map(graph.nodes.map(n=>[n.id,{left:20+(n.column-1)*300,right:220+(n.column-1)*300,top:tops[n.row-1],bottom:tops[n.row-1]+(n.id===active.id?420:120),width:200,height:n.id===active.id?420:120}]));
  for(const edge of graph.edges){const route=routeTopicRelationship(edge,rects,origin,false);for(let i=1;i<route.points.length;i++){const a=route.points[i-1],b=route.points[i];for(let t=.01;t<1;t+=.01){const x=a[0]+(b[0]-a[0])*t,y=a[1]+(b[1]-a[1])*t;for(const [id,r] of rects)assert.ok(!(x>r.left+.5&&x<r.right-.5&&y>r.top+.5&&y<r.bottom-.5),`${active.id}: ${edge.id} crosses ${id}`);}}}
 }
});
