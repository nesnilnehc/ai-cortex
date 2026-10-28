import {catalog} from './workflow.mjs?v=topic-local-branches';
import {getNodeDetails,getNodeSkillSelection} from './panel-model.mjs?v=topic-local-branches';
import sourceEdges from './skill-edges.json?v=topic-local-branches' with {type:'json'};
const order=['direction','planning','research','design','quality','build','commit','release','foundation','collaboration'];
const ids=new Set(catalog.map(skill=>skill.id));
export function getSkillGraph(){
 return structuredClone({groups:order.map(id=>{const detail=getNodeDetails(id);return {id,title:detail.title,summary:detail.help.point,availability:['research','foundation','collaboration'].includes(id)?'anytime':'on-demand',note:id==='release'?'发布前要核对材料、检查与授权；公告依据实际发布结果。':id==='commit'?'保存、整合和发布是不同动作，按本次需要选择。':id==='quality'?'工程质量、是否符合原意、实际运行结果分别核对。':'',skills:getNodeSkillSelection(id).skills};}),edges:sourceEdges});
}
export function getSkillNeighborhood(id){
 if(!ids.has(id))throw new Error(`Unknown skill: ${id}`);
 const edges=sourceEdges.filter(edge=>edge.from===id||edge.to===id);
 return structuredClone({edges,related:[...new Set(edges.map(edge=>edge.from===id?edge.to:edge.from))]});
}

// One evidential parent controls placement, not execution order. Shared methods and coordinators remain roots.
export function getSkillForest(groupId){
 const group=getSkillGraph().groups.find(group=>group.id===groupId);if(!group)throw new Error('Unknown skill context');
 const members=new Set(group.skills.map(skill=>skill.id)),inside=sourceEdges.filter(edge=>members.has(edge.from)&&members.has(edge.to));
 const locked=new Set(group.skills.filter(skill=>inside.filter(edge=>edge.from===skill.id&&edge.kind==='call').length>=2||inside.filter(edge=>edge.to===skill.id&&edge.kind==='method').length>1).map(skill=>skill.id));
 const rank={call:0,input:1,method:2,suggest:3},parents=new Map();
 for(const edge of [...inside].sort((a,b)=>rank[a.kind]-rank[b.kind])){
  if(locked.has(edge.to)||parents.has(edge.to))continue;
  let ancestor=edge.from,cycle=false;
  while(ancestor){if(ancestor===edge.to){cycle=true;break;}ancestor=parents.get(ancestor)?.from;}
  if(!cycle)parents.set(edge.to,edge);
 }
 const build=id=>({skill:group.skills.find(skill=>skill.id===id),via:parents.get(id)??null,coordinator:sourceEdges.filter(edge=>edge.from===id&&edge.kind==='call').length>=2,children:group.skills.filter(skill=>parents.get(skill.id)?.from===id).map(skill=>build(skill.id))});
 const roots=group.skills.filter(skill=>!parents.has(skill.id)).map(skill=>build(skill.id));
 const branchIds=new Set([...parents.values()].map(edge=>edge.id));
 const connections=inside.filter(edge=>branchIds.has(edge.id)||edge.kind==='method'||edge.kind==='call');
 return structuredClone({roots,connections});
}

// Every node reserves a right-hand gutter; cross-column bridges run above the node area.
export function routeSkillConnection(from,to,origin,kind='call',obstacles=[]){
 const lanes={call:16,method:20,input:24,suggest:28};
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
 const sourceLane=start[0]+lanes[kind],targetLane=end[0]+lanes[kind];
 if(Math.abs(sourceLane-targetLane)<1)return [start,[sourceLane,start[1]],[targetLane,end[1]],end];
 const low=Math.min(sourceLane,targetLane),high=Math.max(sourceLane,targetLane);
 const blockers=obstacles.filter(rect=>rect.left-origin.left<high&&rect.right-origin.left>low).map(rect=>({top:rect.top-origin.top,bottom:(rect.bottom??rect.top+rect.height)-origin.top}));
 const candidates=[8,...blockers.flatMap(rect=>[rect.top-4,rect.bottom+4])].filter(y=>y>=8).sort((a,b)=>Math.abs(a-start[1])-Math.abs(b-start[1]));
 const bridge=candidates.find(y=>blockers.every(rect=>y<rect.top-2||y>rect.bottom+2))??8;
 return [start,[sourceLane,start[1]],[sourceLane,bridge],[targetLane,bridge],[targetLane,end[1]],end];
}
