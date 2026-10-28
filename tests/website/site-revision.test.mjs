// Covers: AIC-REQ-04 A13-A15; direct route, support and translated identity contracts.
import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
const read=p=>JSON.parse(readFileSync(new URL('../../website/'+p,import.meta.url)));
test('global destinations retain directory/install bookmarks and language families',async()=>{
 const n=await import('../../website/site-navigation.mjs');
 assert.equal(n.getSiteDestination('overview','zh').href,'/zh.html?lang=zh#capabilities');
 for(const h of ['#asset-directory','#skills','#specs','#protocols','#rules']){assert.equal(n.getActiveDestination('/zh.html',h),'directory');assert.equal(n.getAlternateDestination('/zh.html',h,'en'),'/?lang=en'+h);}
 assert.equal(n.getActiveDestination('/index.html','#start'),'start');
 assert.equal(n.getActiveDestination('/explore/index.html',''),'overview');
 assert.equal(n.getAlternateDestination('/zh.html','#bogus','en'),'/?lang=en');
 assert.throws(()=>n.getSiteDestination('bogus','zh'));
 assert.throws(()=>n.getSiteDestination('home','fr'));
});
test('localized names remain different from purposes and true identities stay guarded',async()=>{
 const {validateLocales,getSkillGuidance}=await import('../../website/explore/locale.mjs');
 const zh=read('explore/locales/zh.json'),en=read('explore/locales/en.json');
 assert.equal(getSkillGuidance('review-requirements','zh').name,'审查需求');
 for(const id of Object.keys(zh.skills)){assert.match(zh.skills[id].name,/[\u3400-\u9fff]/);assert.notEqual(zh.skills[id].name,zh.skills[id].purpose);assert.ok(en.skills[id].name);}
 assert.equal(validateLocales(zh,en),true);
 const bad=structuredClone(en);bad.contexts.planning.skills[0]='publish-release';assert.throws(()=>validateLocales(zh,bad));
 const empty=structuredClone(en);empty.skills['review-requirements'].name='';assert.throws(()=>validateLocales(zh,empty));
});
test('support scopes have per-target evidence and exclude invented endpoints',async()=>{
 const {getSupportScopes,validateSupportScopes}=await import('../../website/explore/support-scopes.mjs');
 const records=read('explore/support-scopes.json');
 assert.equal(validateSupportScopes(records),true);assert.throws(()=>validateSupportScopes([]));
 for(const provider of ['foundation','collaboration']){const scopes=getSupportScopes(provider,'zh');assert.ok(scopes[0].targets.length>2);for(const target of scopes[0].targets){assert.ok(target.condition);assert.ok(target.sources[0].quote);}}
 assert.throws(()=>getSupportScopes('unknown','zh'));
 const bad=structuredClone(records);bad[0].targets[0].topicId='unknown';assert.throws(()=>validateSupportScopes(bad));
 const missing=structuredClone(records);missing[0].targets[0].sources=[];assert.throws(()=>validateSupportScopes(missing));
});

// Covers: A13; static navigation remains useful without scripts and mirrors its owner.
test('all four native headers mirror shared routes and keep utilities outside primary navigation',()=>{
 const nav=read('site-navigation.json');
 for(const [file,lang] of [['index.html','en'],['zh.html','zh']]){
  const html=readFileSync(new URL('../../website/'+file,import.meta.url),'utf8');
  for(const id of ['home','overview','directory','start']){const tag=html.match(new RegExp('<a[^>]*data-site-destination="'+id+'"[^>]*>[^<]*</a>'))?.[0];assert.ok(tag,id);assert.ok(tag.includes('href="'+nav.destinations[id].routes[lang]+'"'));assert.ok(tag.includes(nav.destinations[id].labels[lang]));}
  const primary=html.match(/<nav[^>]*>([\s\S]*?)<\/nav>/)[1];assert.doesNotMatch(primary,/find-tools|theme|language-link|工作关系|Work relationships/);
  for(const id of ['capabilities','skills','specs','protocols','rules','start'])if(!file.startsWith('explore'))assert.ok(html.includes('id="'+id+'"'));
 }
});

// Covers: A13; native context is a reconciled mirror, not independent editable copy.
test('native classification cards mirror locale-owned names and purposes',()=>{
 for(const [file,lang] of [['index.html','en'],['zh.html','zh']]){
  const html=readFileSync(new URL('../../website/'+file,import.meta.url),'utf8');
  const escaped=value=>value.replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#x27;'}[char]));
  for(const record of Object.values(read('explore/locales/'+lang+'.json').classification)){
   assert.ok(html.includes(`<strong>${escaped(record.name)}</strong>`),`missing encoded classification name: ${record.name}`);
   assert.ok(html.includes(`<small>${escaped(record.purpose)}</small>`),`missing encoded classification purpose: ${record.purpose}`);
  }
 }
});
