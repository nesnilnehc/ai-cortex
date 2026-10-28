// AIC-REQ-08: new catalogue members remain discoverable with usable bilingual guidance.
import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
const read=path=>JSON.parse(readFileSync(new URL('../../website/explore/'+path,import.meta.url),'utf8'));
// Covers: AIC-REQ-08#AC1.
test('eli5 and ponytail are present exactly once in catalogue and both locales',async()=>{
 const metadata=read('skill-metadata.json'),classification=read('classification.json');
 const {findSkills}=await import('../../website/explore/workflow.mjs');
 for(const id of ['eli5','ponytail']){
  assert.ok(metadata.skills[id],`${id} metadata is missing`);
  assert.ok(metadata.groupOrder.includes(metadata.skills[id].owner));
  assert.equal(classification.groups.flatMap(g=>g.skillIds).filter(x=>x===id).length,1);
  assert.ok(findSkills({query:id}).some(skill=>skill.id===id));
  const source=readFileSync(new URL(`../../skills/${id}/SKILL.md`,import.meta.url));
  assert.equal(metadata.skills[id].sourceHashes[`skills/${id}/SKILL.md`],createHash('sha256').update(source).digest('hex'));
  for(const lang of ['en','zh'])for(const field of ['name','purpose','when','provide','use','result'])assert.ok(read(`locales/${lang}.json`).skills[id]?.[field]?.trim(),`${id}/${lang}/${field}`);
 }
});

// Covers: AIC-REQ-08#AC1, AIC-REQ-08#AC7.
test('provenance requires full coverage, three categories and revision-bound safe evidence',async()=>{
 const {validateProjection,getProvenance}=await import('../../website/explore/provenance.mjs');
 const revision='a'.repeat(40),evidence=`https://github.com/nesnilnehc/ai-cortex/blob/${revision}/evidence/a.json`;
 const data={schema_version:1,source_revision:revision,skills:{a:{classification:'native',evidence:[evidence]},b:{classification:'third_party_original',evidence:[evidence]},c:{classification:'third_party_adapted',evidence:[evidence]}}};
 assert.equal(validateProjection(data,['a','b','c']),data);
 assert.equal(getProvenance(data,'a',read('locales/en.json').provenance).label,'AI Cortex original');
 assert.equal(getProvenance(data,'c',read('locales/zh.json').provenance).label,'第三方改编');
 for(const alter of [d=>delete d.skills.a,d=>d.skills.a.classification='unverified',d=>d.skills.a.evidence=['javascript:alert(1)'],d=>d.skills.a.evidence=[evidence.replace(revision,'b'.repeat(40))],d=>d.skills.a.evidence=[evidence.replace('/evidence/a.json','/%2e%2e/private')],d=>d.skills.a.evidence=[],d=>d.skills.a.extra='private']){
  const bad=structuredClone(data);alter(bad);assert.throws(()=>validateProjection(bad,['a','b','c']));
 }
 const preview={schema_version:1,source_revision:null,delivery_ready:false,skills:{a:{classification:'native',evidence:['/provenance-evidence/a.json']}}};
 assert.throws(()=>validateProjection(preview,['a']));assert.equal(validateProjection(preview,['a'],{allowPreview:true}),preview);
 assert.throws(()=>getProvenance(data,'missing',read('locales/en.json').provenance));
});

// Covers: AIC-REQ-08#AC6.
test('evidence actions stay siblings of selection controls and carry accessible names',async()=>{
 const {frameSkill}=await import('../../website/explore/provenance.mjs');
 const make=tag=>({tagName:tag,children:[],attrs:{},append(...items){this.children.push(...items);},setAttribute(key,value){this.attrs[key]=value;}});
 const doc={createElement:make},control=make('button'),revision='a'.repeat(40);
 const data={schema_version:1,source_revision:revision,skills:{a:{classification:'third_party_adapted',evidence:[`https://github.com/nesnilnehc/ai-cortex/blob/${revision}/evidence/a.json`]}}};
 const frame=frameSkill(control,'a',data,read('locales/en.json').provenance,doc);
 assert.equal(frame.children.includes(control),true);
 assert.equal(control.children.length,0);
 const badge=frame.children.find(n=>n.tagName==='span');assert.equal(badge.textContent,'Third-party adapted');
 const links=frame.children.find(n=>n.tagName==='nav');const anchor=links.children[0];assert.equal(anchor.target,'_blank');assert.match(anchor.attrs['aria-label'],/a/);assert.equal(anchor.rel,'noopener');
});

test('reviewed catalogue bootstrap validates before activating renderers',async()=>{
 const {initializeProvenance,decorateSkill}=await import('../../website/explore/provenance.mjs');
 const revision='a'.repeat(40),data={schema_version:1,source_revision:revision,skills:{a:{classification:'native',evidence:[`https://github.com/nesnilnehc/ai-cortex/blob/${revision}/evidence/a.json`]}}};
 const copy=read('locales/en.json').provenance,control={};
 assert.equal(await initializeProvenance({manifest:{},ids:['a'],copy}),true);
 assert.equal(decorateSkill(control,'a',copy),control);
 let failure='';
 assert.equal(await initializeProvenance({manifest:{provenanceRevision:revision},ids:['a'],copy,fetcher:async()=>({ok:false}),reportError:text=>failure=text}),false);
 assert.equal(failure,copy.unavailable);
 assert.equal(await initializeProvenance({manifest:{provenanceRevision:revision},ids:['a'],copy,fetcher:async()=>({ok:true,json:async()=>data}),reportError:()=>assert.fail('unexpected error')}),true);
 const make=tag=>({tagName:tag,children:[],append(...xs){this.children.push(...xs);},setAttribute(){}});
 assert.equal(decorateSkill(make('button'),'a',copy,{createElement:make}).className,'provenance-entry');
});

test('catalogue summary uses the current membership count',async()=>{
 const {getCopy}=await import('../../website/explore/locale.mjs');
 const count=Object.keys(read('skill-metadata.json').skills).length;
 for(const locale of ['en','zh'])assert.ok(getCopy(locale,'ca39d237326',[count]).includes(String(count)));
});

test('search dialogue groups cover the whole catalogue including both intakes',async()=>{
 const {getToolGroups}=await import('../../website/explore/story-model.mjs');
 const expected=Object.keys(read('skill-metadata.json').skills).sort();
 assert.deepEqual(getToolGroups().flatMap(g=>g.skills.map(s=>s.id)).sort(),expected);
 for(const id of ['eli5','ponytail'])assert.ok(getToolGroups(id).some(g=>g.skills.some(s=>s.id===id)));
});

test('catalogue loading supplies a bounded cancellation signal',async()=>{
 const {initializeProvenance}=await import('../../website/explore/provenance.mjs');
 const revision='a'.repeat(40),signal=AbortSignal.abort();let observed;
 const copy=read('locales/en.json').provenance;
 const result=await initializeProvenance({manifest:{provenanceRevision:revision},ids:['a'],copy,signalFactory:()=>signal,fetcher:async(url,options)=>{observed=options?.signal;throw new Error('aborted fixture');}});
 assert.equal(result,false);assert.equal(observed,signal);
});

// Covers: AIC-REQ-08#AC1; approved original-badge omission.
test('confirmed originals have evidence access without a badge',async()=>{
 const {frameSkill}=await import('../../website/explore/provenance.mjs');
 const make=tag=>({tagName:tag,children:[],attrs:{},append(...items){this.children.push(...items);},setAttribute(key,value){this.attrs[key]=value;}});
 const revision='a'.repeat(40),data={schema_version:1,source_revision:revision,skills:{a:{classification:'native',evidence:[`https://github.com/nesnilnehc/ai-cortex/blob/${revision}/evidence/a.json`]}}};
 const frame=frameSkill(make('button'),'a',data,read('locales/en.json').provenance,{createElement:make});
 assert.equal(frame.children.some(n=>n.className==='provenance-badge'),false);
 assert.equal(frame.children.some(n=>n.tagName==='nav'),true);
 assert.throws(()=>frameSkill(make('button'),'missing',data,read('locales/en.json').provenance,{createElement:make}));
});

test('catalogue failure exposes one safe diagnostic at its owning boundary',async()=>{
 const {initializeProvenance}=await import('../../website/explore/provenance.mjs');
 const errors=[];
 const result=await initializeProvenance({manifest:{provenanceRevision:'a'.repeat(40)},ids:['a'],copy:read('locales/en.json').provenance,fetcher:async()=>{throw new Error('private response payload');},reportError:(message,diagnostic)=>errors.push({message,diagnostic})});
 assert.equal(result,false);assert.equal(errors.length,1);
 assert.deepEqual(errors[0].diagnostic,{operation:'provenance.load',outcome:'failed',code:'PROVENANCE_LOAD_FAILED',stage:'fetch'});
 assert.equal(JSON.stringify(errors).includes('private response payload'),false);
});

// Covers: AIC-REQ-08#AC1, AIC-REQ-08#AC7. Real Python generation feeds the browser contract.
test('browser contract consumes the actual pinned generator output',async()=>{
 const root=fileURLToPath(new URL('../../',import.meta.url));
 const script=`import contextlib,importlib.util,io,json,sys
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'scripts'))
spec=importlib.util.spec_from_file_location('provenance_fixture',Path('scripts/test-skill-provenance-v2.py'))
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
case=module.ProvenanceV2Tests('test_native_requires_creation_and_actual_confirmation_record')
case.setUp()
try:
 index=case.committed_site()
 with contextlib.redirect_stdout(io.StringIO()):
  assert index.main([])==0
 print(json.dumps({'projection':json.loads((case.root/'website/explore/skill-provenance.json').read_text()),'index':(case.skills/'INDEX.md').read_text(),'page':(case.root/'website/index.html').read_text()}))
finally:
 case.doCleanups()
`;
 const generated=JSON.parse(execFileSync('python3',['-c',script],{cwd:root,encoding:'utf8',timeout:60000}));
 const {validateProjection}=await import('../../website/explore/provenance.mjs');
 assert.equal(validateProjection(generated.projection,['alpha']).skills.alpha.classification,'native');
 assert.equal(generated.projection.skills.alpha.evidence.length,2);
 assert.ok(generated.index.includes('[evidence]'));assert.equal(generated.index.includes('**AI Cortex original**'),false);
 assert.ok(generated.page.includes('provenance-evidence'));assert.equal(generated.page.includes('data-provenance="native"'),false);
 const incomplete=structuredClone(generated.projection);delete incomplete.skills.alpha;
 assert.throws(()=>validateProjection(incomplete,['alpha']));
});

// Covers: AIC-REQ-08#AC6. Legacy no-script catalogues use the same badge layout.
test('legacy fallback pages load the shared local catalogue styles',()=>{
 for(const name of ['index.html','zh.html']){
  const html=readFileSync(new URL('../../website/explore/'+name,import.meta.url),'utf8');
  for(const path of ['../styles.css','./story.css','./workspace.css','./dual.css']){
   assert.ok(html.includes(`rel="stylesheet" href="${path}?`),`${name} is missing ${path}`);
   assert.ok(readFileSync(new URL('../../website/explore/'+path,import.meta.url),'utf8').length>0);
  }
 }
});
