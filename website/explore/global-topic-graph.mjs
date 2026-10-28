import sourceEdges from './topic-edges.json?v=aic08-provenance-1' with {type:'json'};
import {dictionary} from './locale.mjs?v=aic08-provenance-1';
const edges=sourceEdges.map(edge=>({...edge,...dictionary.topicEdges[edge.id]}));
import {getTopicMap} from './topic-map.mjs?v=aic08-provenance-1';
const nodes=[
 {id:'direction',row:1,column:1,hint:''},
 {id:'planning',row:1,column:2,hint:''},
 {id:'design',row:1,column:3,hint:''},
 {id:'foundation',row:2,column:1,hint:''},
 {id:'research',row:2,column:2,hint:''},
 {id:'quality',row:2,column:3,hint:''},
 {id:'build',row:2,column:4,hint:''},
 {id:'collaboration',row:3,column:1,hint:''},
 {id:'release',row:3,column:3,hint:''},
 {id:'commit',row:3,column:4,hint:''}
];
export function getGlobalTopicGraph(){return structuredClone({nodes:nodes.map(node=>({...node,hint:dictionary.topics[node.id].hint})),edges,loops:getTopicMap().loops});}
export function routeTopicRelationship(edge,rectangles,origin,mobile=false){
 const a=rectangles.get(edge.from),b=rectangles.get(edge.to);
 if(!a||!b)throw new Error('Unknown topic relationship');
 const x=r=>(r.left+r.right)/2,y=r=>(r.top+r.bottom)/2;
 let points,label,maxWidth=74;
 if(mobile){
  const left=rectangles.get('direction'),right=rectangles.get('planning'),middle=(left.right+right.left)/2;
  switch(edge.id){
   case 'goal-basis':points=[[a.right,y(a)],[b.left,y(b)]];break;
   case 'planning-design':case 'design-quality':case 'norms-collaboration':points=[[x(a),a.bottom],[x(b),b.top]];break;
   case 'repair-feedback':points=[[x(a),a.bottom],[x(b),b.top]];break;
   case 'research-collaboration':points=[[x(a),a.top],[x(b),b.bottom]];break;
   case 'research-planning':case 'norms-planning':{
    const outer=edge.id==='research-planning',lane=origin.left+(outer?3:17),top=right.top-(outer?48:24),end=b.left+b.width*(outer?.72:.28);
    points=[[a.left,y(a)],[lane,y(a)],[lane,top],[end,top],[end,b.top]];label=[(lane+end)/2,top];maxWidth=110;break;
   }
   case 'quality-planning':{
    const lane=middle-5,start=a.top+a.height*.3,end=b.top+b.height*.72;points=[[a.left,start],[lane,start],[lane,end],[b.left,end]];label=[lane,(start+end)/2];maxWidth=48;break;
   }
   case 'design-build':{
    const lane=origin.right-8;points=[[a.right,y(a)],[lane,y(a)],[lane,y(b)],[b.right,y(b)]];label=[origin.right-30,(y(a)+y(b))/2];maxWidth=54;break;
   }
   case 'checks-release':{
    const lane=middle+5,bridge=b.top-25,start=a.top+a.height*.8;points=[[a.left,start],[lane,start],[lane,bridge],[x(b),bridge],[x(b),b.top]];label=[lane,(start+bridge)/2];maxWidth=48;break;
   }
   case 'history-release':points=[[a.left,y(a)],[b.right,y(b)]];maxWidth=48;break;
   case 'conditional-commit':{
    const line=Math.max(a.bottom,b.bottom)+25;points=[[x(a),a.bottom],[x(a),line],[x(b),line],[x(b),b.bottom]];label=[(x(a)+x(b))/2,line];maxWidth=110;break;
   }
   default:throw new Error('Unknown topic relationship');
  }
  if(!label){label=[(points[0][0]+points.at(-1)[0])/2,(points[0][1]+points.at(-1)[1])/2];if(edge.id==='goal-basis')maxWidth=48;}
 }else{
  const headerY=r=>r.top+Math.min(40,r.height/2),bridge=(Math.max(...nodes.filter(n=>n.row===1).map(n=>rectangles.get(n.id).bottom))+Math.min(...nodes.filter(n=>n.row===2).map(n=>rectangles.get(n.id).top)))/2;
  switch(edge.id){
   case 'goal-basis':case 'planning-design':case 'repair-feedback':points=[[a.right,headerY(a)],[b.left,headerY(b)]];break;
   case 'design-quality':case 'norms-collaboration':case 'checks-release':points=[[x(a),a.bottom],[x(b),b.top]];break;
   case 'research-planning':points=[[x(a),a.top],[x(b),b.bottom]];break;
   case 'norms-planning':points=[[x(a),a.top],[x(a),bridge],[b.left+20,bridge],[b.left+20,b.bottom]];label=[(x(a)+b.left+20)/2,bridge];break;
   case 'quality-planning':points=[[a.left+20,a.top],[a.left+20,bridge],[b.right-20,bridge],[b.right-20,b.bottom]];label=[(a.left+b.right)/2,bridge];break;
   case 'design-build':points=[[a.right-20,a.bottom],[a.right-20,bridge],[x(b),bridge],[x(b),b.top]];label=[(a.right-20+x(b))/2,bridge];break;
   case 'research-collaboration':points=[[x(a),a.bottom],[x(a),headerY(b)],[b.right,headerY(b)]];label=[(x(a)+b.right)/2,headerY(b)];break;
   case 'history-release':points=[[a.left,headerY(a)],[b.right,headerY(b)]];break;
   case 'conditional-commit':{const line=Math.max(a.bottom,b.bottom)+25;points=[[x(a),a.bottom],[x(a),line],[x(b),line],[x(b),b.bottom]];label=[(x(a)+x(b))/2,line];maxWidth=140;break;}
   default:throw new Error('Unknown topic relationship');
  }
  label??=[(points[0][0]+points.at(-1)[0])/2,(points[0][1]+points.at(-1)[1])/2];
 }
 return {points:points.map(([px,py])=>[px-origin.left,py-origin.top]),label:[label[0]-origin.left,label[1]-origin.top],maxWidth};
}
