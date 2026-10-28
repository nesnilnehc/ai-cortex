import {stages} from './workflow.mjs?v=topic-local-branches';
export const relations=Object.freeze([
 {id:'goals-work',from:'direction',to:'work',type:'guidance',label:'方向与目标帮助判断哪些工作值得做'},
 {id:'planning-design',from:'planning',to:'design',type:'loop',label:'计划与需求说明相互核对，发现缺口可以返回修改'},
 {id:'design-build',from:'design',to:'build',type:'loop',label:'实现依据说明，发现遗漏再补充并复核'},
 {id:'build-quality',from:'build',to:'quality',type:'loop',label:'边做边验证，发现问题后定向修复并复核'},
 {id:'quality-planning',from:'quality',to:'planning',type:'loop',label:'发现做偏或条件变化时重新审视安排'},
 {id:'commit-ready',from:'commit-checks',to:'commit',type:'prerequisite',label:'保存本次改动前，核对范围、暂存差异与适用检查'},
 {id:'release-ready',from:'release-checks',to:'publish',type:'prerequisite',label:'发布前核对材料、必要检查和本次授权'},
 {id:'published-announcement',from:'published-result',to:'announce',type:'prerequisite',label:'公告依据实际发布结果'},
 {id:'user-feedback',from:'users',to:'work',type:'feedback',label:'用户反馈可以带回新问题，也可以让我们重新审视目标'},
 ...['research','foundation','collaboration'].map(id=>({id:`anytime-${id}`,from:id,to:'work',type:'anytime',label:'遇到需要时调用，不必等某个阶段结束'}))
].map(x=>Object.freeze(x)));
const prerequisites={commit:['本次范围清楚','审阅暂存差异','适用检查已满足'],publish:['发布包就绪','必要检查通过','本次发布已获授权'],announce:['实际发布结果','沟通范围与发送授权明确']};
export function getPrerequisites(id){if(!Object.hasOwn(prerequisites,id))throw Error('Unknown operation');return [...prerequisites[id]];}
export function getMapCoverage(){return [...new Set(stages.flatMap(stage=>stage.skills))];}
export function getExample(id){
 const examples={
  overview:{focus:'planning',edges:[],title:'不必排队，按需要配合。',body:'方向提供依据；工作可以反复调整。保存、发布和公告分别核对自己的前提。'},
  bug:{focus:'quality',edges:['build-quality'],title:'检查发现代码问题。',body:'回到实现修复，再复核受影响的检查。开发过程中可以多次验证，也可以多次保存清楚的改动。'},
  requirements:{focus:'design',edges:['planning-design','design-build'],title:'已有需求遗漏了搜索范围。',body:'Agent 可以先直接追问并补充需求文档。需要统一文档内容或系统复核时，再参考规范、规则或审查技能；不必让所有工作重新排队。'},
  release:{focus:'release',edges:['release-ready','published-announcement'],title:'准备把改动交给用户。',body:'先看发布包、必要检查和授权。拿到实际发布结果，再据此准备公告；一次提交不能代替这些依据。'}
 };
 if(!Object.hasOwn(examples,id))throw Error('Unknown example');return structuredClone(examples[id]);
}
