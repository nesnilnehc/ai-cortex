import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {getNodeDetails} from './panel-model.mjs';
import {catalog} from './workflow.mjs';
const html=readFileSync(new URL('./index.html',import.meta.url),'utf8');
test('one map and one contextual panel own the only request editor and copy action',()=>{
 assert.equal((html.match(/class="relations-canvas(?:\s[^"]*)?"/g)||[]).length,1);
 const panel=html.slice(html.indexOf('<aside id="detail-panel"'),html.indexOf('</aside>'));
 for(const id of ['request-text','copy-request']){
  assert.ok(panel.includes(`id="${id}"`));
  assert.equal((html.match(new RegExp(`id="${id}"`,'g'))||[]).length,1);
 }
 assert.ok(html.includes('<dialog id="tools"'));
 for(const old of ['class="story-scene"','class="topic-heading"','class="use-section"','class="example-options"'])assert.ok(!html.includes(old));
});
test('primary skill access is an expanded graph rather than a dropdown or collapsed list',()=>{
 assert.ok(html.includes('id="skill-groups"'));
 for(const id of ['node-asset-select','all-node-tools','recommended-tools'])assert.ok(!html.includes(`id="${id}"`));
});

test('the single work map has no perspective selector or alternate-view entry',()=>{
 assert.ok(!html.includes('id="help-perspective"'));
 assert.ok(!html.includes('class="lens-picker"'));
 assert.ok(!html.includes('换个角度看帮助'));
});
