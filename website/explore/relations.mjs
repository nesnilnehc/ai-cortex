import {dictionary} from './locale.mjs?v=version-delivery-20261104';
export function getExample(id){if(!Object.hasOwn(dictionary.examples,id))throw Error('Unknown example');return structuredClone(dictionary.examples[id]);}
