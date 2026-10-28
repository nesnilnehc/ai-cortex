import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
import {initializeLanguage} from '../../website/language.mjs';
const root=new URL('../../website/explore/',import.meta.url);

// Covers: AIC-REQ-04#A11; related A3/A5/A7/A10.
test('explorer language selection stays in the explorer family and preserves context',()=>{
 const redirects=[];
 const env={location:{href:'https://example.test/explore/?campaign=docs#story',replace:u=>redirects.push(u)},navigator:{languages:['zh-CN']},localStorage:{getItem:()=>null,setItem(){}}};
 initializeLanguage(env,'en',{en:'/explore/',zh:'/explore/zh.html'});
 assert.equal(redirects[0],'https://example.test/explore/zh.html?campaign=docs#story');
});
// Covers: AIC-REQ-04#A11; related A3/A5/A7/A10.
test('language route maps reject unsafe or incomplete destinations before navigation',()=>{
 const env={location:{href:'https://example.test/explore/',replace(){throw Error('Must not navigate');}},navigator:{languages:['en']},localStorage:{getItem:()=>null}};
 for(const routes of [{en:'/explore/'},{en:'//outside.test/',zh:'/explore/zh.html'},{en:'/explore/',zh:'https://outside.test/'}])assert.throws(()=>initializeLanguage(env,'en',routes),/route/i);
});
// Covers: AIC-REQ-04#A11; related A3/A5/A7/A10.
test('source URLs use canonical asset revision and reject path escape',async()=>{
 const {sourceUrl}=await import('../../website/explore/source-links.mjs');
 const manifest=JSON.parse(readFileSync(new URL('source-manifest.json',root)));
 assert.match(manifest.assetsRevision,/^[a-f0-9]{40}$/);
 assert.equal(sourceUrl('skills/define-mission/SKILL.md'),`${manifest.repositoryUrl}/blob/${manifest.assetsRevision}/skills/define-mission/SKILL.md`);
 for(const path of ['../../private','skills/../private','https://outside.test/','/skills/x','skills/%2e%2e/private'])assert.throws(()=>sourceUrl(path),/source|path/i);
});
// Covers: AIC-REQ-04#A11; related A3/A5/A7/A10.
test('both locale dictionaries cover every skill with meaningful usage, no language fallback',async()=>{
 const {getCopy,getSkillGuidance,validateLocales}=await import('../../website/explore/locale.mjs');
 const zh=JSON.parse(readFileSync(new URL('locales/zh.json',root))),en=JSON.parse(readFileSync(new URL('locales/en.json',root)));
 assert.equal(validateLocales(zh,en),true);
 const {guidanceIds}=await import('../../website/explore/skill-guidance.mjs');
 const canonical=readFileSync(new URL('../../skills/INDEX.md',import.meta.url),'utf8');
 const ids=[...canonical.matchAll(/\]\(\.\/([^/]+)\/SKILL\.md\)/g)].map(m=>m[1]).sort();
 assert.deepEqual(Object.keys(en.skills).sort(),ids);assert.deepEqual([...guidanceIds].sort(),ids);
 for(const id of ids)for(const lang of ['en','zh'])for(const key of ['when','provide','use','result'])assert.ok(getSkillGuidance(id,lang)[key].trim().length>12,`${id}/${lang}/${key}`);
 const bad=structuredClone(en);delete bad.skills['define-mission'].provide;assert.throws(()=>validateLocales(zh,bad),/locale|missing|field/i);
 assert.throws(()=>getCopy('en','not-a-key'),/copy|key/i);
 assert.throws(()=>getCopy('fr','title'),/locale/i);
});
// Covers: AIC-REQ-04#A11; related A3/A5/A7/A10.
test('both static editions provide sources without scripting and no experiment dependencies',()=>{
 for(const edition of ['index.html','zh.html']){
  const html=readFileSync(new URL('../'+edition,root),'utf8');
  assert.match(html,/id="source-fallback"[^>]+https:\/\/github.com/);
  assert.match(html,/rel="canonical"/);assert.match(html,/hreflang="en"/);assert.match(html,/hreflang="zh-CN"/);
  assert.doesNotMatch(html,/\.\.\/\.\.\/|本地原型|仅本地预览/);
  assert.ok(existsSync(new URL('explorer-host.mjs',root)));
 }
});
// Covers: AIC-REQ-04#A11; related A3/A5/A7/A10.
test('home and install navigation keeps an explicit locale when storage is blocked',async()=>{
 const {getExplorerRoutes}=await import('../../website/explore/site-contract.mjs');
 assert.equal(getExplorerRoutes('en').home,'/?lang=en');
 assert.equal(getExplorerRoutes('zh').home,'/zh.html?lang=zh');
 assert.equal(getExplorerRoutes('en').alternate,'/zh.html?lang=zh#capabilities');
 assert.throws(()=>getExplorerRoutes('fr'),/locale/i);
});
// Covers: AIC-REQ-04#A11; related A3/A5/A7/A10.
test('locale validation cannot translate identities or change typed state',async()=>{
 const {validateLocales}=await import('../../website/explore/locale.mjs');
 const zh=JSON.parse(readFileSync(new URL('locales/zh.json',root))),en=JSON.parse(readFileSync(new URL('locales/en.json',root)));
 const wrongIdentity=structuredClone(en);wrongIdentity.contexts.planning.skills[0]='publish-release';
 assert.throws(()=>validateLocales(zh,wrongIdentity),/identity|locale/i);
 const wrongState=structuredClone(en);wrongState.extras.gates.pass.checksComplete=false;
 assert.throws(()=>validateLocales(zh,wrongState),/identity|locale/i);
 const wrongShape=structuredClone(en);wrongShape.extras.topicMap=[];
 assert.throws(()=>validateLocales(zh,wrongShape),/locale/i);
});
