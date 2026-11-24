import {dictionary} from './locale.mjs?v=rename-session-0-1-1-20261124';
export function getExample(id){if(!Object.hasOwn(dictionary.examples,id))throw Error('Unknown example');return structuredClone(dictionary.examples[id]);}
