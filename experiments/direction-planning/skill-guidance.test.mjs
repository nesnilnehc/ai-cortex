import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {catalog} from './workflow.mjs';
import {getSkillGuidance,guidanceIds} from './skill-guidance.mjs';

test('every current skill has four Chinese usage fields grounded in the current definition',()=>{
 assert.deepEqual([...guidanceIds].sort(),catalog.map(x=>x.id).sort());
 for(const {id} of catalog){
  const guide=getSkillGuidance(id);
  for(const key of ['when','provide','use','result'])assert.match(guide[key],/[\u4e00-\u9fff]/,`${id}/${key}`);
  assert.ok(guide.use.includes(id),`${id}: usable natural-language request`);
  const source=readFileSync(new URL(`../../skills/${id}/SKILL.md`,import.meta.url));
  assert.equal(guide.sourceHash,createHash('sha256').update(source).digest('hex'),`${id}: definition changed; review summary`);
 }
});
test('usage guidance is isolated and unknown skills cannot borrow another skill instructions',()=>{
 assert.throws(()=>getSkillGuidance('unknown'),/Unknown skill/);
 const guide=getSkillGuidance('commit-work');guide.result='changed';
 assert.notEqual(getSkillGuidance('commit-work').result,'changed');
});
test('high-impact boundaries remain distinct in the Chinese explanation',()=>{
 assert.match(getSkillGuidance('commit-work').result,/不.*推送/);
 assert.match(getSkillGuidance('publish-release').provide,/就绪|ready/);
 assert.match(getSkillGuidance('announce-release').provide,/实际发布|已发布/);
 assert.match(getSkillGuidance('review-requirements').result,/不.*改写/);
 assert.match(getSkillGuidance('update-roadmap').result,/不.*Now.*Next.*Later/);
 assert.match(getSkillGuidance('prioritize-backlog').result,/不.*路线图/);
 assert.match(getSkillGuidance('manage-secret').provide,/不要.*聊天/);
 assert.match(getSkillGuidance('scaffold-agent-tests').provide,/测试契约/);
});

test('internal assessment is explained through its public coordinator rather than advertised as a direct invocation',()=>{
 const guide=getSkillGuidance('assess-product-opportunity');
 assert.equal(guide.entry,'internal');
 assert.match(guide.use,/请用 product-opportunity-analysis/);
 assert.doesNotMatch(guide.use,/请用 assess-product-opportunity/);
 assert.match(guide.when,/内部/);
});
