import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {getRelationship,getTrace,getCoverage} from './relationship.mjs';
test('coverage matches the actual planning category, including supporting capabilities',()=>{
 const html=readFileSync(new URL('../../website/zh.html',import.meta.url),'utf8');
 const branch=html.split('id="map-planning"')[1].split('</details>')[0];
 const skills=[...branch.matchAll(/data-class-skill="([^"]+)"/g)].map(m=>m[1]);
 assert.equal(skills.length,16);
 assert.deepEqual([...getCoverage()].sort(),skills.sort());
});
test('trace preserves goal to backlog to roadmap identity under delay',()=>{
 const trace=getTrace('find','delay');
 assert.deepEqual(trace.items.map(x=>x.id),['R1','R3']);
 assert.equal(trace.items.find(x=>x.id==='R1').tier,'Next');
 assert.equal(trace.items.find(x=>x.id==='R1').priority,'P1');
 assert.equal(trace.goal.id,'G2');
});
test('new urgent work traces to reliability without hiding the old work',()=>{
 assert.deepEqual(getTrace('reliable','urgent').items.map(x=>x.id),['BUG2','BUG1']);
 assert.equal(getTrace('all','urgent').items.length,5);
});
test('node details explain inputs outputs and boundaries; unknown keys reject',()=>{
 for(const key of ['direction','goals','backlog','choices','roadmap','feedback','help']){
  const node=getRelationship(key);assert.ok(node.input&&node.output&&node.boundary&&node.example&&node.skills.length);
 }
 assert.throws(()=>getRelationship('unknown'));assert.throws(()=>getTrace('unknown','base'));
});
test('returned data is isolated',()=>{
 getRelationship('direction').skills.length=0;
 assert.equal(getRelationship('direction').skills.length,3);
});
