import {getCallHierarchy} from './relationship-model.mjs?v=aic08-provenance-3';
import {catalog} from './workflow.mjs?v=aic08-provenance-3';
import {getNodeDetails,getNodeSkillSelection} from './panel-model.mjs?v=aic08-provenance-3';
import rawEdges from './skill-edges.json?v=aic08-provenance-3' with {type:'json'};
import metadata from './skill-metadata.json?v=aic08-provenance-3' with {type:'json'};
import {dictionary} from './locale.mjs?v=aic08-provenance-3';
const sourceEdges=rawEdges.map(edge=>({...edge,...dictionary.skillEdges[edge.id]}));
const order=['direction','planning','research','design','quality','build','commit','release','foundation','collaboration'];
const ids=new Set(catalog.map(skill=>skill.id));
export function getSkillGraph(){return structuredClone({groups:metadata.groupOrder.map(id=>{const detail=getNodeDetails(id);return {id,title:detail.title,summary:detail.help.point,availability:['research','foundation','collaboration'].includes(id)?'anytime':'on-demand',note:dictionary.topics[id].note,skills:getNodeSkillSelection(id).skills};}),edges:sourceEdges});}
export function getSkillNeighborhood(id){
 if(!ids.has(id))throw new Error(`Unknown skill: ${id}`);
 const edges=sourceEdges.filter(edge=>edge.from===id||edge.to===id);
 return structuredClone({edges,related:[...new Set(edges.map(edge=>edge.from===id?edge.to:edge.from))]});
}

// One evidential parent controls placement, not execution order. Shared methods and coordinators remain roots.
export function getSkillForest(groupId){
 const group=getSkillGraph().groups.find(group=>group.id===groupId);if(!group)throw new Error('Unknown skill context');
 const tree=getCallHierarchy({view:'relations',groupId}),parents=new Map(tree.children.map(e=>[e.to,e]));
 const build=id=>({skill:group.skills.find(s=>s.id===id),via:parents.get(id)??null,coordinator:sourceEdges.some(e=>e.from===id&&e.kind==='call'),children:tree.children.filter(e=>e.from===id).map(e=>build(e.to))});
 const members=new Set(group.skills.map(s=>s.id));
 return structuredClone({roots:tree.roots.map(build),connections:sourceEdges.filter(e=>members.has(e.from)&&members.has(e.to)&&['call','sequence'].includes(e.kind))});
}

// Every node reserves a right-hand gutter; cross-column bridges run above the node area.
export function routeSkillConnection(from,to,origin,kind='call',obstacles=[]){
 const lanes={call:16,method:20,input:24,suggest:28,sequence:32,feedback:36};
 if(!Object.hasOwn(lanes,kind))throw new Error('Unknown relationship kind');
 const clear=points=>points.slice(1).every((point,index)=>{
  const before=points[index];return obstacles.every(rect=>{
   const left=rect.left-origin.left+.5,right=rect.right-origin.left-.5,top=rect.top-origin.top+.5,bottom=(rect.bottom??rect.top+rect.height)-origin.top-.5;
   return before[0]===point[0]?!(point[0]>left&&point[0]<right&&Math.max(before[1],point[1])>top&&Math.min(before[1],point[1])<bottom):!(point[1]>top&&point[1]<bottom&&Math.max(before[0],point[0])>left&&Math.min(before[0],point[0])<right);
  });
 });
 if(to.left>=from.right+12||from.left>=to.right+12){
  const forward=to.left>=from.right+12;
  const start=[(forward?from.right:from.left)-origin.left,from.top+from.height/2-origin.top],end=[(forward?to.left:to.right)-origin.left,to.top+to.height/2-origin.top];
  const middle=(start[0]+end[0])/2+(lanes[kind]-16);
  const points=[start,[middle,start[1]],[middle,end[1]],end];if(clear(points))return points;
 }
 const start=[from.right-origin.left,from.top+from.height/2-origin.top];
 const end=[to.right-origin.left,to.top+to.height/2-origin.top];
 const lane=Math.max(start[0],end[0],...obstacles.map(rect=>rect.right-origin.left))+lanes[kind];
 return [start,[lane,start[1]],[lane,end[1]],end];
}
