import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {getTopicMap,createTopicState} from './topic-map.mjs';
import {getSkillGraph} from './skill-graph.mjs';
test('topic topology covers every topic once and retains only sourced cross-topic edges',()=>{
 const map=getTopicMap(),graph=getSkillGraph();
 assert.deepEqual(map.regions.flatMap(r=>r.topics).sort(),graph.groups.map(g=>g.id).sort());
 assert.equal(new Set(map.regions.flatMap(r=>r.topics)).size,10);
 assert.deepEqual(map.edges.flatMap(e=>e.evidence).sort(),graph.edges.filter(e=>e.from!==e.to&&graph.groups.find(g=>g.skills.some(s=>s.id===e.from)).id!==graph.groups.find(g=>g.skills.some(s=>s.id===e.to)).id).map(e=>e.id).sort());
 assert.ok(map.edges.find(e=>e.kind==='loop'&&e.from==='quality'&&e.to==='build'));
 for(const edge of [...map.edges,...map.loops]){assert.ok(edge.condition);for(const source of edge.sources)assert.ok(readFileSync(new URL(source.path,import.meta.url),'utf8').includes(source.quote));}
 assert.deepEqual(map.regions.find(r=>r.kind==='support').topics,['research','foundation','collaboration']);
});
test('disclosure can expand, collapse, reveal a searched peer, and reject unknown topics',()=>{
 const state=createTopicState();assert.deepEqual(state.expanded(),[]);
 state.toggle('quality');assert.deepEqual(state.expanded(),['quality']);
 state.toggle('quality');assert.deepEqual(state.expanded(),[]);
 state.reveal('build');state.reveal('build');assert.deepEqual(state.expanded(),['build']);
 state.reveal('quality');assert.deepEqual(state.expanded(),['quality']);
 state.collapseAll();assert.deepEqual(state.expanded(),[]);
 assert.throws(()=>state.toggle('missing'),/Unknown/);
 const map=getTopicMap();map.regions[0].topics.length=0;assert.ok(getTopicMap().regions[0].topics.length);
});
