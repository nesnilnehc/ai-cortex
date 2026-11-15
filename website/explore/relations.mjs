import {dictionary} from './locale.mjs?v=archive-milestone-20261115';
export function getExample(id){if(!Object.hasOwn(dictionary.examples,id))throw Error('Unknown example');return structuredClone(dictionary.examples[id]);}
