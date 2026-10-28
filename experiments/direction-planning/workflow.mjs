import sourceCatalog from './catalog.json' with {type:'json'};
import {getCoverage} from './relationship.mjs';
export const catalog=Object.freeze(sourceCatalog.map(skill=>Object.freeze({...skill})));
const design=['orchestrate-repair-requirements-loop','review-requirements','review-functional-design','review-technical-design','review-tasks'];
const definitions=[
 {id:'research',title:'研究与机会',question:'这个问题值得投入吗？',outcome:'研究依据 → 机会判断',skills:['deep-research','market-research','competitive-research','policy-research','assess-product-opportunity','product-opportunity-analysis'],input:'开放问题、用户信号与已有研究。',output:'可追溯的研究结论、机会建议和证据缺口。',boundary:'研究提供事实，机会评估承接判断；不把未经核实的假设直接写成产品决定。',steps:['明确问题与范围','核实原始证据','形成机会建议'],prompt:'请基于已有资料研究这个问题，区分事实、推断与证据缺口，再给出是否值得继续投入的建议。不要替我决定未明确的产品取舍。'},
 {id:'planning',title:'方向与规划',question:'为什么做，先做什么？',outcome:'方向 → 目标 → 待办 → 路线图',skills:[...getCoverage().filter(id=>id!=='orchestrate-repair-requirements-loop'),'review-roadmap'],input:'项目现状、用户需求、已有方向与承诺。',output:'目标与工作之间的关系、有依据的优先级、依赖和路线图。',boundary:'已有资料直接复用；路线图纳入、执行批准、验收和发布保持区别。诊断与编排帮助选择步骤，不要求全链重做。',steps:['明确方向与目标','关联需求与缺陷','检查取舍与条件','形成并维护路线图'],prompt:'请根据项目现有方向、目标、需求与缺陷，整理一轮有依据的路线图规划，保留已确定的决定与承诺，列出需要我判断的取舍。'},
 {id:'design',title:'需求与设计审查',question:'想做的事说清楚了吗？',outcome:'已有需求与设计 → 审查发现',skills:design,input:'已有路线图、需求、功能设计、技术设计和任务资料。',output:'对应资料的审查发现与需要补充的依据。',boundary:'这里审查已有资料，不声称这些技能自动完成所有设计。需求和设计由项目工作流程形成；发现问题后回到相应资料修订并复核。',steps:['核对需求与计划','审查功能与技术设计','核对任务覆盖与条件'],prompt:'请审查本次变更已有的需求、设计和任务资料，指出影响实施的缺口并给出定位。只做适用范围的审查，不编造缺失的业务决定。'},
 {id:'build',title:'实施与验证',question:'改动能运行，行为正确吗？',outcome:'项目实现 → 测试与运行证据',skills:['automate-tests','scaffold-agent-tests','redeploy-local'],input:'获准实施的任务、现有代码、测试契约与项目工具。',output:'实际测试结果、必要的智能体测试套件，以及授权范围内的本地运行结果。',boundary:'写代码由当前智能体与项目工作流程完成；这里的技能提供测试与本地运行支持。生成测试、测试通过和生产验收不是同一件事。',steps:['按项目约定实施改动','按需补充智能体测试','运行实际检查','需要时更新本地环境'],prompt:'请依据已批准的任务实施并验证改动，按项目要求先写相关测试，运行适用检查并报告结果；需要本地重部署时先核实项目方式，未执行的检查明确列出。'},
 {id:'quality',title:'代码审查与修复',question:'实现可靠吗，也符合原意吗？',outcome:'工程检查 ＋ 功能核对 ＋ 运行证据',skills:[...catalog.filter(skill=>skill.id.startsWith('review-')&&!design.includes(skill.id)&&skill.id!=='review-roadmap').map(skill=>skill.id),'orchestrate-code-review','orchestrate-repair-loop'],input:'实际改动、批准的需求与设计，以及测试和验收证据。',output:'工程发现、功能对齐结论、运行检查结果；需要时进行有限轮次的修复与复核。',boundary:'工程审查与功能核对是并列检查，互相不能代替。语言、框架和质量专项按改动选择；审查通过也不能代替实际运行验收。',steps:['按改动选择审查范围','分别核对工程与功能','执行必要的验证','有问题则修复并复核'],prompt:'请对本次改动执行适用的工程审查，单独核对实现与批准意图的一致性，并运行必要的测试与验收检查。发现阻断问题时定向修复、复核受影响的检查，报告剩余限制。'},
 {id:'commit',title:'提交与整合',question:'如何把改动清楚地交付到主线？',outcome:'清晰提交 → 按需整合分支',skills:['commit-work','deliver-feature','integrate-branches'],input:'范围明确、经过适用验证的工作区改动，或待整合的分支。',output:'有逻辑边界与说明的提交；按授权选择单分支交付或多分支整合。',boundary:'提交不等于推送，整合不等于发布。单分支交付和多分支整合是不同入口，不必连续执行；实际写入和推送遵循当前授权。',steps:['核对变更范围与验证','审阅暂存差异','创建逻辑清晰的提交','按需选择分支整合方式'],prompt:'请检查本次改动与验证结果，按逻辑范围准备清晰的提交，审阅暂存差异后执行已授权的提交操作。若需要整合分支，先说明当前分支与可选入口；不要将提交视为已经发布。'},
 {id:'release',title:'发布与沟通',question:'能交给使用者了吗？',outcome:'发布包 → 发布回执 → 用户公告',skills:['prepare-release','publish-release','announce-release','changelog-video'],input:'明确的变更范围、项目版本政策与必要质量证据。',output:'可审阅的发布材料包；授权发布后的实际回执；基于已发布事实的公告。',boundary:'准备、发布和公告分别负责。视频是可选发布材料，不是强制步骤；没有实际发布回执不能声称已经发布。',steps:['准备并验证发布包','按需生成变更视频','授权后执行发布','依据已发布事实沟通'],prompt:'请先根据项目约定准备本次发布材料，核对版本、范围、验证与可选材料，报告是否就绪。正式发布和公告发送需遵循已有授权；未发布时不要生成虚假的发布成功结论。'},
 {id:'foundation',title:'项目基础与知识',question:'怎样让后续工作有共同依据？',outcome:'约定 · 文档 · 自动化 · 凭据支持',skills:['define-docs-norms','generate-agent-entry','generate-standard-readme','generate-github-workflow','refine-skill-design','manage-secret'],input:'项目现状、已有约定和具体维护目标。',output:'文档规范、智能体入口、README、工作流或经审查的技能；按需提供个人凭据管理支持。',boundary:'这些能力贯穿各阶段，按问题调用；不构成每个项目都必须先完成的初始化清单。此原型不收集或展示真实凭据。',steps:['复用现有约定','补齐当前缺口','核对入口与使用方式'],prompt:'请检查项目现有约定与入口，仅补齐影响当前工作的规范、文档或自动化缺口，保留权威来源和已确定的选择。'},
 {id:'collaboration',title:'沟通与系统集成',question:'如何把事实清楚地传给别人？',outcome:'产品事实 · 可独立理解的表达 · 契约消息',skills:['prepare-presales-response','decontextualize-text','publish-nats-message','consume-nats-message'],input:'产品证据、需要分享的内容，或已经约定的消息契约。',output:'有依据的售前材料、去除内部依赖的表达，或符合契约的消息处理结果。',boundary:'这些是独立适用的工作入口，不是每次发布之后都要发送消息。外部发送和写入按实际授权执行；原型不连接消息系统。',steps:['核实事实与共享范围','选择文档或消息契约','在授权范围交付并核对'],prompt:'请依据现有产品事实或消息契约准备本次沟通，区分可复用事实与本次特定条件，保留证据来源。发送消息或写入外部系统只按本次明确授权执行。'}
];
export const stages=Object.freeze(definitions.map(stage=>Object.freeze({...stage,skills:Object.freeze([...stage.skills]),steps:Object.freeze([...stage.steps])})));
export function getStage(id){const stage=stages.find(stage=>stage.id===id);if(!stage)throw Error('Unknown stage');return structuredClone(stage);}
export function findSkills({query='',stage='all'}={}){
 const scope=stage==='all'?null:new Set(getStage(stage).skills);
 const term=query.trim().toLocaleLowerCase();
 return catalog.filter(skill=>(!scope||scope.has(skill.id))&&`${skill.id} ${skill.purpose} ${skill.description}`.toLocaleLowerCase().includes(term));
}
export function getGateState(id){
 const states={
  pass:{engineering:'无阻断发现',alignment:'与批准意图一致',verification:'必要检查已通过',mayProceed:true,title:'可以准备提交',note:'演示假设适用检查均已完成。接下来核对提交范围；提交不代表已经整合或发布。'},
  fail:{engineering:'存在阻断发现',alignment:'修复后重新核对',verification:'相关检查未通过',mayProceed:false,title:'回到实现，修复后再核对',note:'修复工程或功能问题后，重跑受影响的检查。不能靠忽略失败或弱化断言进入提交。'},
  missing:{engineering:'无阻断发现',alignment:'尚未完成核对',verification:'缺少验收证据',mayProceed:false,title:'补充依据，不能声称已验证',note:'即使工程审查没有发现问题，也不能推断实现符合原意，或用户流程已经通过验收。'}
 };
 if(!Object.hasOwn(states,id))throw Error('Unknown gate state');return structuredClone(states[id]);
}
