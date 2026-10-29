import {decorateSkill} from './provenance.mjs?v=aic08-provenance-3';
// DOM adapter: graph rendering/routing remains native and is wired by the shared host.
export function mountRelationships(container,{getExpanded,revealSkill,revealWork,onRestore}){
 return {capture(){return {expandedTopicId:getExpanded(),scrollByRegion:Object.fromEntries([...container.querySelectorAll('[data-context]')].map(n=>[n.dataset.context,n.querySelector('.local-skill-scroll')?.scrollTop??0])),pan:{x:container.querySelector('.relations-canvas').scrollLeft,y:container.scrollTop}};},restore(saved){onRestore(saved);container.querySelector('.relations-canvas').scrollLeft=saved.pan.x;container.scrollTop=saved.pan.y;for(const n of container.querySelectorAll('[data-context]')){const port=n.querySelector('.local-skill-scroll');if(port)port.scrollTop=saved.scrollByRegion[n.dataset.context]??0;}},reveal(target){if(target.kind==='skill')return revealSkill(target.id);if(target.kind==='work'||target.kind==='support')return revealWork(target.id);}};
}

export function createRelationshipRenderer(context){
 const {$,graph,topicMap,topicState,globalTopics,forests,overviewEdges,catalog,dictionary,t,getSkillNeighborhood,getNodeDetails,routeTopicRelationship,routeSkillConnection,getSupportScopes,getNodeForSkill,closePanel,openNode,showTopicRelation,showSupport,setPanelMode,highlightSkill,getGraphSelection,getActiveView,getSelectedNode,alignClassification}=context;
function drawSkillEdges(id=getGraphSelection()){
 if(getActiveView()!=="relations")return;
 const candidates=id?getSkillNeighborhood(id).edges:overviewEdges;
 for(const group of graph.groups){
  const branch=document.querySelector(`[data-branch="${group.id}"]`);if(!branch)continue;
  const content=branch.querySelector('.local-skill-content'),svg=branch.querySelector('.local-skill-connections'),paths=branch.querySelector('.local-skill-paths');
  if(branch.hidden){paths.replaceChildren();continue;}
  const box=content.getBoundingClientRect(),buttons=[...content.querySelectorAll('.skill-node')],obstacles=buttons.map(node=>node.getBoundingClientRect()),members=new Set(buttons.map(node=>node.dataset.skill));
  svg.setAttribute('viewBox',`0 0 ${box.width} ${box.height}`);
  paths.replaceChildren(...candidates.filter(edge=>members.has(edge.from)&&members.has(edge.to)).map(edge=>{
   const from=content.querySelector(`[data-skill="${edge.from}"]`).getBoundingClientRect(),to=content.querySelector(`[data-skill="${edge.to}"]`).getBoundingClientRect(),points=routeSkillConnection(from,to,box,edge.kind,obstacles);
   const path=document.createElementNS('http://www.w3.org/2000/svg','path');path.dataset.skillEdge=edge.id;path.dataset.kind=edge.kind;path.setAttribute('d',points.map((point,index)=>`${index?'L':'M'}${point.join(',')}`).join(' '));path.setAttribute('marker-end',`url(#local-arrow-${group.id})`);return path;
  }));
 }
}
function ensureTopicVisible(id){
 if(getActiveView()!=="relations")return;
 const section=document.querySelector(`.skill-group[data-context="${id}"]`),viewport=$('.relations-canvas'),v=viewport.getBoundingClientRect();let rect=section.getBoundingClientRect();if(rect.left<v.left+8)viewport.scrollLeft+=rect.left-v.left-8;else if(rect.right>v.right-8)viewport.scrollLeft+=rect.right-v.right+8;rect=section.getBoundingClientRect();
 const limit=matchMedia('(max-width:1199px)').matches&&$('#detail-panel').dataset.open==='true'?$('#detail-panel').getBoundingClientRect().top-10:innerHeight-12;
 const port=section.querySelector('.local-skill-scroll'),selected=section.querySelector('.skill-node[aria-pressed=true]');
 if(port&&selected&&$('#detail-panel').dataset.open==='true'&&innerWidth<1200){const header=port.getBoundingClientRect().top-rect.top;port.style.maxHeight=`${Math.max(selected.getBoundingClientRect().height+2,Math.min(innerWidth<768?170:220,limit-24-header))}px`;alignLocalSkill(selected.dataset.skill);rect=section.getBoundingClientRect();}
 const delta=rect.top<12?rect.top-12:rect.bottom>limit?Math.min(rect.bottom-limit,rect.top-12):0;
 if(delta)window.scrollBy({top:delta,behavior:'instant'});
}
function alignLocalSkill(id){
 if(getActiveView()!=="relations"){alignClassification(id);return;}
 const button=document.querySelector(`.skill-node[data-skill="${id}"]`),port=button.closest('.local-skill-scroll'),r=button.getBoundingClientRect(),p=port.getBoundingClientRect();
 if(r.top<p.top||r.bottom>p.bottom)port.scrollTop+=r.top-p.top-(p.height-r.height)/2;
}
function renderMap(){
 const groups=graph.groups.map(group=>{
  const section=document.createElement('section');section.className='skill-group';section.dataset.context=group.id;
  const heading=document.createElement('button');heading.type='button';heading.dataset.node=group.id;heading.className='skill-group-heading';heading.setAttribute('aria-controls','detail-panel');
  const title=document.createElement('strong'),count=document.createElement('span');title.textContent=group.title;count.textContent=t('ce0a244d87b',[group.availability==='anytime'?t('cb85f99d2f2'):'',group.skills.length]);heading.append(title,count);heading.addEventListener('click',()=>{openNode(group.id,heading);setPanelMode('work');highlightSkill(null);});
  const list=document.createElement('div');list.className='skill-node-list';list.id=`skills-${group.id}`;list.hidden=true;
  const toggle=document.createElement('button');toggle.type='button';toggle.className='topic-toggle';toggle.dataset.toggle=group.id;toggle.setAttribute('aria-expanded','false');toggle.setAttribute('aria-controls',list.id);toggle.textContent=t('c13611c1d54',[group.skills.length]);
  toggle.addEventListener('click',()=>{topicState.toggle(group.id);if(getSelectedNode()&&(!topicState.expanded().includes(group.id)||getSelectedNode()!==group.id)){closePanel();toggle.focus();}syncTopics();if(topicState.expanded().includes(group.id))ensureTopicVisible(group.id);});
  const summary=document.createElement('p');summary.className='topic-summary';summary.textContent=group.summary;

  function createTree(node){
   const tree=document.createElement('div');tree.className='skill-tree';tree.dataset.root=String(!node.via);
   const skill=node.skill,button=document.createElement('button');button.type='button';button.className='skill-node';button.dataset.skill=skill.id;button.dataset.branchLabel=node.via?`${dictionary.dual[node.via.callMode]} · ${node.via.label}`:'';button.dataset.coordinator=String(node.coordinator);button.setAttribute('aria-pressed','false');button.setAttribute('aria-controls','detail-panel');
   const purpose=document.createElement('strong'),code=document.createElement('code'),badge=document.createElement('small');purpose.textContent=skill.purpose;code.textContent=skill.id;
   const count=getSkillNeighborhood(skill.id).related.length;button.dataset.relationCount=String(count);button.title=skill.id;badge.textContent=button.dataset.branchLabel||(count?t('ccef6f94950',[node.coordinator?t('ce21265bf25'):'',count]):'');const name=document.createElement('span');name.className='skill-display-name';name.textContent=skill.name;if(skill.name!==skill.id)button.append(name);button.append(code,purpose,badge);
   button.addEventListener('click',()=>openNode(group.id,button,skill.id));tree.append(decorateSkill(button,skill.id,dictionary.provenance));
   if(node.children.length){const children=document.createElement('div');children.className='skill-children';children.append(...[...node.children].sort((a,b)=>Number(Boolean(a.children.length))-Number(Boolean(b.children.length))).map(createTree));tree.append(children);}return tree;
  }
  const forest=forests.get(group.id),branched=forest.roots.filter(node=>node.children.length),standalone=forest.roots.filter(node=>!node.children.length);
  list.append(...branched.map(createTree));
  if(standalone.length){const peers=document.createElement('div');peers.className='standalone-roots';peers.append(...standalone.map(createTree));list.append(peers);}
  for(const scope of getSupportScopes(group.id)){
   const scopeButton=document.createElement('button');scopeButton.className='support-scope-label';scopeButton.textContent=scope.label;scopeButton.dataset.supportScope=group.id;scopeButton.addEventListener('click',()=>showSupport(group.id,scopeButton));section.append(scopeButton);
  }
  const note=document.createElement('p');note.className='skill-group-note';note.textContent=group.note;note.hidden=!group.note;const loop=topicMap.loops.find(loop=>loop.from===group.id);
  section.append(heading,summary,toggle);if(loop){const button=document.createElement('button');button.type='button';button.className='topic-loop';button.dataset.topicRelation=loop.id;button.textContent=`↶ ${loop.label}`;button.addEventListener('click',()=>showTopicRelation(loop));section.append(button);}section.append(note,list);return section;
 });
 const board=document.createElement('div');board.className='global-topic-board';board.setAttribute('aria-label',t('cb68a20e391'));
 const svg=document.createElementNS('http://www.w3.org/2000/svg','svg');svg.id='topic-connections';svg.setAttribute('aria-hidden','true');svg.innerHTML='<defs><marker id="topic-support-arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto-start-reverse"><path d="M0,0 L7,3.5 L0,7" fill="var(--support-color)"/></marker><marker id="topic-arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto-start-reverse"><path d="M0,0 L7,3.5 L0,7" fill="currentColor"/></marker></defs><g id="topic-edge-paths"></g>';board.append(svg);
 for(const node of globalTopics.nodes){
  const section=groups.find(group=>group.dataset.context===node.id);section.style.setProperty('--topic-row',node.row);section.style.setProperty('--topic-column',node.column);
  const list=section.querySelector('.skill-node-list');const branch=document.createElement('section');branch.className='expanded-skill-branch';branch.dataset.branch=node.id;branch.hidden=true;
  const title=document.createElement('h3');title.textContent=t('c52c3548da1',[getNodeDetails(node.id).title]);
  const port=document.createElement('div');port.className='local-skill-scroll';port.setAttribute('aria-label',t('cc06e6abec6',[getNodeDetails(node.id).title]));port.tabIndex=0;
  const content=document.createElement('div');content.className='local-skill-content';
  const lines=document.createElementNS('http://www.w3.org/2000/svg','svg');lines.classList.add('local-skill-connections');lines.setAttribute('aria-hidden','true');lines.innerHTML=`<defs><marker id="local-arrow-${node.id}" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7" fill="currentColor"/></marker></defs><g class="local-skill-paths"></g>`;
  content.append(lines,list);port.append(content);branch.append(title,port);section.append(branch);
  const hint=document.createElement('p');hint.className='topic-purpose';hint.textContent=node.hint;section.insertBefore(hint,section.querySelector('.topic-toggle'));
  section.querySelector('.topic-summary').hidden=true;section.querySelector('.skill-group-note').hidden=true;board.append(section);
 }
 const labels=globalTopics.edges.map(edge=>{const button=document.createElement('button');button.type='button';button.className='global-topic-edge-label';button.dataset.topicRelation=edge.id;button.dataset.kind=edge.kind;button.textContent=edge.label;button.setAttribute('aria-label',t('c0106763057',[getNodeDetails(edge.from).title,edge.bidirectional?'↔':'→',getNodeDetails(edge.to).title,edge.label]));button.addEventListener('click',()=>showTopicRelation(edge));board.append(button);return button;});
 const controls=document.createElement('div');controls.className='map-disclosure-controls';const collapse=document.createElement('button');collapse.type='button';collapse.id='collapse-topics';collapse.textContent=t('c251a5b1b9d');collapse.addEventListener('click',()=>{topicState.collapseAll();closePanel();syncTopics();collapse.focus();});controls.append(collapse);
 $('#skill-groups').replaceChildren(controls,board);syncTopics();
 $('.map-key').replaceChildren(...[t('ce983002e67'),t('c578ddb44d7'),t('c45c99a67bb')].map(text=>{const span=document.createElement('span');span.textContent=text;return span;}));
 $('#relation-text').replaceChildren(...[...globalTopics.edges,...globalTopics.loops].map(edge=>{const li=document.createElement('li');li.textContent=`${getNodeDetails(edge.from).title} ${edge.bidirectional?'↔':'→'} ${getNodeDetails(edge.to).title}：${edge.condition}`;return li;}));
 $('#panel-preview').textContent=t('ceb5e906633');highlightSkill(null);
 new ResizeObserver(()=>{drawSkillEdges();drawTopicEdges();}).observe($('#skill-groups'));drawTopicEdges();
}
function drawTopicEdges(){
 if(getActiveView()!=="relations")return;
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
 for(const group of graph.groups){const open=topicState.expanded().includes(group.id),section=document.querySelector(`.skill-group[data-context="${group.id}"]`);section.dataset.expanded=String(open);document.getElementById(`skills-${group.id}`).hidden=!open;document.querySelector(`[data-branch="${group.id}"]`).hidden=!open;const button=section.querySelector('.topic-toggle');button.setAttribute('aria-expanded',String(open));button.textContent=t('c7eaca64fc4',[open?t('cafd4b78353'):t('c00bd3960fe'),group.skills.length]);}
 drawSkillEdges();drawTopicEdges();
}
function revealTopic(id){topicState.reveal(id);syncTopics();}

 return {renderMap,drawSkillEdges,drawTopicEdges,syncTopics,revealTopic,ensureTopicVisible,alignLocalSkill};
}
