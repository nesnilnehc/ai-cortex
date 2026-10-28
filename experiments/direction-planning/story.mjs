import {getGlobalTopicGraph,routeTopicRelationship} from './global-topic-graph.mjs?v=topic-local-branches';
import {getTopicMap,createTopicState} from './topic-map.mjs?v=topic-local-branches';
import {getSkillGraph,getSkillNeighborhood,getSkillForest,routeSkillConnection} from './skill-graph.mjs?v=topic-local-branches';
import {getHelpLabels,getMapProjection} from './work-map.mjs?v=single-map';
import {createRequestState} from './request-state.mjs';
import {initializeTheme} from '../../website/theme.mjs';
import {catalog} from './workflow.mjs?v=topic-local-branches';
import {getSkillGuidance} from './skill-guidance.mjs';
import {getSimpleGate,getToolGroups} from './story-model.mjs?v=topic-local-branches';
import {relations,getExample} from './relations.mjs?v=topic-local-branches';
import {getNodeDetails,getNodeForSkill,getNodeSkillSelection} from './panel-model.mjs?v=topic-local-branches';
const $=selector=>document.querySelector(selector);
const library=$('#tools');
const requestState=createRequestState();
let selectedNode=null;
let panelOpener=$('#find-tools');
let activeExample=null;
let selectedSkill=null;
let graphSelection=null;
initializeTheme(window,document.documentElement,$('#theme'));
function usageFields(id){
 const guide=getSkillGuidance(id),dl=document.createElement('dl');dl.className='skill-usage-fields';
 for(const [key,label] of [['when','什么时候用'],['provide','需要提供什么'],['use','怎么使用'],['result','预期结果']]){
  const dt=document.createElement('dt'),dd=document.createElement('dd');dt.textContent=label;dd.textContent=guide[key];dl.append(dt,dd);
 }
 return dl;
}
function usageAccess(id){
 const p=document.createElement('p');p.className='skill-access';
 if(getSkillGuidance(id).entry==='internal'){p.textContent='这是产品机会分析中的内部评估步骤。请从 product-opportunity-analysis 提出需求，由 Agent 协调使用；本页不运行技能。';return p;}
 p.append('在已接入 AI Cortex 的 Agent 中提出下面的请求。未识别技能时，让它读取本地 ');
 const code=document.createElement('code');code.textContent=`skills/${id}/SKILL.md`;p.append(code,'。尚未接入时，可先看');
 const setup=document.createElement('a');setup.href='../../README.md';setup.target='_blank';setup.rel='noopener';setup.textContent='安装说明';p.append(setup,'。本页只作说明，不运行技能。');return p;
}
function setPanelMode(mode,reveal=false){
 document.body.dataset.panelMode=mode;
 if(reveal&&selectedSkill){revealTopic(getNodeForSkill(selectedSkill));alignLocalSkill(selectedSkill);ensureTopicVisible(getNodeForSkill(selectedSkill));}
 const showAssets=mode==='assets';
 if(mode!=='work'&&selectedSkill&&graphSelection!==selectedSkill)highlightSkill(selectedSkill);
 $('#selected-tool').hidden=!showAssets;$('#skill-relations').hidden=mode!=='relations';$('#work-explanation').hidden=mode!=='work';$('.panel-copy-action').hidden=mode!=='work';
 $('#panel-assets-button').setAttribute('aria-pressed',String(showAssets));$('#panel-work-button').setAttribute('aria-pressed',String(mode==='work'));$('#panel-relations-button').setAttribute('aria-pressed',String(mode==='relations'));
 $('.panel-body').scrollTop=0;
 const selectedButton=selectedSkill&&document.querySelector(`.skill-node[data-skill="${selectedSkill}"]`);
 if(selectedButton?.checkVisibility()){alignLocalSkill(selectedSkill);ensureTopicVisible(getNodeForSkill(selectedSkill));drawSkillEdges();}
}
function renderSelectedSkill(skill){
 selectedSkill=skill.id;highlightSkill(skill.id);renderSkillRelations(skill.id);
 $('#selected-tool-purpose').textContent=skill.purpose;$('#selected-tool-guide').replaceChildren(usageFields(skill.id),usageAccess(skill.id));
 $('#selected-tool-link').textContent=`查看 ${skill.id} 原文（英文，可选）`;$('#selected-tool-link').href=`../../skills/${skill.id}/SKILL.md`;
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
  const h=document.createElement('h3');h.textContent={commit:'保存提交前',publish:'发布前',announce:'公告前'}[condition.operation];
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
const kindLabels={call:'按需调用',method:'复用方法',input:'成果作依据',suggest:'只作推荐'};
function openGraphSkill(id){
 revealTopic(getNodeForSkill(id));
 const target=document.querySelector(`.skill-node[data-skill="${id}"]`);
 openNode(getNodeForSkill(id),target,id);
}
function renderSkillRelations(id){
 const {edges}=getSkillNeighborhood(id);$('#relation-count').textContent=`${edges.length}`;$('#panel-relations-button').dataset.count=String(edges.length);
 const heading=document.createElement('h3');heading.textContent='和哪些技能配合？';
 const entries=edges.map(edge=>{
  const section=document.createElement('section');section.dataset.relation=edge.id;
  const p=document.createElement('p'),from=catalog.find(x=>x.id===edge.from),to=catalog.find(x=>x.id===edge.to);
  p.textContent=`${from.purpose} → ${to.purpose}`;if(getNodeForSkill(edge.from)!==getNodeForSkill(edge.to))section.dataset.crossTopic='true';
  const label=document.createElement('strong');label.textContent=edge.label;
  const note=document.createElement('p');note.textContent=edge.condition;
  const peer=edge.from===id?to:from,button=document.createElement('button');button.type='button';button.className='relation-peer';button.dataset.peer=peer.id;button.textContent=`查看：${peer.purpose}`;
  button.addEventListener('click',()=>openGraphSkill(peer.id));
  const source=document.createElement('a');source.href=edge.source;source.target='_blank';source.rel='noopener';source.textContent='关系依据（原文）';
  section.append(label,p,note,button,source);return section;
 });
 if(!edges.length){const p=document.createElement('p');p.textContent='本图未标出它与其他技能的直接调用或输入关系。同属一类，不代表必须按顺序使用。';entries.push(p);}
 $('#skill-relations').replaceChildren(heading,...entries);
}
function highlightSkill(id){
 graphSelection=id;
 const neighborhood=id?getSkillNeighborhood(id):{edges:[],related:[]};
 for(const button of document.querySelectorAll('.skill-node')){
  button.setAttribute('aria-pressed',String(button.dataset.skill===id));button.dataset.related=String(neighborhood.related.includes(button.dataset.skill));
  const direct=button.dataset.skill===id?[]:neighborhood.edges.filter(edge=>edge.from===button.dataset.skill||edge.to===button.dataset.skill);
  button.querySelector('small').textContent=direct.length?[...new Set(direct.map(edge=>edge.label))].join(' / '):button.dataset.branchLabel||(Number(button.dataset.relationCount)?`${button.dataset.coordinator==='true'?'协调 · ':''}${button.dataset.relationCount} 项关联`:'');
 }
 $('#map-view-note').textContent=id?`${catalog.find(skill=>skill.id===id).purpose}：${neighborhood.related.length} 项直接关联。连线只表示标注的关系，不会执行技能。`:'技能在所属主题内展开；技能多时只滚动该主题的列表。';
 drawSkillEdges(id);
}
function drawSkillEdges(id=graphSelection){
 const candidates=id?getSkillNeighborhood(id).edges:overviewEdges;
 for(const group of graph.groups){
  const branch=document.querySelector(`[data-branch="${group.id}"]`);if(!branch)continue;
  const content=branch.querySelector('.local-skill-content'),svg=branch.querySelector('.local-skill-connections'),paths=branch.querySelector('.local-skill-paths');
  if(branch.hidden){paths.replaceChildren();continue;}
  const box=content.getBoundingClientRect(),buttons=[...content.querySelectorAll('.skill-node')],obstacles=buttons.map(node=>node.getBoundingClientRect()),members=new Set(buttons.map(node=>node.dataset.skill));
  svg.setAttribute('viewBox',`0 0 ${box.width} ${box.height}`);
  paths.replaceChildren(...candidates.filter(edge=>members.has(edge.from)&&members.has(edge.to)).map(edge=>{
   const from=content.querySelector(`[data-skill="${edge.from}"]`).getBoundingClientRect(),to=content.querySelector(`[data-skill="${edge.to}"]`).getBoundingClientRect(),points=routeSkillConnection(from,to,box,'call',obstacles);
   const path=document.createElementNS('http://www.w3.org/2000/svg','path');path.dataset.skillEdge=edge.id;path.dataset.kind=edge.kind;path.setAttribute('d',points.map((point,index)=>`${index?'L':'M'}${point.join(',')}`).join(' '));path.setAttribute('marker-end',`url(#local-arrow-${group.id})`);return path;
  }));
 }
}
function ensureTopicVisible(id){
 const section=document.querySelector(`.skill-group[data-context="${id}"]`),viewport=$('.relations-canvas'),v=viewport.getBoundingClientRect();let rect=section.getBoundingClientRect();if(rect.left<v.left+8)viewport.scrollLeft+=rect.left-v.left-8;else if(rect.right>v.right-8)viewport.scrollLeft+=rect.right-v.right+8;rect=section.getBoundingClientRect();
 const limit=matchMedia('(max-width:1199px)').matches&&$('#detail-panel').dataset.open==='true'?$('#detail-panel').getBoundingClientRect().top-10:innerHeight-12;
 const delta=rect.top<12?rect.top-12:rect.bottom>limit?Math.min(rect.bottom-limit,rect.top-12):0;
 if(delta)window.scrollBy({top:delta,behavior:'instant'});
}
function alignLocalSkill(id){
 const button=document.querySelector(`.skill-node[data-skill="${id}"]`),port=button.closest('.local-skill-scroll'),r=button.getBoundingClientRect(),p=port.getBoundingClientRect();
 port.scrollTop+=r.top-p.top-(p.height-r.height)/2;
}
function renderMap(){
 const groups=graph.groups.map(group=>{
  const section=document.createElement('section');section.className='skill-group';section.dataset.context=group.id;
  const heading=document.createElement('button');heading.type='button';heading.dataset.node=group.id;heading.className='skill-group-heading';heading.setAttribute('aria-controls','detail-panel');
  const title=document.createElement('strong'),count=document.createElement('span');title.textContent=group.title;count.textContent=`${group.availability==='anytime'?'按需支持 · ':''}${group.skills.length} 项`;heading.append(title,count);heading.addEventListener('click',()=>{openNode(group.id,heading);setPanelMode('work');highlightSkill(null);});
  const list=document.createElement('div');list.className='skill-node-list';list.id=`skills-${group.id}`;list.hidden=true;
  const toggle=document.createElement('button');toggle.type='button';toggle.className='topic-toggle';toggle.dataset.toggle=group.id;toggle.setAttribute('aria-expanded','false');toggle.setAttribute('aria-controls',list.id);toggle.textContent=`展开 ${group.skills.length} 项技能`;
  toggle.addEventListener('click',()=>{topicState.toggle(group.id);if(selectedNode&&(!topicState.expanded().includes(group.id)||selectedNode!==group.id)){closePanel();toggle.focus();}syncTopics();if(topicState.expanded().includes(group.id))ensureTopicVisible(group.id);});
  const summary=document.createElement('p');summary.className='topic-summary';summary.textContent=group.summary;

  function createTree(node){
   const tree=document.createElement('div');tree.className='skill-tree';tree.dataset.root=String(!node.via);
   const skill=node.skill,button=document.createElement('button');button.type='button';button.className='skill-node';button.dataset.skill=skill.id;button.dataset.branchLabel=node.via?.label??'';button.dataset.coordinator=String(node.coordinator);button.setAttribute('aria-pressed','false');button.setAttribute('aria-controls','detail-panel');
   const purpose=document.createElement('strong'),code=document.createElement('code'),badge=document.createElement('small');purpose.textContent=skill.purpose;code.textContent=skill.id;
   const count=getSkillNeighborhood(skill.id).related.length;button.dataset.relationCount=String(count);button.title=skill.id;badge.textContent=node.via?.label||(count?`${node.coordinator?'协调 · ':''}${count} 项关联`:'');button.append(code,purpose,badge);
   button.addEventListener('click',()=>openNode(group.id,button,skill.id));tree.append(button);
   if(node.children.length){const children=document.createElement('div');children.className='skill-children';children.append(...[...node.children].sort((a,b)=>Number(Boolean(a.children.length))-Number(Boolean(b.children.length))).map(createTree));tree.append(children);}return tree;
  }
  const forest=forests.get(group.id),branched=forest.roots.filter(node=>node.children.length),standalone=forest.roots.filter(node=>!node.children.length);
  list.append(...branched.map(createTree));
  if(standalone.length){const peers=document.createElement('div');peers.className='standalone-roots';peers.append(...standalone.map(createTree));list.append(peers);}
  const note=document.createElement('p');note.className='skill-group-note';note.textContent=group.note;note.hidden=!group.note;const loop=topicMap.loops.find(loop=>loop.from===group.id);
  section.append(heading,summary,toggle);if(loop){const button=document.createElement('button');button.type='button';button.className='topic-loop';button.dataset.topicRelation=loop.id;button.textContent=`↶ ${loop.label}`;button.addEventListener('click',()=>showTopicRelation(loop));section.append(button);}section.append(note,list);return section;
 });
 const board=document.createElement('div');board.className='global-topic-board';board.setAttribute('aria-label','完整主题关系图');
 const svg=document.createElementNS('http://www.w3.org/2000/svg','svg');svg.id='topic-connections';svg.setAttribute('aria-hidden','true');svg.innerHTML='<defs><marker id="topic-support-arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto-start-reverse"><path d="M0,0 L7,3.5 L0,7" fill="var(--support-color)"/></marker><marker id="topic-arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto-start-reverse"><path d="M0,0 L7,3.5 L0,7" fill="currentColor"/></marker></defs><g id="topic-edge-paths"></g>';board.append(svg);
 for(const node of globalTopics.nodes){
  const section=groups.find(group=>group.dataset.context===node.id);section.style.setProperty('--topic-row',node.row);section.style.setProperty('--topic-column',node.column);
  const list=section.querySelector('.skill-node-list');const branch=document.createElement('section');branch.className='expanded-skill-branch';branch.dataset.branch=node.id;branch.hidden=true;
  const title=document.createElement('h3');title.textContent=`${getNodeDetails(node.id).title}的技能`;
  const port=document.createElement('div');port.className='local-skill-scroll';port.setAttribute('aria-label',`${getNodeDetails(node.id).title}的技能列表`);port.tabIndex=0;
  const content=document.createElement('div');content.className='local-skill-content';
  const lines=document.createElementNS('http://www.w3.org/2000/svg','svg');lines.classList.add('local-skill-connections');lines.setAttribute('aria-hidden','true');lines.innerHTML=`<defs><marker id="local-arrow-${node.id}" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7" fill="currentColor"/></marker></defs><g class="local-skill-paths"></g>`;
  content.append(lines,list);port.append(content);branch.append(title,port);section.append(branch);
  const hint=document.createElement('p');hint.className='topic-purpose';hint.textContent=node.hint;section.insertBefore(hint,section.querySelector('.topic-toggle'));
  section.querySelector('.topic-summary').hidden=true;section.querySelector('.skill-group-note').hidden=true;board.append(section);
 }
 const labels=globalTopics.edges.map(edge=>{const button=document.createElement('button');button.type='button';button.className='global-topic-edge-label';button.dataset.topicRelation=edge.id;button.dataset.kind=edge.kind;button.textContent=edge.label;button.setAttribute('aria-label',`${getNodeDetails(edge.from).title} ${edge.bidirectional?'↔':'→'} ${getNodeDetails(edge.to).title}：${edge.label}，查看条件与依据`);button.addEventListener('click',()=>showTopicRelation(edge));board.append(button);return button;});
 const controls=document.createElement('div');controls.className='map-disclosure-controls';const collapse=document.createElement('button');collapse.type='button';collapse.id='collapse-topics';collapse.textContent='收起所有技能';collapse.addEventListener('click',()=>{topicState.collapseAll();closePanel();syncTopics();collapse.focus();});controls.append(collapse);
 $('#skill-groups').replaceChildren(controls,board);syncTopics();
 $('.map-key').replaceChildren(...['橙色虚线：使用已有成果','橙色实线：条件调用或问题返回','绿色虚线：按需支持；双向箭头：往返交接'].map(text=>{const span=document.createElement('span');span.textContent=text;return span;}));
 $('#relation-text').replaceChildren(...[...globalTopics.edges,...globalTopics.loops].map(edge=>{const li=document.createElement('li');li.textContent=`${getNodeDetails(edge.from).title} ${edge.bidirectional?'↔':'→'} ${getNodeDetails(edge.to).title}：${edge.condition}`;return li;}));
 $('#panel-preview').textContent='点主题之间的关系查看条件；展开主题，再点技能看中文用法。';highlightSkill(null);
 new ResizeObserver(()=>{drawSkillEdges();drawTopicEdges();}).observe($('#skill-groups'));drawTopicEdges();
}
function drawTopicEdges(){
 const board=$('.global-topic-board');if(!board)return;
 const origin=board.getBoundingClientRect(),mobile=matchMedia('(max-width:767px)').matches;
 const nodes=new Map(globalTopics.nodes.map(node=>[node.id,document.querySelector(`.skill-group[data-context="${node.id}"]`).getBoundingClientRect()]));
 $('#topic-connections').setAttribute('viewBox',`0 0 ${origin.width} ${origin.height}`);
 $('#topic-edge-paths').replaceChildren(...globalTopics.edges.map(edge=>{
  const route=routeTopicRelationship(edge,nodes,origin,mobile),path=document.createElementNS('http://www.w3.org/2000/svg','path');path.dataset.topicEdge=edge.id;path.dataset.kind=edge.kind;
  path.setAttribute('d',route.points.map((point,index)=>`${index?'L':'M'}${point.join(',')}`).join(' '));path.setAttribute('marker-end',edge.kind==='support'?'url(#topic-support-arrow)':'url(#topic-arrow)');
  if(edge.bidirectional)path.setAttribute('marker-start',edge.kind==='support'?'url(#topic-support-arrow)':'url(#topic-arrow)');
  const label=document.querySelector(`.global-topic-edge-label[data-topic-relation="${edge.id}"]`);label.style.left=`${route.label[0]}px`;label.style.top=`${route.label[1]}px`;label.style.width=`${route.maxWidth}px`;label.style.maxWidth=`${route.maxWidth}px`;
  return path;
 }));
}
function syncTopics(){
 const active=globalTopics.nodes.find(node=>topicState.expanded().includes(node.id));for(let column=1;column<=4;column++)$('.global-topic-board').style.setProperty(`--topic-col-${column}`,active?.column===column?'2fr':'1fr');
 for(const group of graph.groups){const open=topicState.expanded().includes(group.id),section=document.querySelector(`.skill-group[data-context="${group.id}"]`);section.dataset.expanded=String(open);document.getElementById(`skills-${group.id}`).hidden=!open;document.querySelector(`[data-branch="${group.id}"]`).hidden=!open;const button=section.querySelector('.topic-toggle');button.setAttribute('aria-expanded',String(open));button.textContent=`${open?'收起':'展开'} ${group.skills.length} 项技能`;}
 drawSkillEdges();drawTopicEdges();
}
function revealTopic(id){topicState.reveal(id);syncTopics();}
function showTopicRelation(edge){
 openNode(edge.from,document.querySelector(`[data-topic-relation="${edge.id}"]`));highlightSkill(null);
 $('.panel-navigation').hidden=true;$('#detail-title').textContent=edge.label;$('#selected-tool').hidden=true;$('#work-explanation').hidden=true;$('.panel-copy-action').hidden=true;$('#skill-relations').hidden=false;
 const heading=document.createElement('h3'),body=document.createElement('p');heading.textContent=edge.from===edge.to?'这个主题里的反馈循环':`${getNodeDetails(edge.from).title} ${edge.bidirectional?'↔':'→'} ${getNodeDetails(edge.to).title}`;body.textContent=edge.condition;
 const sources=edge.sources.map(source=>{const a=document.createElement('a');a.href=source.path;a.target='_blank';a.rel='noopener';a.textContent='查看定义依据（英文）';return a;});
 $('#skill-relations').replaceChildren(heading,body,...sources);
 document.querySelectorAll('.skill-group').forEach(group=>group.dataset.topicRelated=String([edge.from,edge.to].includes(group.dataset.context)));
 $('#panel-relations-button').setAttribute('aria-pressed','true');$('#panel-assets-button').setAttribute('aria-pressed','false');$('#panel-work-button').setAttribute('aria-pressed','false');
}
function openNode(id,opener,skillId=null){
 $('.panel-navigation').hidden=false;
 if(skillId)revealTopic(id);
 document.querySelectorAll('.skill-group').forEach(group=>group.dataset.topicRelated='false');
 const detail=getNodeDetails(id),changed=requestState.select(id);selectedNode=id;panelOpener=opener??$('#find-tools');clearExample();
 document.querySelectorAll('[data-node]').forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.node===id)));
 $('#panel-placeholder').hidden=true;$('#panel-content').hidden=false;$('#detail-panel').dataset.open='true';document.body.dataset.panelOpen='true';$('#detail-panel').setAttribute('aria-labelledby','detail-title');
 renderWorkHelp(id);
 $('#detail-title').textContent=getMapProjection().nodes[id].title;$('#detail-summary').textContent=detail.summary;$('#detail-boundary').textContent=detail.boundary;
 $('#ordinary-help').textContent=detail.usage.ordinary;$('#cortex-help').textContent=detail.usage.cortex;$('#adopted-help').textContent=detail.usage.adopted;
 $('#asset-help').replaceChildren(...detail.usage.assets.flatMap(asset=>{const term=document.createElement('dt'),a=document.createElement('a'),description=document.createElement('dd');a.textContent=asset.kind;a.href=asset.href;a.target='_blank';a.rel='noopener';term.append(a);description.textContent=asset.purpose;return [term,description];}));
 $('#context-details').hidden=detail.relationships.length===0;
 if(changed)$('#context-details').open=true;
 $('#context-relations').replaceChildren(...detail.relationships.map(item=>{const section=document.createElement('div'),h=document.createElement('h3'),p=document.createElement('p');h.textContent=item.title;p.textContent=item.body;section.append(h,p);return section;}));
 const tile={direction:1,planning:1,design:2,build:3,quality:4,commit:5,release:6,research:0,foundation:7,collaboration:7}[id];
 $('#panel-picture').style.backgroundPosition=`${tile%4*100/3}% ${tile>=4?100:0}%`;$('#panel-picture').setAttribute('aria-label',`${detail.title}的说明插画`);
 const selection=getNodeSkillSelection(id,skillId??(changed?null:selectedSkill));
 renderSelectedSkill(selection.selected);setPanelMode('assets');
 $('#detail-examples').hidden=detail.examples.length===0;
 $('#try-example').textContent={bug:'看看发现代码问题时',requirements:'看看需求说不清时',release:'看看准备发布时'}[detail.examples[0]]??'';
 $('#quality-details').hidden=id!=='quality';$('#quality-details').open=false;
 renderPrerequisites(detail);
 $('#request-context').textContent=`用于：${detail.title}`;
 if(changed){$('#request-text').value=detail.prompt;$('#copy-feedback').textContent='已切换工作，默认请求已更新。可编辑后复制。';$('#edit-request').open=false;$('#copy-request').disabled=false;}
 $('.panel-body').scrollTop=0;$('#detail-panel').focus({preventScroll:true});drawTopicEdges();
 if(skillId){alignLocalSkill(skillId);ensureTopicVisible(id);drawSkillEdges();}
}
function closePanel(){
 document.querySelectorAll('.skill-group').forEach(group=>group.dataset.topicRelated='false');
 selectedNode=null;selectedSkill=null;highlightSkill(null);requestState.clear();clearExample();$('#detail-panel').dataset.open='false';document.body.dataset.panelOpen='false';$('#detail-panel').setAttribute('aria-labelledby','panel-title');$('#panel-content').hidden=true;$('#panel-placeholder').hidden=false;
 document.querySelectorAll('[data-node]').forEach(button=>button.setAttribute('aria-pressed','false'));
 if(panelOpener?.isConnected)panelOpener.focus({preventScroll:true});drawTopicEdges();
}
function renderGate(id){
 const state=getSimpleGate(id);document.querySelectorAll('[data-result]').forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.result===id)));
 $('#simple-gate-title').textContent=state.title;$('#simple-gate-body').textContent=state.body;
}
function renderDirectory(){
 const query=$('#tool-search').value,groups=getToolGroups(query),count=groups.reduce((sum,group)=>sum+group.skills.length,0);
 $('#tool-status').textContent=`找到 ${count} 项，共 ${catalog.length} 项技能。`;$('#no-tools').hidden=count>0;
 $('#tool-groups').replaceChildren(...groups.map(group=>{
  const details=document.createElement('details');details.className='tool-group';details.dataset.group=group.id;details.open=query.trim().length>0;
  const summary=document.createElement('summary'),count=document.createElement('span');summary.textContent=group.title;count.textContent=`${group.availability==='anytime'?'按需支持 · ':''}${group.skills.length} 项`;summary.append(count);
  const list=document.createElement('div');list.className='tool-list';
  list.append(...group.skills.map(skill=>{
   const button=document.createElement('button');button.type='button';button.className='tool-entry';button.dataset.tool=skill.id;
   const purpose=document.createElement('strong'),code=document.createElement('code');purpose.textContent=skill.purpose;code.textContent=skill.id;button.append(purpose,code);
   button.addEventListener('click',()=>{library.close();openGraphSkill(skill.id);});return button;
  }));details.append(summary,list);return details;
 }));
}
function openLibrary(event){event?.preventDefault();renderDirectory();if(!library.open)library.showModal();$('#tool-search').focus();}

$('#close-panel').addEventListener('click',closePanel);
$('#find-tools').addEventListener('click',openLibrary);
$('#close-library').addEventListener('click',()=>library.close());
library.addEventListener('keydown',event=>{if(event.key==='Escape'){event.preventDefault();event.stopPropagation();library.close();}});
$('#tool-search').addEventListener('input',renderDirectory);
$('#clear-tools').addEventListener('click',()=>{$('#tool-search').value='';renderDirectory();$('#tool-search').focus();});
$('#try-example').addEventListener('click',()=>{
 if(activeExample){clearExample();return;}
 const id=getNodeDetails(selectedNode).examples[0];if(!id)return;activeExample=id;const example=getExample(id);
 document.querySelectorAll('[data-edge]').forEach(edge=>edge.classList.toggle('emphasized',example.edges.includes(edge.dataset.edge)));
 $('#try-example').setAttribute('aria-pressed','true');$('#example-title').textContent=example.title;$('#example-body').textContent=example.body;$('#example-note').hidden=false;
});
document.querySelectorAll('[data-result]').forEach(button=>button.addEventListener('click',()=>renderGate(button.dataset.result)));
$('#request-text').addEventListener('input',()=>{requestState.edit();$('#copy-request').disabled=false;$('#copy-feedback').textContent='请求已修改，可复制当前文字。';});
$('#copy-request').addEventListener('click',async()=>{
 const token=requestState.begin($('#request-text').value);if(!token)return;
 $('#copy-request').disabled=true;$('#copy-feedback').textContent='正在复制这段请求…';
 try{
  await navigator.clipboard.writeText(token.text);
  if(requestState.finish(token)){$('#copy-request').disabled=false;$('#copy-feedback').textContent='已复制，可以粘贴到你的智能体。';}
 }catch{
  if(!requestState.finish(token))return;
  $('#copy-request').disabled=false;$('#edit-request').open=true;$('#request-text').focus();$('#request-text').select();
  $('#copy-feedback').textContent='这段工作请求未能自动复制。请按 ⌘C 或 Ctrl+C 复制已选中的文字，或重试。';
 }
});
document.addEventListener('keydown',event=>{if(event.key==='Escape'&&!library.open&&selectedNode){event.preventDefault();closePanel();}});

$('#catalog-count').textContent=`全部 ${catalog.length} 项。找到后，回到图旁查看。`;
renderMap();
renderGate('missing');
if(location.hash==='#tools')openLibrary();
