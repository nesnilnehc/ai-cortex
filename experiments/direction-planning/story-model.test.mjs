import {test} from 'node:test';
import assert from 'node:assert/strict';
import {getChapter,getSimpleGate,getToolGroups,chapterIds} from './story-model.mjs';
test('plain-language topics remain selectable without defining a next stage',()=>{
 assert.deepEqual(chapterIds,['research','planning','design','build','quality','commit','release']);
 assert.deepEqual(chapterIds.map(id=>getChapter(id).tile),[0,1,2,3,4,5,6]);
 for(const id of chapterIds){const chapter=getChapter(id);assert.ok(chapter.title.length<=22);assert.ok(chapter.alt);}
 assert.throws(()=>getChapter('unknown'));
});
test('quality evidence is distinct from permission to commit or publish',()=>{
 assert.equal(getSimpleGate('missing').checksComplete,false);
 assert.match(getSimpleGate('pass').body,/分别核对/);
 assert.throws(()=>getSimpleGate('unknown'));
});
test('all 70 tools remain available in grouped disclosure and search',()=>{
 const groups=getToolGroups('');assert.equal(groups.length,9);
 const ids=groups.flatMap(group=>group.skills.map(skill=>skill.id));assert.equal(ids.length,70);assert.equal(new Set(ids).size,70);
 assert.deepEqual(getToolGroups('commit-work').flatMap(group=>group.skills.map(skill=>skill.id)),['commit-work']);
 assert.equal(getToolGroups('no-matching-tool-xyz').length,0);
});
