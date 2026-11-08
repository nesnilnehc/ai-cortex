import {dictionary} from './locale.mjs?v=plan-next-16-20261108';
export function getExample(id){if(!Object.hasOwn(dictionary.examples,id))throw Error('Unknown example');return structuredClone(dictionary.examples[id]);}
