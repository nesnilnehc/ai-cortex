import {dictionary} from './locale.mjs?v=skill-design-audit-20261120';
export function getExample(id){if(!Object.hasOwn(dictionary.examples,id))throw Error('Unknown example');return structuredClone(dictionary.examples[id]);}
