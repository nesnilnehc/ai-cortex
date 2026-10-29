import loops from './topic-map.json?v=aic08-provenance-3' with {type:'json'};
import {dictionary} from './locale.mjs?v=aic08-provenance-3';
import metadata from './skill-metadata.json?v=aic08-provenance-3' with {type:'json'};
export const getTopicMap=()=>structuredClone({...dictionary.extras.topicMap,loops:loops.map(loop=>({...loop,...dictionary.loops[loop.id]}))});
export function createTopicState(){
 const valid=new Set(metadata.groupOrder),open=new Set();
 const check=id=>{if(!valid.has(id))throw new Error(`Unknown topic: ${id}`);};
 return {expanded:()=>[...open],toggle(id){check(id);if(open.has(id))open.delete(id);else {open.clear();open.add(id);}},reveal(id){check(id);open.clear();open.add(id);},collapseAll(){open.clear();}};
}
