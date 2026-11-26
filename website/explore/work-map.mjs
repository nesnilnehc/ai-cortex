import {dictionary} from './locale.mjs?v=manage-secret-1-2-0-20261126';
export const getHelpLabels=()=>structuredClone(dictionary.extras.labels);
export const getMapProjection=()=>({nodes:Object.fromEntries(Object.entries(dictionary.topics).map(([id,topic])=>[id,{...dictionary.extras.projection.nodes[id],title:topic.name}]))});
