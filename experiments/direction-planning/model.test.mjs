import { test } from 'node:test';
import assert from 'node:assert/strict';
import { getPlan, getScenario } from './model.mjs';
test('a blocker delays search without reducing its priority', () => {
 const plan=getPlan('delay');
 assert.equal(plan.items.find(x=>x.id==='R1').priority,'P1');
 assert.equal(plan.items.find(x=>x.id==='R1').tier,'Next');
 assert.match(plan.reason,/依赖/);
});
test('urgent work displaces repair but preserves every existing item',()=>{
 const base=getPlan('base'), urgent=getPlan('urgent');
 assert.equal(urgent.items.length,base.items.length+1);
 for(const item of base.items) assert.ok(urgent.items.some(x=>x.id===item.id));
 assert.equal(urgent.items[0].id,'BUG2');
});
test('completion records evidence without claiming a release',()=>{
 const item=getPlan('complete').items.find(x=>x.id==='BUG1');
 assert.equal(item.state,'验收通过'); assert.match(item.condition,/未发布/);
});
test('scenarios have distinct requests and unknown selections reject',()=>{
 const keys=['direction','backlog','existing','change'];
 assert.equal(new Set(keys.map(k=>getScenario(k).prompt)).size,4);
 assert.throws(()=>getPlan('unknown')); assert.throws(()=>getScenario('unknown'));
});
test('plan snapshots do not share mutable items',()=>{
 getPlan('base').items[0].tier='Later';
 assert.equal(getPlan('base').items[0].tier,'Now');
});
