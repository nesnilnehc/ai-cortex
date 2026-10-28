import {getPlan,getScenario} from './model.mjs';
import {getRelationship,getTrace} from './relationship.mjs';
const $=s=>document.querySelector(s);
let scenario='backlog';
let selectedGoal='all';
let selectedNode='backlog';
let selectedEvent='base';
const insight={direction:'<strong>从目标看工作：</strong>每张工作卡都说明它服务的结果。方向尚未确定时，先形成目标草案，不急着排满计划。',backlog:'<strong>从取舍看安排：</strong>P0 / P1 表示重要程度；Now / Next / Later 还取决于依赖和容量。试试下方的“依赖延期”。',existing:'<strong>从原计划看缺口：</strong>这里保留同一份基线。整理时核对目标、来源、开始条件和完成依据，不自动改动已经作出的安排。',change:'<strong>从变化看影响：</strong>选择下方事件，查看相对基线的变化。状态和日期由维护处理，层级调整另形成待确认提案。'};
function renderScenario(key){
 scenario=key;const data=getScenario(key);
 for(const b of document.querySelectorAll('[data-scenario]'))b.setAttribute('aria-pressed',String(b.dataset.scenario===key));
 $('#scenario-title').textContent=data.title;$('#scenario-intro').textContent=data.intro;
 $('#artifact').textContent=data.artifact;$('#detail').textContent=data.detail;$('#prompt').value=data.prompt;
 $('#scenario-insight').innerHTML=insight[key];
 document.querySelectorAll('.journey li').forEach((node,i)=>node.classList.toggle('active',i===data.focus));
 $('#skills').replaceChildren(...data.skills.map(name=>{const li=document.createElement('li'),a=document.createElement('a');a.textContent=name;a.href=`../../skills/${name}/SKILL.md`;li.append(a);return li;}));
 $('#copy-status').textContent='切换场景会更新默认请求。';
 renderNode({direction:'direction',backlog:'choices',existing:'roadmap',change:'feedback'}[key]);
 renderPlan('base');
}
function renderPlan(event){
 selectedEvent=event;
 const plan=getPlan(event),base=getPlan('base');
 for(const b of document.querySelectorAll('[data-event]'))b.setAttribute('aria-pressed',String(b.dataset.event===event));
 $('#plan').replaceChildren(...['Now','Next','Later'].map((tier,i)=>{
 const lane=document.createElement('section');lane.className='lane';
 const items=plan.items.filter(item=>item.tier===tier);
 const heading=document.createElement('h4');heading.textContent=tier;const count=document.createElement('span');count.textContent=String(items.length).padStart(2,'0');heading.append(count);lane.append(heading);
 const caption=document.createElement('p');caption.textContent=['当前聚焦的工作','下一步，等待条件','后续方向，择机复核'][i];lane.append(caption);
 for(const item of items){
 const original=base.items.find(x=>x.id===item.id);const delta=!original?'新增事项 · 安排提案':original.tier!==item.tier?`${original.tier} → ${item.tier} · 安排提案`:original.state!==item.state?'状态更新 · 验收记录':original.condition!==item.condition?'开始条件更新':'';
 const card=document.createElement('article');card.className=`work-item${delta?' changed':''}`;card.dataset.item=item.id;
 const meta=document.createElement('div');meta.className='item-meta';meta.textContent=item.id;const priority=document.createElement('span');priority.className='priority';priority.textContent=item.priority;meta.append(priority);card.append(meta);
 const h=document.createElement('h5');h.textContent=item.name;card.append(h);
 for(const [value,className] of [[item.state,'state'],[item.condition,''],[`目标：${item.goal}`,'']]){const p=document.createElement('p');p.className=className;p.textContent=value;card.append(p);}
 if(delta){const mark=document.createElement('span');mark.className='delta';mark.textContent=delta;card.append(mark);}lane.append(card);
 }return lane;
 }));
 $('#reason').textContent=plan.reason;$('#changes').replaceChildren(...plan.changes.map(text=>{const li=document.createElement('li');li.textContent=text;return li;}));
 renderTrace();
}
document.querySelectorAll('[data-scenario]').forEach(b=>b.addEventListener('click',()=>renderScenario(b.dataset.scenario)));
document.querySelectorAll('[data-event]').forEach(b=>b.addEventListener('click',()=>renderPlan(b.dataset.event)));
$('#reset').addEventListener('click',()=>renderPlan('base'));
$('#copy').addEventListener('click',async()=>{try{await navigator.clipboard.writeText($('#prompt').value);$('#copy-status').textContent='已复制，可粘贴到你的智能体。';}catch{$('#prompt').focus();$('#prompt').select();$('#copy-status').textContent='自动复制不可用，请按 ⌘C 或 Ctrl+C 复制所选请求。';}});
function renderNode(key){
 selectedNode=key;
 const node=getRelationship(key);
 document.querySelectorAll('[data-node]').forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.node===key)));
 for(const [selector,value] of Object.entries({'#node-title':node.title,'#node-question':node.question,'#node-input':node.input,'#node-output':node.output,'#node-example':node.example,'#node-boundary':node.boundary}))$(selector).textContent=value;
 $('#node-skills').replaceChildren(...node.skills.map(name=>{
  const li=document.createElement('li'),a=document.createElement('a');
  a.textContent=name;a.href=`../../skills/${name}/SKILL.md`;li.append(a);return li;
 }));
 $('#node-skills-disclosure').open=false;
}
function renderTrace(){
 const trace=getTrace(selectedGoal,selectedEvent);
 document.querySelectorAll('[data-goal]').forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.goal===selectedGoal)));
 $('#trace-goal').textContent=`${trace.goal.id==='ALL'?'':trace.goal.id+' · '}${trace.goal.outcome}`;
 $('#trace-backlog').textContent=trace.items.map(item=>`${item.id} ${item.name} · ${item.priority}`).join('\n');
 $('#trace-plan').textContent=trace.items.map(item=>`${item.id} → ${item.tier} · ${item.state}`).join('\n');
 $('#trace-metric').textContent=trace.goal.metric;
 $('#example-goals').textContent=selectedGoal==='all'?'可靠提交 · 找到记录 · 复用结果':`${trace.goal.id} · ${trace.goal.title}`;
 $('#example-backlog').textContent=trace.items.map(item=>item.id).join(' · ');
 $('#example-roadmap').textContent=['Now','Next','Later'].map(tier=>`${tier} ${trace.items.filter(item=>item.tier===tier).length}`).join(' · ');
 $('#example-choices').textContent=selectedGoal==='find'&&selectedEvent==='delay'?'搜索仍是 P1，但依赖尚未就绪':'重要程度与就绪分别判断';
 $('#example-feedback').textContent=selectedEvent==='base'?'交付反馈，重新检查目标与工作':{delay:'接口延期 → 复核依赖与安排',urgent:'入口故障 → 新增问题并重新取舍',complete:'验收通过 → 仍需观察用户价值'}[selectedEvent];
 const ids=new Set(trace.items.map(item=>item.id));
 document.querySelectorAll('[data-item]').forEach(card=>{
  card.classList.toggle('trace-match',selectedGoal!=='all'&&ids.has(card.dataset.item));
  card.classList.toggle('trace-other',selectedGoal!=='all'&&!ids.has(card.dataset.item));
 });
}
document.querySelectorAll('[data-node]').forEach(button=>button.addEventListener('click',()=>renderNode(button.dataset.node)));
document.querySelectorAll('[data-goal]').forEach(button=>button.addEventListener('click',()=>{selectedGoal=button.dataset.goal;renderTrace();}));
document.querySelectorAll('[data-view]').forEach(button=>button.addEventListener('click',()=>{
 const relation=button.dataset.view==='relation';
 document.querySelectorAll('[data-view]').forEach(other=>other.setAttribute('aria-pressed',String(button===other)));
 $('#relation-view').hidden=!relation;$('#sequence-view').hidden=relation;
 $('.node-detail').hidden=!relation;$('.map-support').hidden=!relation;
}));
renderScenario(scenario);
