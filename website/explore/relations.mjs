import {dictionary} from './locale.mjs?v=version-notes-refinement-20261105';
export function getExample(id){if(!Object.hasOwn(dictionary.examples,id))throw Error('Unknown example');return structuredClone(dictionary.examples[id]);}
