import {createExplorerState} from './explorer-state.mjs?v=aic08-provenance-3';
import {mountClassification} from './classification-view.mjs?v=aic08-provenance-3';
import {mountRelationships,createRelationshipRenderer} from './relationship-view.mjs?v=aic08-provenance-3';
import {dictionary} from './locale.mjs?v=aic08-provenance-3';
import {relationships,classification} from './relationship-model.mjs?v=aic08-provenance-3';
import {getSupportScopes} from './support-scopes.mjs?v=aic08-provenance-3';
import {locale,t} from './locale.mjs?v=aic08-provenance-3';
import {sourceUrl} from './source-links.mjs?v=aic08-provenance-3';
import {getExplorerRoutes,explorerLanguageRoutes} from './site-contract.mjs?v=aic08-provenance-3';
import {getGlobalTopicGraph,routeTopicRelationship} from './global-topic-graph.mjs?v=aic08-provenance-3';
import {getTopicMap,createTopicState} from './topic-map.mjs?v=aic08-provenance-3';
import {getSkillGraph,getSkillNeighborhood,getSkillForest,routeSkillConnection} from './skill-graph.mjs?v=aic08-provenance-3';
import {getHelpLabels,getMapProjection} from './work-map.mjs?v=aic08-provenance-3';
import {createRequestState} from './request-state.mjs?v=aic08-provenance-3';
import {catalog} from './workflow.mjs?v=aic08-provenance-3';
import {getSkillGuidance} from './skill-guidance.mjs?v=aic08-provenance-3';
import {getSimpleGate,getToolGroups} from './story-model.mjs?v=aic08-provenance-3';
import {getExample} from './relations.mjs?v=aic08-provenance-3';
import {getNodeDetails,getNodeForSkill,getNodeSkillSelection} from './panel-model.mjs?v=aic08-provenance-3';
import sourceManifest from './source-manifest.json?v=aic08-provenance-3' with {type:'json'};
import {initializeProvenance,decorateSkill} from './provenance.mjs?v=aic08-provenance-3';
if(await initializeProvenance({manifest:sourceManifest,ids:catalog.map(s=>s.id),copy:dictionary.provenance,previewHost:['localhost','127.0.0.1','[::1]'].includes(globalThis.location?.hostname),reportError:(message,diagnostic)=>{console.error(diagnostic);const note=document.createElement('p');note.className='provenance-load-error';note.textContent=message;note.setAttribute('role','alert');const retry=document.createElement('button');retry.type='button';retry.className='secondary';retry.textContent=dictionary.provenance.retry;retry.addEventListener('click',()=>location.reload());note.append(' ',retry);document.querySelector('.explain-heading').append(note);document.querySelector('.view-switch').hidden=true;document.querySelector('#find-tools').hidden=true;}})){
const $=selector=>document.querySelector(selector);
$('.view-switch').append($('#find-tools'));$('.graph-toolbar').hidden=true;
$('#catalogue-summary').textContent=t('ca39d237326',[catalog.length]);
const library=$('#tools');
const explorerState=createExplorerState();let activeView='classification',classificationAdapter,relationshipAdapter,generation=0;
const viewPorts={classification:$('#classification-view'),relations:$('#relations-view')};
const requestState=createRequestState();
let selectedNode=null;
let panelOpener=$('#find-tools');
let activeExample=null;
let selectedSkill=null;
let graphSelection=null;


function usageFields(id){
 const guide=getSkillGuidance(id),dl=document.createElement('dl');dl.className='skill-usage-fields';
 for(const [key,label] of [['when',t('c7bddfe7b8e')],['provide',t('c0bcca5d6e4')],['use',t('cd5ca9e5562')],['result',t('c2f7bc20732')]]){
  const dt=document.createElement('dt'),dd=document.createElement('dd');dt.textContent=label;dd.textContent=guide[key];dl.append(dt,dd);
 }
 return dl;
}
function usageAccess(id){
 const p=document.createElement('p');p.className='skill-access';
 if(getSkillGuidance(id).entry==='internal'){p.textContent=t('c9aaf81b68d');return p;}
 p.append(t('ce325a8409f'));
 const code=document.createElement('code');code.textContent=`skills/${id}/SKILL.md`;p.append(code,t('c101fa19abd'));
 const setup=document.createElement('a');setup.href=getExplorerRoutes(locale).home+'#start';setup.target='_blank';setup.rel='noopener';setup.textContent=t('c8ee8142e28');p.append(setup,t('cb8c19dd611'));return p;
}
function setPanelMode(mode,reveal=false){
 const normalized=mode==='assets'?'usage':mode;try{explorerState.setDetailMode(normalized);}catch{ return; }
 document.body.dataset.panelMode=mode;
 if(reveal&&selectedSkill&&activeView==='relations'){revealTopic(getNodeForSkill(selectedSkill));alignLocalSkill(selectedSkill);ensureTopicVisible(getNodeForSkill(selectedSkill));}
 const showAssets=mode==='assets';
 if(mode!=='work'&&selectedSkill&&graphSelection!==selectedSkill)highlightSkill(selectedSkill);
 $('#selected-tool').hidden=!showAssets;$('#skill-relations').hidden=mode!=='relations';$('#work-explanation').hidden=mode!=='work';$('.panel-copy-action').hidden=mode!=='work';
 $('#panel-assets-button').setAttribute('aria-pressed',String(showAssets));$('#panel-work-button').setAttribute('aria-pressed',String(mode==='work'));$('#panel-relations-button').setAttribute('aria-pressed',String(mode==='relations'));
 $('.panel-body').scrollTop=0;
 const selectedButton=selectedSkill&&document.querySelector(`.skill-node[data-skill="${selectedSkill}"]`);
 if(selectedButton?.checkVisibility()){alignLocalSkill(selectedSkill);ensureTopicVisible(getNodeForSkill(selectedSkill));drawSkillEdges();}
}
function clearDetailProvenance(){const title=$('#detail-title');if(title.parentElement.classList.contains('provenance-entry'))title.parentElement.replaceWith(title);}
function renderSelectedSkill(skill){
 selectedSkill=skill.id;highlightSkill(skill.id);renderSkillRelations(skill.id);
 $('#detail-title').textContent=skill.name===skill.id?skill.id:`${skill.name} · ${skill.id}`;$('#selected-tool-purpose').textContent=skill.purpose;$('#selected-tool-guide').replaceChildren(usageFields(skill.id),usageAccess(skill.id));
 clearDetailProvenance();const title=$('#detail-title'),host=title.parentElement,next=title.nextSibling;const frame=decorateSkill(title,skill.id,dictionary.provenance);if(frame!==title)host.insertBefore(frame,next);
 $('#selected-tool-link').textContent=t('cdaa1554f98',[skill.id]);$('#selected-tool-link').href=sourceUrl(`skills/${skill.id}/SKILL.md`);
}
$('#panel-assets-button').addEventListener('click',()=>setPanelMode('assets',true));
$('#panel-work-button').addEventListener('click',()=>setPanelMode('work'));
$('#panel-relations-button').addEventListener('click',()=>setPanelMode('relations',true));
function clearExample(){
 activeExample=null;$('#example-note').hidden=true;$('#try-example').setAttribute('aria-pressed','false');
 document.querySelectorAll('[data-edge]').forEach(edge=>edge.classList.remove('emphasized'));
}
function renderPrerequisites(detail){
 $('#operation-details').hidden=detail.prerequisites.length===0;$('#operation-details').open=false;
 $('#operation-prerequisites').replaceChildren(...detail.prerequisites.flatMap(condition=>{
  const h=document.createElement('h3');h.textContent={commit:t('c43eaf707af'),publish:t('ca363b74ba5'),announce:t('c63261419fb')}[condition.operation];
  const ul=document.createElement('ul');ul.append(...condition.items.map(text=>{const li=document.createElement('li');li.textContent=text;return li;}));return [h,ul];
 }));
}
function renderWorkHelp(id){
 const detail=getNodeDetails(id),lens=getHelpLabels();
 $('#work-help').replaceChildren(...['point','line','plane'].flatMap(key=>{const dt=document.createElement('dt'),dd=document.createElement('dd');dt.textContent=lens[key];dd.textContent=detail.help[key];return [dt,dd];}));
}
const graph=getSkillGraph();
const topicMap=getTopicMap(),topicState=createTopicState(),globalTopics=getGlobalTopicGraph();
const forests=new Map(graph.groups.map(group=>[group.id,getSkillForest(group.id)]));
const overviewEdges=[...new Map([...forests.values()].flatMap(forest=>forest.connections).map(edge=>[edge.id,edge])).values()];
function openGraphSkill(id){
 const target=activeView==='classification'?classificationAdapter.reveal(id):document.querySelector(`.skill-node[data-skill="${id}"]`);
 if(activeView==='relations')revealTopic(getNodeForSkill(id));
 openNode(getNodeForSkill(id),target,id);
}
function renderSkillRelations(id){
 const {edges}=getSkillNeighborhood(id);$('#relation-count').textContent=`${edges.length}`;$('#panel-relations-button').dataset.count=String(edges.length);
 const heading=document.createElement('h3');heading.textContent=t('c50333ae4c1');
 const entries=edges.map(edge=>{
  const section=document.createElement('section');section.dataset.relation=edge.id;
  const p=document.createElement('p'),from=catalog.find(x=>x.id===edge.from),to=catalog.find(x=>x.id===edge.to);
  p.textContent=`${from.purpose} → ${to.purpose}`;if(getNodeForSkill(edge.from)!==getNodeForSkill(edge.to))section.dataset.crossTopic='true';
  const label=document.createElement('strong');label.textContent=edge.kind==='call'?`${dictionary.dual[edge.callMode]} · ${edge.label}`:edge.label;
  const note=document.createElement('p');note.textContent=edge.condition;
  const peer=edge.from===id?to:from,button=document.createElement('button');button.type='button';button.className='relation-peer';button.dataset.peer=peer.id;button.textContent=t('cb5d22c41ac',[peer.purpose]);
  button.addEventListener('click',()=>openGraphSkill(peer.id));
  const source=document.createElement('a');source.href=sourceUrl(edge.source);source.target='_blank';source.rel='noopener';source.textContent=t('ca31cbf421c');
  section.append(label,p,note,decorateSkill(button,peer.id,dictionary.provenance),source);return section;
 });
 if(!edges.length){const p=document.createElement('p');p.textContent=t('c11fbdf42ea');entries.push(p);}
 $('#skill-relations').replaceChildren(heading,...entries);
}
function highlightSkill(id){
 graphSelection=id;
 const neighborhood=id?getSkillNeighborhood(id):{edges:[],related:[]};
 for(const button of document.querySelectorAll('.skill-node')){
  button.setAttribute('aria-pressed',String(button.dataset.skill===id));button.dataset.related=String(neighborhood.related.includes(button.dataset.skill));
  const direct=button.dataset.skill===id?[]:neighborhood.edges.filter(edge=>edge.from===button.dataset.skill||edge.to===button.dataset.skill);
  button.querySelector('small').textContent=direct.length?[...new Set(direct.map(edge=>edge.kind==='call'?`${dictionary.dual[edge.callMode]} · ${edge.label}`:edge.label))].join(' / '):button.dataset.branchLabel||(Number(button.dataset.relationCount)?t('ccef6f94950',[button.dataset.coordinator==='true'?t('ce21265bf25'):'',button.dataset.relationCount]):'');
 }
 $('#map-view-note').textContent=id?t('c8aa3366c49',[catalog.find(skill=>skill.id===id).purpose,neighborhood.related.length]):t('c4fc6828042');
 drawSkillEdges(id);
}
const relationshipRenderer=createRelationshipRenderer({$,graph,topicMap,topicState,globalTopics,forests,overviewEdges,catalog,dictionary,t,getSkillNeighborhood,getNodeDetails,routeTopicRelationship,routeSkillConnection,getSupportScopes,getNodeForSkill,closePanel,openNode,showTopicRelation,showSupport,setPanelMode,highlightSkill,getGraphSelection:()=>graphSelection,getActiveView:()=>activeView,getSelectedNode:()=>selectedNode,alignClassification:id=>{classificationAdapter?.reveal(id);ensureClassificationVisible(id);}});
const {renderMap,drawSkillEdges,drawTopicEdges,syncTopics,revealTopic,ensureTopicVisible,alignLocalSkill}=relationshipRenderer;
function showTopicRelation(edge){
 explorerState.selectRelation(edge.id);panelOpener=document.querySelector(`[data-topic-relation="${edge.id}"]`);openExplanation(edge.label);
 const heading=document.createElement('h3'),body=document.createElement('p');heading.textContent=`${getNodeDetails(edge.from).title} ${edge.bidirectional?'↔':'→'} ${getNodeDetails(edge.to).title}`;body.textContent=edge.condition;
 $('#skill-relations').replaceChildren(heading,body,...edge.sources.map(source=>sourceLink(source.path)));document.querySelectorAll('.skill-group').forEach(group=>group.dataset.topicRelated=String([edge.from,edge.to].includes(group.dataset.context)));
}
function sourceLink(path){const a=document.createElement('a');a.href=sourceUrl(path);a.target='_blank';a.rel='noopener';a.textContent=path;return a;}
function openExplanation(title){
 clearDetailProvenance();
 $('.panel-navigation').hidden=true;$('#panel-placeholder').hidden=true;$('#panel-content').hidden=false;$('#detail-panel').dataset.open='true';document.body.dataset.panelOpen='true';$('#detail-panel').setAttribute('aria-labelledby','detail-title');$('#detail-title').textContent=title;$('#selected-tool').hidden=true;$('#work-explanation').hidden=true;$('.panel-copy-action').hidden=true;$('#skill-relations').hidden=false;$('#skill-relations').setAttribute('aria-label',title);$('#detail-panel').focus({preventScroll:true});
}
function showSupport(id,opener){
 explorerState.selectSupport(id);panelOpener=opener;const scope=getSupportScopes(id)[0];openExplanation(scope.label);const parts=[];
 for(const target of scope.targets){const button=document.createElement('button'),condition=document.createElement('p');button.type='button';button.dataset.supportTarget=target.topicId;button.textContent=getNodeDetails(target.topicId).title;button.addEventListener('click',()=>openNode(target.topicId,button));condition.textContent=target.condition;parts.push(button,condition,...target.sources.map(source=>sourceLink(source.path)));}
 $('#skill-relations').replaceChildren(...parts);
}

function openNode(id,opener,skillId=null){
 clearDetailProvenance();
 $('.panel-navigation').hidden=false;
 if(skillId&&activeView==='relations')revealTopic(id);
 if(skillId)explorerState.selectSkill(skillId);else explorerState.selectWork(id);
 document.querySelectorAll('.skill-group').forEach(group=>group.dataset.topicRelated='false');
 const detail=getNodeDetails(id),changed=requestState.select(id);selectedNode=id;panelOpener=opener??$('#find-tools');clearExample();
 document.querySelectorAll('[data-node]').forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.node===id)));
 $('#panel-placeholder').hidden=true;$('#panel-content').hidden=false;$('#detail-panel').dataset.open='true';document.body.dataset.panelOpen='true';$('#detail-panel').setAttribute('aria-labelledby','detail-title');
 renderWorkHelp(id);
 $('#detail-title').textContent=getMapProjection().nodes[id].title;$('#detail-summary').textContent=detail.summary;$('#detail-boundary').textContent=detail.boundary;
 renderSupportScopes(id);$('#ordinary-help').textContent=detail.usage.ordinary;$('#cortex-help').textContent=detail.usage.cortex;$('#adopted-help').textContent=detail.usage.adopted;
 $('#asset-help').replaceChildren(...detail.usage.assets.flatMap(asset=>{const term=document.createElement('dt'),a=document.createElement('a'),description=document.createElement('dd');a.textContent=asset.kind;a.href=sourceUrl(asset.href);a.target='_blank';a.rel='noopener';term.append(a);description.textContent=asset.purpose;return [term,description];}));
 $('#context-details').hidden=detail.relationships.length===0;
 if(changed)$('#context-details').open=true;
 $('#context-relations').replaceChildren(...detail.relationships.map(item=>{const section=document.createElement('div'),h=document.createElement('h3'),p=document.createElement('p');h.textContent=item.title;p.textContent=item.body;section.append(h,p);return section;}));
 const tile={direction:1,planning:1,design:2,build:3,quality:4,commit:5,release:6,research:0,foundation:7,collaboration:7}[id];
 $('#panel-picture').style.backgroundPosition=`${tile%4*100/3}% ${tile>=4?100:0}%`;$('#panel-picture').setAttribute('aria-label',t('c0d3ff8f53d',[detail.title]));
 const selection=getNodeSkillSelection(id,skillId??(changed?null:selectedSkill));
 if(skillId){renderSelectedSkill(selection.selected);setPanelMode('assets');classificationAdapter?.highlight(skillId);}else{selectedSkill=null;setPanelMode('work');}
 $('#detail-examples').hidden=detail.examples.length===0;
 $('#try-example').textContent={bug:t('cc7ecc18347'),requirements:t('c07f643c0bc'),release:t('c6354c2b9c6')}[detail.examples[0]]??'';
 $('#quality-details').hidden=id!=='quality';$('#quality-details').open=false;
 renderPrerequisites(detail);
 $('#request-context').textContent=t('cdd5bca44d5',[detail.title]);
 if(changed){$('#request-text').value=detail.prompt;$('#request-copy-feedback').textContent=t('c7799e90aa1');$('#edit-request').open=false;$('#copy-request').disabled=false;}
 $('.panel-body').scrollTop=0;$('#detail-panel').focus({preventScroll:true});drawTopicEdges();
 if(skillId){alignLocalSkill(skillId);ensureTopicVisible(id);drawSkillEdges();}
}
function closePanel(){
 clearDetailProvenance();
 const previous=explorerState.snapshot(),opener=activeOpener(previous);
 explorerState.clearSelection();classificationAdapter?.highlight(null);
 document.querySelectorAll('.skill-group').forEach(group=>group.dataset.topicRelated='false');
 selectedNode=null;selectedSkill=null;highlightSkill(null);requestState.clear();clearExample();$('#detail-panel').dataset.open='false';document.body.dataset.panelOpen='false';$('#detail-panel').setAttribute('aria-labelledby','panel-title');$('#panel-content').hidden=true;$('#panel-placeholder').hidden=false;
 document.querySelectorAll('[data-node]').forEach(button=>button.setAttribute('aria-pressed','false'));
 (opener??document.querySelector(`[data-view="${activeView}"]`)).focus({preventScroll:true});drawTopicEdges();
}
function renderGate(id){
 const state=getSimpleGate(id);document.querySelectorAll('[data-result]').forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.result===id)));
 $('#simple-gate-title').textContent=state.title;$('#simple-gate-body').textContent=state.body;
}
function renderDirectory(){
 const query=$('#tool-search').value,groups=getToolGroups(query),count=groups.reduce((sum,group)=>sum+group.skills.length,0);
 $('#tool-status').textContent=t('c0d9fb61e09',[count,catalog.length]);$('#no-tools').hidden=count>0;
 $('#tool-groups').replaceChildren(...groups.map(group=>{
  const details=document.createElement('details');details.className='tool-group';details.dataset.group=group.id;details.open=query.trim().length>0;
  const summary=document.createElement('summary'),count=document.createElement('span');summary.textContent=group.title;count.textContent=t('ce0a244d87b',[group.availability==='anytime'?t('cb85f99d2f2'):'',group.skills.length]);summary.append(count);
  const list=document.createElement('div');list.className='tool-list';
  list.append(...group.skills.map(skill=>{
   const button=document.createElement('button');button.type='button';button.className='tool-entry';button.dataset.tool=skill.id;
   const purpose=document.createElement('strong'),code=document.createElement('code');purpose.textContent=skill.purpose;code.textContent=skill.id;const name=document.createElement('span');name.className='skill-display-name';name.textContent=skill.name;if(skill.name!==skill.id)button.append(name);button.append(purpose,code);
   button.addEventListener('click',()=>{library.close();openGraphSkill(skill.id);});return decorateSkill(button,skill.id,dictionary.provenance);
  }));details.append(summary,list);return details;
 }));
}
function openLibrary(event){event?.preventDefault();renderDirectory();if(!library.open)library.showModal();explorerState.updateLookup({open:true,query:$('#tool-search').value});$('#tool-search').focus();}

$('#close-panel').addEventListener('click',closePanel);
$('#find-tools').addEventListener('click',openLibrary);
$('#close-library').addEventListener('click',()=>library.close());
library.addEventListener('keydown',event=>{if(event.key==='Escape'){event.preventDefault();event.stopPropagation();library.close();}});
$('#tool-search').addEventListener('input',()=>{explorerState.updateLookup({query:$('#tool-search').value});renderDirectory();});
library.addEventListener('close',()=>{explorerState.updateLookup({open:false});if(document.activeElement===document.body||library.contains(document.activeElement))$('#find-tools').focus();});
$('#clear-tools').addEventListener('click',()=>{$('#tool-search').value='';renderDirectory();$('#tool-search').focus();});
$('#try-example').addEventListener('click',()=>{
 if(activeExample){clearExample();return;}
 const id=getNodeDetails(selectedNode).examples[0];if(!id)return;activeExample=id;const example=getExample(id);
 document.querySelectorAll('[data-edge]').forEach(edge=>edge.classList.toggle('emphasized',example.edges.includes(edge.dataset.edge)));
 $('#try-example').setAttribute('aria-pressed','true');$('#example-title').textContent=example.title;$('#example-body').textContent=example.body;$('#example-note').hidden=false;
});
document.querySelectorAll('[data-result]').forEach(button=>button.addEventListener('click',()=>renderGate(button.dataset.result)));
$('#request-text').addEventListener('input',()=>{requestState.edit();$('#copy-request').disabled=false;$('#request-copy-feedback').textContent=t('c86736613b4');});
$('#copy-request').addEventListener('click',async()=>{
 const token=requestState.begin($('#request-text').value);if(!token)return;
 $('#copy-request').disabled=true;$('#request-copy-feedback').textContent=t('c318dfff552');
 try{
  await navigator.clipboard.writeText(token.text);
  if(requestState.finish(token)){$('#copy-request').disabled=false;$('#request-copy-feedback').textContent=t('c1d6543525d');}
 }catch{
  if(!requestState.finish(token))return;
  $('#copy-request').disabled=false;$('#edit-request').open=true;$('#request-text').focus();$('#request-text').select();
  $('#request-copy-feedback').textContent=t('c86b482c898');
 }
});
document.addEventListener('keydown',event=>{if(event.key==='Escape'&&!library.open&&$('#detail-panel').dataset.open==='true'){event.preventDefault();closePanel();}});

$('#catalog-count').textContent=t('c63d19e319a',[catalog.length]);
renderMap();
renderGate('missing');
if(location.hash==='#tools')openLibrary();



function renderSupportScopes(id){
 const section=document.querySelector('#support-scope-details')??document.createElement('section');section.id='support-scope-details';section.replaceChildren();section.hidden=true;
 for(const scope of getSupportScopes(id)){
  section.hidden=false;const h=document.createElement('h3');h.textContent=scope.label;section.append(h);
  for(const target of scope.targets){const button=document.createElement('button'),p=document.createElement('p');button.type='button';button.dataset.supportTarget=target.topicId;button.textContent=getNodeDetails(target.topicId).title;button.addEventListener('click',()=>{openNode(target.topicId,document.querySelector(`[data-node="${target.topicId}"]`));setPanelMode('work');ensureTopicVisible(target.topicId);});p.textContent=target.condition;section.append(button,p);for(const source of target.sources){const link=document.createElement('a');link.textContent=source.path;link.href=sourceUrl(source.path);link.target='_blank';link.rel='noopener';section.append(link);}}
 }
 document.querySelector('#work-explanation').prepend(section);
}

function showSkillRelation(id,opener){
 const edge=relationships.find(e=>e.id===id);if(!edge)throw Error('Unknown relationship');
 explorerState.selectRelation(id);panelOpener=opener;openExplanation(edge.label);$('.panel-navigation').hidden=true;$('#panel-placeholder').hidden=true;$('#panel-content').hidden=false;$('#detail-panel').dataset.open='true';document.body.dataset.panelOpen='true';$('#detail-title').textContent=edge.label;$('#selected-tool').hidden=true;$('#work-explanation').hidden=true;$('.panel-copy-action').hidden=true;$('#skill-relations').hidden=false;
 const title=document.createElement('h3'),condition=document.createElement('p'),source=document.createElement('a'),peer=document.createElement('button');title.textContent=`${dictionary.skills[edge.from].name} → ${dictionary.skills[edge.to].name}`;condition.textContent=edge.condition;source.href=sourceUrl(edge.source);source.textContent=edge.source;source.target='_blank';source.rel='noopener';peer.type='button';peer.dataset.peer=edge.to;peer.textContent=dictionary.skills[edge.to].name;peer.addEventListener('click',()=>openGraphSkill(edge.to));$('#skill-relations').replaceChildren(title,condition,source,decorateSkill(peer,edge.to,dictionary.provenance));$('#detail-panel').focus({preventScroll:true});
}
classificationAdapter=mountClassification(viewPorts.classification,{onSelectSkill:(id,opener)=>openNode(getNodeForSkill(id),opener,id),onSelectRelation:showSkillRelation,onSelectSupport:showSupport,onCollapse:(ids,opener)=>{if(activeView==='classification'&&ids.includes(selectedSkill)){closePanel();opener.focus();}},onViewStateChange:state=>explorerState.updateViewState('classification',state)});
relationshipAdapter=mountRelationships(viewPorts.relations,{getExpanded:()=>topicState.expanded()[0]??null,revealSkill:id=>{revealTopic(getNodeForSkill(id));alignLocalSkill(id);ensureTopicVisible(getNodeForSkill(id));return document.querySelector(`.skill-node[data-skill="${id}"]`);},revealWork:id=>{ensureTopicVisible(id);return document.querySelector(`[data-node="${id}"]`);},onRestore:saved=>{topicState.collapseAll();if(saved.expandedTopicId)topicState.reveal(saved.expandedTopicId);syncTopics();}});
function setView(view,{historyDriven=false}={}){
 if(!['classification','relations'].includes(view))throw Error('Unknown view');
 const adapters={classification:classificationAdapter,relations:relationshipAdapter};explorerState.updateViewState(activeView,adapters[activeView].capture());explorerState.setView(view);activeView=view;const ticket=++generation;
 for(const [id,port]of Object.entries(viewPorts)){port.hidden=id!==view;port.inert=id!==view;}
 for(const button of document.querySelectorAll('[data-view]'))button.setAttribute('aria-pressed',String(button.dataset.view===view));
 adapters[view].restore(explorerState.snapshot().viewState[view]);
 const state=explorerState.snapshot(),target=state.detail.open?state.detail.target:state.selectedSkillId?{kind:'skill',id:state.selectedSkillId}:null;
 requestAnimationFrame(()=>{if(ticket!==generation)return;if(target){let selection=target;if(target.kind==='relation'){const edge=relationships.find(e=>e.id===target.id)||globalTopics.edges.find(e=>e.id===target.id)||globalTopics.loops.find(e=>e.id===target.id);selection={kind:relationships.includes(edge)?'skill':'work',id:edge.from};}if(view==='classification'){if(selection.kind==='skill'){classificationAdapter.reveal(selection.id);ensureClassificationVisible(selection.id);}else for(const group of classification.groups.filter(g=>g.skillIds.some(id=>getNodeForSkill(id)===selection.id)))document.getElementById(group.id).open=true;}else relationshipAdapter.reveal(selection);}drawTopicEdges();drawSkillEdges();});
 if(!historyDriven){const url=new URL(location.href);url.searchParams.set('view',view);history.replaceState(null,'',url);window.dispatchEvent(new Event('explorerviewchange'));document.querySelector(`[data-view="${view}"]`).focus({preventScroll:true});}
}
for(const button of document.querySelectorAll('[data-view]'))button.addEventListener('click',()=>setView(button.dataset.view));
function restoreLocation(){const requested=new URL(location.href).searchParams.get('view');const view=requested==='relations'?'relations':'classification';$('#view-notice').textContent=requested&&!['classification','relations'].includes(requested)?dictionary.dual.invalidView:'';setView(view,{historyDriven:true});const category=classification.groups.find(g=>'#'+g.id===location.hash);if(category&&view==='classification')document.getElementById(category.id).open=true;else if(category)$('#view-notice').textContent=`${dictionary.classification[category.id].name} · ${dictionary.dual.categoryContext}`;}
window.addEventListener('popstate',restoreLocation);window.addEventListener('hashchange',restoreLocation);restoreLocation();

function ensureClassificationVisible(id){
 const button=classificationAdapter?.find(id);if(!button||!button.checkVisibility())return;const card=button.closest('.classification-card'),r=button.getBoundingClientRect(),c=card.getBoundingClientRect(),limit=innerWidth<1200&&$('#detail-panel').dataset.open==='true'?$('#detail-panel').getBoundingClientRect().top-10:innerHeight-12;
 if(c.top<56||r.bottom>limit)window.scrollBy({top:c.top-56,behavior:'instant'});
}

function activeOpener(state){
 if(panelOpener?.isConnected&&panelOpener.checkVisibility())return panelOpener;
 const target=state.detail.target;let id=state.selectedSkillId;
 if(target?.kind==='relation'){const edge=relationships.find(e=>e.id===target.id);if(edge)id=edge.from;}
 if(target?.kind==='support')return document.querySelector(activeView==='classification'?`[data-class-support="${target.id}"]`:`[data-support-scope="${target.id}"]`);
 if(id){const button=activeView==='classification'?classificationAdapter.find(id):document.querySelector(`.skill-node[data-skill="${id}"]`);if(button?.checkVisibility())return button;}
 return document.querySelector(`[data-view="${activeView}"]`);
}

$("#capabilities").dataset.ready="true";

}
