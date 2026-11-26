import {dictionary} from './locale.mjs?v=manage-secret-1-2-1-20261126';
export function getExample(id){if(!Object.hasOwn(dictionary.examples,id))throw Error('Unknown example');return structuredClone(dictionary.examples[id]);}
