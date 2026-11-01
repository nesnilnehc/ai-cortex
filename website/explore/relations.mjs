import {dictionary} from './locale.mjs?v=build-artifacts-20261101';
export function getExample(id){if(!Object.hasOwn(dictionary.examples,id))throw Error('Unknown example');return structuredClone(dictionary.examples[id]);}
