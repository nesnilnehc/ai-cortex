import {dictionary} from './locale.mjs?v=opportunity-assessment-20261120';
export function getExample(id){if(!Object.hasOwn(dictionary.examples,id))throw Error('Unknown example');return structuredClone(dictionary.examples[id]);}
