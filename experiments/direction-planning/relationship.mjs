import {getPlan} from './model.mjs';
const nodes={
 direction:{title:'项目方向',question:'为什么做？希望带来什么改变？',input:'项目服务的用户、核心问题、已有使命与愿景。',output:'使命、愿景与衡量核心价值的北极星指标。',boundary:'方向和指标为后续判断提供依据；不直接决定某项功能的优先级，也不强制重写已有方向。',example:'使命：让团队可靠地处理服务请求。愿景：每个请求都可追踪。北极星指标候选：每周被可靠处理的有效请求数（示例，无实测值）。',skills:['define-mission','define-vision','define-north-star']},
 goals:{title:'目标与战略主题',question:'要取得什么结果？',input:'方向、核心价值指标、已有战略主题与现实约束。',output:'可判断是否达成的目标；需要时用战略主题组织长期投入。',boundary:'目标描述结果，战略主题描述持续投入方向；目标不等于功能清单。已有目标可直接复用，缺少上游时仅提出有依据的候选。',example:'主题：可靠服务、信息可达、持续运营。G1：避免重复提交；G2：让用户找到历史请求；G3：让团队复用处理结果。仅展开其中一条关系，不代表完整战略方案。',skills:['define-strategic-pillars','design-strategic-goals']},
 backlog:{title:'待办池 · Backlog',question:'哪些需求和问题值得考虑？',input:'目标引导的想法，以及用户反馈、真实需求和缺陷。',output:'有稳定编号、来源和预期结果的需求或缺陷记录，并关联所支持的目标。',boundary:'待办不全是从目标向下拆出来的，也会从真实问题进入。登记不代表批准执行；需求修复只在已有审查发现且范围获授权时进行。',example:'G1 → BUG1 重复提交；G2 → R1 搜索、R3 提醒；G3 → R2 导出。所有演示记录都保留在池中，尚未安排的工作也有位置。',skills:['capture-work-items','orchestrate-repair-requirements-loop']},
 choices:{title:'取舍与就绪条件',question:'什么重要？下一步能开始吗？',input:'需求与缺陷、项目优先级政策、依赖证据、容量及已有决定。',output:'重要程度和理由，以及下一步的依赖、阻塞与就绪依据。',boundary:'重要程度与就绪程度分别判断。P1 不意味着立即开始；优先沿用已确认政策和决定，不无故对全部事项重新评分。',example:'R1 搜索为 P1，但依赖检索接口。接口延期时仍为 P1，开始条件变为“等待就绪依据”。',skills:['prioritize-backlog','map-item-dependencies']},
 roadmap:{title:'路线图',question:'先推进什么？如何组织交付？',input:'目标、已有优先级、就绪条件、已确定的范围与时间承诺。',output:'解释安排的主路线图；按项目需要选择迭代、版本、时间线和里程碑视图。',boundary:'路线图表达选择与安排，不代替完整 backlog。Now / Next / Later 是一种安排视图，日期、迭代和版本不能互相冒充；纳入不等于批准执行。',example:'主视图回答方向与先后；版本视图回答哪些一起交付；迭代回答本周期追求什么；时间线回答时间与关键事件。只启用有依据且有用的视图。',skills:['define-roadmap','promote-roadmap-items']},
 feedback:{title:'反馈与调整',question:'做完后有用吗？变化影响了什么？',input:'实际进展、验收和发布证据、用户反馈与指标观察。',output:'状态与日期更新、保留原因的变更记录，以及符合条件的归档。',boundary:'开发完成、验收通过、发布和目标达成分别核实。完成证据不自动证明用户价值；发现目标不再合适时，提出重新审视的建议。',example:'接口延期 → 复核依赖与计划。验收完成 → 维护状态，另查发布依据。用户仍找不到记录 → 回看 G2 与新的需求，而不只是移动看板卡片。',skills:['update-roadmap','archive-milestone']},
 help:{title:'不知道从哪里开始？',question:'先找缺口，再做适用的工作。',input:'项目现状、现有资料，以及用户本次授权的工作范围。',output:'下一步建议；或一项核实后的治理行动；或一轮按需组织的路线图规划。',boundary:'这是帮助选择与推进工作的入口，不是每个节点之前都必须走的步骤。路线图编排按范围调用步骤，不自动重建使命、愿景或整个战略层。',example:'plan-next：诊断并建议；orchestrate-governance-step：核实后推进一项治理行动；orchestrate-roadmap-planning：组织已授权的路线图工作。',skills:['plan-next','orchestrate-governance-step','orchestrate-roadmap-planning']}
};
const goals={
 all:{id:'ALL',title:'全部工作',outcome:'服务请求可靠、可查、可复用',metric:'示例关注：有效请求处理情况；此处没有实测指标。'},
 reliable:{id:'G1',title:'可靠提交',outcome:'避免同一次操作产生重复请求',metric:'验证时观察重复请求与提交失败；修复验收不等于该目标已达成。'},
 find:{id:'G2',title:'找到记录',outcome:'用户能找到自己需要的历史请求',metric:'验证时观察查找成功情况；上线搜索功能不等于查找问题已解决。'},
 reuse:{id:'G3',title:'复用结果',outcome:'团队能复用已经处理的请求记录',metric:'验证时观察导出结果的实际使用；有导出按钮不等于产生用户价值。'}
};
const membership={BUG1:'reliable',BUG2:'reliable',R1:'find',R3:'find',R2:'reuse'};
export function getRelationship(key){if(!Object.hasOwn(nodes,key))throw Error('Unknown relationship');return structuredClone(nodes[key]);}
export function getCoverage(){return [...new Set(Object.values(nodes).flatMap(node=>node.skills))];}
export function getTrace(goal,event='base'){
 if(!Object.hasOwn(goals,goal))throw Error('Unknown goal');
 const plan=getPlan(event);
 return {goal:structuredClone(goals[goal]),items:plan.items.filter(item=>goal==='all'||membership[item.id]===goal)};
}
