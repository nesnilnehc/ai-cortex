import {dictionary} from './locale.mjs?v=aic08-provenance-1';
export function getExample(id){if(!Object.hasOwn(dictionary.examples,id))throw Error('Unknown example');return structuredClone(dictionary.examples[id]);}
