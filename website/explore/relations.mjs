import {dictionary} from './locale.mjs?v=artifact-inspection-20261104';
export function getExample(id){if(!Object.hasOwn(dictionary.examples,id))throw Error('Unknown example');return structuredClone(dictionary.examples[id]);}
