import {dictionary} from './locale.mjs?v=video-production-skills-20261125';
export function getExample(id){if(!Object.hasOwn(dictionary.examples,id))throw Error('Unknown example');return structuredClone(dictionary.examples[id]);}
