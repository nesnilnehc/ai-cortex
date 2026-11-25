import {dictionary} from './locale.mjs?v=redeploy-local-3-4-1-20261125';
export function getExample(id){if(!Object.hasOwn(dictionary.examples,id))throw Error('Unknown example');return structuredClone(dictionary.examples[id]);}
