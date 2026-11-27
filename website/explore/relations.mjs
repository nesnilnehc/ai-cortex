import {dictionary} from './locale.mjs?v=upgrade-dependencies-1-0-0-20261127';
export function getExample(id){if(!Object.hasOwn(dictionary.examples,id))throw Error('Unknown example');return structuredClone(dictionary.examples[id]);}
