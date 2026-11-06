import {dictionary} from './locale.mjs?v=milestone-planning-20261106';
export function getExample(id){if(!Object.hasOwn(dictionary.examples,id))throw Error('Unknown example');return structuredClone(dictionary.examples[id]);}
