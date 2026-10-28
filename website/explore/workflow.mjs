import metadata from './skill-metadata.json?v=aic08-provenance-2' with {type:'json'};
import {dictionary} from './locale.mjs?v=aic08-provenance-2';
export const catalog=Object.freeze(Object.values(metadata.skills).map(skill=>Object.freeze({id:skill.id,description:skill.description,name:dictionary.skills[skill.id].name,purpose:dictionary.skills[skill.id].purpose})));
export function findSkills({query=''}={}){const term=query.trim().toLocaleLowerCase();return catalog.filter(skill=>`${skill.id} ${skill.name} ${skill.purpose} ${skill.description}`.toLocaleLowerCase().includes(term));}
