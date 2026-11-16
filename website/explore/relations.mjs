import {dictionary} from './locale.mjs?v=roadmap-grouping-20261116';
export function getExample(id){if(!Object.hasOwn(dictionary.examples,id))throw Error('Unknown example');return structuredClone(dictionary.examples[id]);}
