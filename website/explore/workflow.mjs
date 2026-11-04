import metadata from './skill-metadata.json?v=artifact-protocols-20261104' with {type:'json'};
import {dictionary} from './locale.mjs?v=artifact-protocols-20261104';
export const catalog=Object.freeze(Object.values(metadata.skills).map(skill=>Object.freeze({id:skill.id,description:skill.description,name:dictionary.skills[skill.id].name,purpose:dictionary.skills[skill.id].purpose})));
export function findSkills({query=''}={}){const term=query.trim().toLocaleLowerCase();return catalog.filter(skill=>`${skill.id} ${skill.name} ${skill.purpose} ${skill.description}`.toLocaleLowerCase().includes(term));}
