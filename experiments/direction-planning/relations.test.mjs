import {test} from 'node:test';
import assert from 'node:assert/strict';
import {relations,getExample,getPrerequisites,getMapCoverage} from './relations.mjs';
import {catalog} from './workflow.mjs';
test('the map separates guidance, loops, prerequisites, feedback and anytime support',()=>{
 assert.deepEqual([...new Set(relations.map(x=>x.type))].sort(),['anytime','feedback','guidance','loop','prerequisite']);
 assert.ok(relations.some(x=>x.type==='loop'&&x.from==='build'&&x.to==='quality'));
 assert.ok(!relations.some(x=>x.from==='commit'&&x.to==='release'));
});
test('publication and announcement each have their own prerequisites',()=>{
 assert.ok(getPrerequisites('publish').includes('发布包就绪'));
 assert.ok(getPrerequisites('publish').includes('本次发布已获授权'));
 assert.ok(getPrerequisites('announce').includes('实际发布结果'));
 assert.ok(getPrerequisites('commit').includes('审阅暂存差异'));
 assert.throws(()=>getPrerequisites('unknown'));
});
test('examples highlight relevant relationships without inventing a completed stage',()=>{
 assert.ok(getExample('bug').edges.includes('build-quality'));
 assert.ok(getExample('requirements').edges.includes('planning-design'));
 assert.ok(getExample('release').edges.includes('release-ready'));
 assert.equal(getExample('release').focus,'release');
 assert.throws(()=>getExample('unknown'));
});
test('all registered skills still have an entry, without depending on a linear order',()=>{
 assert.deepEqual(getMapCoverage().sort(),catalog.map(x=>x.id).sort());
 assert.equal(getMapCoverage().length,70);
});
test('the entry has no previous/next sequence controls or automatic review-to-commit action',async()=>{
 const {readFileSync}=await import('node:fs');
 const html=readFileSync(new URL('./index.html',import.meta.url),'utf8');
 const script=readFileSync(new URL('./story.mjs',import.meta.url),'utf8');
 assert.ok(!html.includes('id="next"'));
 assert.ok(!html.includes('id="previous"'));
 assert.ok(!script.includes('getNextChapter'));
 const {getSkillGraph}=await import('./skill-graph.mjs');
 const groups=getSkillGraph().groups;
 assert.deepEqual(groups.filter(group=>group.availability==='anytime').map(group=>group.id).sort(),['collaboration','foundation','research']);
 assert.match(groups.find(group=>group.id==='release').note,/发布前要核对/);
});
