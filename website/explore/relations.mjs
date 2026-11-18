import {dictionary} from './locale.mjs?v=upgrade-dependencies-20261118';
export function getExample(id){if(!Object.hasOwn(dictionary.examples,id))throw Error('Unknown example');return structuredClone(dictionary.examples[id]);}
