import {dictionary} from './locale.mjs?v=roadmap-delivery-20261113';
export function getExample(id){if(!Object.hasOwn(dictionary.examples,id))throw Error('Unknown example');return structuredClone(dictionary.examples[id]);}
