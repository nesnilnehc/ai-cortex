import {dictionary} from './locale.mjs?v=presales-sync-20261102';
export function getExample(id){if(!Object.hasOwn(dictionary.examples,id))throw Error('Unknown example');return structuredClone(dictionary.examples[id]);}
