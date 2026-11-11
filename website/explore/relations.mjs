import {dictionary} from './locale.mjs?v=product-requirement-skills-20261111';
export function getExample(id){if(!Object.hasOwn(dictionary.examples,id))throw Error('Unknown example');return structuredClone(dictionary.examples[id]);}
