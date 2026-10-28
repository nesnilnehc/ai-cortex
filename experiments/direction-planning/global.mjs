import {catalog,stages,getStage,findSkills,getGateState} from './workflow.mjs';
const $=selector=>document.querySelector(selector);
let currentStage='quality';
let currentGate='missing';
let selectedSkill=null;
const select=$('#stage-filter');
for(const stage of stages){const option=document.createElement('option');option.value=stage.id;option.textContent=`${stage.title} · ${stage.skills.length} 项`;select.append(option);}
for(const button of document.querySelectorAll('[data-stage]'))button.querySelector('.stage-count').textContent=`${getStage(button.dataset.stage).skills.length} 项`;
function renderStage(id,{resetSearch=true,updateLibrary=true}={}){
 const stage=getStage(id);currentStage=id;
 document.querySelectorAll('[data-stage]').forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.stage===id)));
 $('#stage-overline').textContent=`当前环节 / ${stage.skills.length} 项技能`;
 $('#stage-title').textContent=stage.title;$('#stage-question').textContent=stage.question;
 $('#stage-input').textContent=stage.input;$('#stage-output').textContent=stage.output;$('#stage-boundary').textContent=stage.boundary;
 $('#stage-steps').replaceChildren(...stage.steps.map((text,i)=>{const li=document.createElement('li'),number=document.createElement('span');number.textContent=String(i+1).padStart(2,'0');li.append(number,document.createTextNode(text));return li;}));
 $('#quality-demo').hidden=id!=='quality';$('#commit-demo').hidden=id!=='commit';
 $('#open-planning').hidden=id!=='planning'||!$('#planning-explorer').hidden;
 $('#close-planning').hidden=$('#planning-explorer').hidden;
 $('#global-prompt').value=stage.prompt;$('#global-copy-status').textContent='可编辑后复制；切换环节会恢复该环节的默认请求。';
 if(updateLibrary){select.value=id;if(resetSearch)$('#skill-search').value='';renderLibrary();}
}
function renderGate(id){
 currentGate=id;const gate=getGateState(id);
 document.querySelectorAll('[data-gate]').forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.gate===id)));
 $('#gate-engineering').textContent=gate.engineering;$('#gate-alignment').textContent=gate.alignment;$('#gate-verification').textContent=gate.verification;
 $('#gate-title').textContent=gate.title;$('#gate-note').textContent=gate.note;
 $('#gate-next').textContent=gate.mayProceed?'看看如何提交 →':id==='fail'?'回看实施与验证 ↶':'查看本环节技能 ↓';
}
function renderLibrary(){
 const matches=findSkills({query:$('#skill-search').value,stage:select.value});
 $('#library-status').textContent=`显示 ${matches.length} / ${catalog.length} 项技能${select.value==='all'?' · 全部环节':` · ${getStage(select.value).title}`}。点击用途，查看所属环节与技能原文。`;
 $('#skill-empty').hidden=matches.length>0;
 $('#selected-skill').hidden=true;selectedSkill=null;
 $('#skill-results').replaceChildren(...matches.map(skill=>{
  const button=document.createElement('button');button.type='button';button.className='skill-result';button.dataset.skill=skill.id;button.setAttribute('aria-pressed','false');
  const strong=document.createElement('strong'),code=document.createElement('code');strong.textContent=skill.purpose;code.textContent=skill.id;button.append(strong,code);
  button.addEventListener('click',()=>{
   selectedSkill=skill.id;const stage=stages.find(stage=>stage.skills.includes(skill.id));
   renderStage(stage.id,{updateLibrary:false});
   document.querySelectorAll('[data-skill]').forEach(other=>other.setAttribute('aria-pressed',String(other.dataset.skill===selectedSkill)));
   $('#selected-skill').hidden=false;$('#selected-skill-title').textContent=skill.id;$('#selected-skill-purpose').textContent=skill.purpose;
   $('#selected-skill-stage').textContent=`所在环节：${stage.title}。点击上方对应节点，可查看输入、产出与工作衔接。`;
   $('#selected-skill-source').href=`../../skills/${skill.id}/SKILL.md`;
   $('#selected-skill').scrollIntoView({block:'center'});
  });return button;
 }));
}
function showAll(){select.value='all';$('#skill-search').value='';renderLibrary();}
document.querySelectorAll('[data-stage]').forEach(button=>button.addEventListener('click',()=>renderStage(button.dataset.stage)));
document.querySelectorAll('[data-gate]').forEach(button=>button.addEventListener('click',()=>renderGate(button.dataset.gate)));
$('#gate-next').addEventListener('click',()=>{
 if(currentGate==='pass')renderStage('commit');
 else if(currentGate==='fail')renderStage('build');
 else $('#skill-library').scrollIntoView({block:'start'});
});
$('#skill-search').addEventListener('input',renderLibrary);
select.addEventListener('change',()=>{if(select.value!=='all')renderStage(select.value,{resetSearch:false});else renderLibrary();});
$('#show-all').addEventListener('click',showAll);$('#browse-all').addEventListener('click',showAll);$('#clear-search').addEventListener('click',showAll);
$('#stage-skills-link').addEventListener('click',()=>{select.value=currentStage;$('#skill-search').value='';renderLibrary();});
$('#open-planning').addEventListener('click',()=>{
 $('#planning-explorer').hidden=false;$('#open-planning').hidden=true;$('#close-planning').hidden=false;$('#planning-explorer').scrollIntoView({block:'start'});
});
$('#close-planning').addEventListener('click',()=>{
 $('#planning-explorer').hidden=true;$('#close-planning').hidden=true;$('#open-planning').hidden=currentStage!=='planning';$('.stage-detail').scrollIntoView({block:'start'});
});
$('#global-copy').addEventListener('click',async()=>{
 try{await navigator.clipboard.writeText($('#global-prompt').value);$('#global-copy-status').textContent='已复制，可粘贴到你的智能体。';}
 catch{$('#global-prompt').focus();$('#global-prompt').select();$('#global-copy-status').textContent='自动复制不可用，请按 ⌘C 或 Ctrl+C 复制所选请求。';}
});
renderStage(currentStage);renderGate(currentGate);
