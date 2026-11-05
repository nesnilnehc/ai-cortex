import {dictionary} from './locale.mjs?v=version-notes-refinement-20261105';
export const getHelpLabels=()=>structuredClone(dictionary.extras.labels);
export const getMapProjection=()=>({nodes:Object.fromEntries(Object.entries(dictionary.topics).map(([id,topic])=>[id,{...dictionary.extras.projection.nodes[id],title:topic.name}]))});
