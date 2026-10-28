import {test} from 'node:test';
import assert from 'node:assert/strict';
import {getNodeDetails} from './panel-model.mjs';
import {getHelpLabels,getWorkHelp,getMapProjection} from './work-map.mjs';
test('plain-language work labels explain context without geometric prerequisites',()=>{
 const labels=getHelpLabels();assert.match(labels.point,/工作/);
 assert.ok(!['point','line','plane'].some(key=>/[点线面]：/.test(labels[key])));
 labels.point='changed';assert.notEqual(getHelpLabels().point,'changed');
});
test('selected work retains concrete contextual help and all its skills',()=>{
 const detail=getNodeDetails('design');assert.match(detail.help.point,/审查/);
 assert.deepEqual(detail.help,getWorkHelp('design'));assert.ok(detail.skills.length);
});
test('every mapped subject has complete isolated help and unknown subjects fail',()=>{
 for(const id of Object.keys(getMapProjection().nodes)){
  const help=getWorkHelp(id);assert.ok(help.point&&help.line&&help.plane);
 }
 const before=getWorkHelp('design');before.point='mutated';assert.notEqual(getWorkHelp('design').point,'mutated');
 assert.throws(()=>getWorkHelp('unknown'));
});
test('one work map retains subjects, relationship meanings and isolated snapshots',()=>{
 const map=getMapProjection();assert.equal(map.nodes.design.title,'把事情说清楚');
 assert.equal(map.edges['build-quality'],'修复后复核');
 assert.match(map.guide,/判断依据/);assert.ok(map.boundary&&map.feedback);
 map.nodes.design.title='mutated';assert.equal(getMapProjection().nodes.design.title,'把事情说清楚');
});
