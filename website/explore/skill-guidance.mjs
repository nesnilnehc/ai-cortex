export {getSkillGuidance} from './locale.mjs?v=aic04-host-1';
import metadata from './skill-metadata.json?v=aic04-host-1' with {type:'json'};
export const guidanceIds=Object.freeze(Object.keys(metadata.skills));
