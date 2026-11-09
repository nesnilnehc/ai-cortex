import {dictionary} from './locale.mjs?v=plan-next-17-20261109';
export function getExample(id){if(!Object.hasOwn(dictionary.examples,id))throw Error('Unknown example');return structuredClone(dictionary.examples[id]);}
