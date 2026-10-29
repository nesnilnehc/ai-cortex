import {dictionary} from './locale.mjs?v=aic06-build-release-1';
export function getExample(id){if(!Object.hasOwn(dictionary.examples,id))throw Error('Unknown example');return structuredClone(dictionary.examples[id]);}
