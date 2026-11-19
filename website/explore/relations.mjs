import {dictionary} from './locale.mjs?v=presentation-video-20261119';
export function getExample(id){if(!Object.hasOwn(dictionary.examples,id))throw Error('Unknown example');return structuredClone(dictionary.examples[id]);}
