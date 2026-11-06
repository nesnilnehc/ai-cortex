import metadata from './skill-metadata.json?v=milestone-planning-20261106' with {type:'json'};
import {dictionary} from './locale.mjs?v=milestone-planning-20261106';
export const catalog=Object.freeze(Object.values(metadata.skills).map(skill=>Object.freeze({id:skill.id,description:skill.description,name:dictionary.skills[skill.id].name,purpose:dictionary.skills[skill.id].purpose})));
export function findSkills({query=''}={}){const term=query.trim().toLocaleLowerCase();return catalog.filter(skill=>`${skill.id} ${skill.name} ${skill.purpose} ${skill.description}`.toLocaleLowerCase().includes(term));}
