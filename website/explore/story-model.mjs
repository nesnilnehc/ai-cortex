import {dictionary} from './locale.mjs?v=aic06-build-release-1';
import {findSkills} from './workflow.mjs?v=aic06-build-release-1';
export function getSimpleGate(id){if(!Object.hasOwn(dictionary.extras.gates,id))throw Error('Unknown gate state');return structuredClone(dictionary.extras.gates[id]);}
export function getToolGroups(query=''){const matches=findSkills({query});return dictionary.extras.lookup.map(group=>({...group,skills:matches.filter(skill=>group.skills.includes(skill.id))})).filter(group=>group.skills.length);}
