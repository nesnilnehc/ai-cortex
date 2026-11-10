import {dictionary} from './locale.mjs?v=rename-session-20261110';
export function getExample(id){if(!Object.hasOwn(dictionary.examples,id))throw Error('Unknown example');return structuredClone(dictionary.examples[id]);}
