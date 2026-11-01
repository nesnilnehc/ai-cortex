import {dictionary} from './locale.mjs?v=project-owned-release-20261101';
export function getExample(id){if(!Object.hasOwn(dictionary.examples,id))throw Error('Unknown example');return structuredClone(dictionary.examples[id]);}
