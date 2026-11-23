import {dictionary} from './locale.mjs?v=plan-next-17-1-0-20261123';
export function getExample(id){if(!Object.hasOwn(dictionary.examples,id))throw Error('Unknown example');return structuredClone(dictionary.examples[id]);}
