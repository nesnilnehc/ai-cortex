import {decorateSkill} from './provenance.mjs?v=aic08-provenance-2';
import {getSupportScopes} from './support-scopes.mjs?v=aic08-provenance-2';
import {classification,getCallHierarchy,getSkillOrder,relationships} from './relationship-model.mjs?v=aic08-provenance-2';
import {catalog} from './workflow.mjs?v=aic08-provenance-2';
import {dictionary} from './locale.mjs?v=aic08-provenance-2';
export function mountClassification(container,{onSelectSkill,onSelectRelation,onSelectSupport,onCollapse,onViewStateChange}){
 const support=document.createElement('div');support.className='classification-support';for(const id of ['foundation','collaboration']){const scope=getSupportScopes(id)[0],button=document.createElement('button');button.type='button';button.dataset.classSupport=id;button.textContent=scope.label;button.addEventListener('click',()=>onSelectSupport(id,button));support.append(button);}container.prepend(support);
 const find=id=>container.querySelector(`[data-class-skill="${id}"]`);
 for(const group of classification.groups){
  let userToggle=false;const card=container.querySelector(`[id="${group.id}"]`),body=card.querySelector('.classification-body'),tree=getCallHierarchy({view:'classification',groupId:group.id}),list=document.createElement('ul');
  function node(id){const skill=catalog.find(s=>s.id===id),li=document.createElement('li'),a=document.createElement('button');a.type='button';a.className='classification-skill';a.dataset.classSkill=id;a.setAttribute('aria-pressed','false');
   for(const [tag,text]of[['span',skill.name],['code',skill.id],['small',skill.purpose]]){if(tag==='span'&&skill.name===skill.id)continue;const child=document.createElement(tag);child.textContent=text;a.append(child);}
   a.addEventListener('click',()=>onSelectSkill(id,a));li.append(decorateSkill(a,id,dictionary.provenance));
   const parent=tree.children.find(e=>e.to===id);if(parent){const label=document.createElement('button');label.type='button';label.className='call-condition';label.dataset.callMode=parent.callMode;label.textContent=dictionary.dual[parent.callMode];label.addEventListener('click',()=>onSelectRelation(parent.id,label));li.prepend(label);}
   const children=tree.children.filter(e=>e.from===id);if(children.length){const ul=document.createElement('ul');ul.className='call-children';ul.append(...children.map(e=>node(e.to)));li.append(ul);}
   const related=relationships.filter(e=>e.from===id&&!tree.children.some(c=>c.id===e.id));
   if(related.length){const refs=document.createElement('details'),summary=document.createElement('summary');summary.textContent=`${dictionary.dual.reference} · ${related.length}`;refs.append(summary);for(const edge of related){const b=document.createElement('button');b.type='button';b.className='classification-reference';b.dataset.classRelation=edge.id;b.textContent=`${edge.kind==='sequence'?dictionary.dual.sequence:edge.kind==='call'?dictionary.dual[edge.callMode]:edge.label} → ${catalog.find(s=>s.id===edge.to).name}`;b.addEventListener('click',()=>onSelectRelation(edge.id,b));refs.append(decorateSkill(b,edge.to,dictionary.provenance));}li.append(refs);}
   return li;
  }
  list.append(...tree.roots.map(node));const note=document.createElement('p');note.className='browse-note';note.textContent=dictionary.dual.browse;body.replaceChildren(note,list);
  card.querySelector('summary').addEventListener('click',()=>{userToggle=true;});
  card.addEventListener('toggle',()=>{onViewStateChange(capture());if(!card.open&&userToggle)onCollapse(group.skillIds,card.querySelector('summary'));userToggle=false;});
 }
 function capture(){return {expandedCategoryIds:[...container.querySelectorAll('.classification-card[open]')].map(n=>n.id),scrollByRegion:Object.fromEntries([...container.querySelectorAll('.classification-card')].map(c=>[c.id,c.querySelector('.classification-body').scrollTop]))};}
 function restore(snapshot){for(const card of container.querySelectorAll('.classification-card')){card.open=snapshot.expandedCategoryIds.includes(card.id);card.querySelector('.classification-body').scrollTop=snapshot.scrollByRegion[card.id]??0;}}
 function reveal(id){const button=find(id);if(!button)return;const card=button.closest('details.classification-card');card.open=true;const port=card.querySelector('.classification-body');const r=button.getBoundingClientRect(),p=port.getBoundingClientRect();if(r.top<p.top||r.bottom>p.bottom)port.scrollTop+=r.top-p.top-10;return button;}
 return {capture,restore,reveal,find,highlight(id){for(const b of container.querySelectorAll('[data-class-skill]'))b.setAttribute('aria-pressed',String(b.dataset.classSkill===id));}};
}
