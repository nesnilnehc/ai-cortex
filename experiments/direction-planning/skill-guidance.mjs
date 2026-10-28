import guidance from './skill-guidance.json' with {type:'json'};

// Localized explanations supplement the defining skills; they do not execute them.
export const guidanceIds=Object.freeze(Object.keys(guidance));
export function getSkillGuidance(id){
 if(!Object.hasOwn(guidance,id))throw new Error(`Unknown skill: ${id}`);
 return structuredClone(guidance[id]);
}
