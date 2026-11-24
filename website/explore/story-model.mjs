import {dictionary} from './locale.mjs?v=rename-session-0-1-1-20261124';
import {findSkills} from './workflow.mjs?v=rename-session-0-1-1-20261124';
export function getSimpleGate(id){if(!Object.hasOwn(dictionary.extras.gates,id))throw Error('Unknown gate state');return structuredClone(dictionary.extras.gates[id]);}
export function getToolGroups(query=''){const matches=findSkills({query});return dictionary.extras.lookup.map(group=>({...group,skills:matches.filter(skill=>group.skills.includes(skill.id))})).filter(group=>group.skills.length);}
