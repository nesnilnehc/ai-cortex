const scenarios = {
 direction:{title:'先把方向说清楚',intro:'从项目现状出发，建立目标与日常工作的联系。',steps:['核对项目现状','提出目标与衡量依据','连接需求与目标'],focus:0,artifact:'目标草案',detail:'先核实项目服务谁、解决什么问题，再形成有依据的目标；需要你决定的方向保持为提案。',skills:['define-mission','define-vision','define-north-star','design-strategic-goals'],prompt:'请基于项目已有资料，梳理项目服务的用户、核心问题与阶段目标。区分事实和推断，给出目标与衡量依据草案；保留已确定的方向，列出需要我决定的取舍。'},
 backlog:{title:'让想法变成可解释的安排',intro:'重要程度、依赖条件和近期安排，放在一起看。',steps:['盘点需求与缺陷','应用优先级政策','检查依赖并安排'],focus:2,artifact:'路线图与安排依据',detail:'高优先级表示重要，进入 Now 还需要条件就绪。每个安排都能回答为什么，以及下一步缺什么。',skills:['orchestrate-roadmap-planning','prioritize-backlog','map-item-dependencies','promote-roadmap-items'],prompt:'请基于项目已有目标、需求和缺陷，整理一轮路线图规划。保留已确定的优先级与承诺，检查依赖与下一步条件，提出 Now / Next / Later 安排，列出缺失依据和需要我决定的取舍。'},
 existing:{title:'已有计划，从原处接着走',intro:'保留已有决定，让计划更容易阅读和核对。',steps:['找到现有计划与来源','核对结构和事实缺口','原处整理并复核'],focus:3,artifact:'对齐后的计划与缺口清单',detail:'沿用现有优先级、范围、承诺与链接。结构修复与新的业务取舍分别说明，不因整理而重新规划。',skills:['orchestrate-roadmap-planning','review-roadmap','define-roadmap'],prompt:'请检查并整理项目现有路线图，保留已有优先级、层级、范围、日期承诺和稳定链接。先列出结构问题与证据缺口，仅修复有依据的结构问题；新的业务取舍另列提案，不重新排序。'},
 change:{title:'变化发生后，看清影响',intro:'更新计划，也留下为什么改变的依据。',steps:['核对变化与事实依据','分析受影响的工作','更新计划并保留记录'],focus:4,artifact:'变更对照与调整记录',detail:'日期和状态变化进入维护；需要改变 Now / Next / Later 时另做安排决策。完成开发、通过验收和发布分别记录。',skills:['update-roadmap','map-item-dependencies','promote-roadmap-items','review-roadmap'],prompt:'项目计划发生变化，请先核对变化依据，分析受影响的需求、依赖与日期，给出调整前后对照。保留已确认承诺及变更原因；若需改变优先级或 Now / Next / Later 安排，单独列出待决定的提案。'}
};
const base=[
{id:'BUG1',name:'修复重复提交',priority:'P0',tier:'Now',state:'进行中',condition:'完成回归与验收',goal:'可靠地提交请求'},
{id:'R1',name:'搜索历史请求',priority:'P1',tier:'Now',state:'待开始',condition:'检索接口已就绪',goal:'更快找到请求'},
{id:'R2',name:'导出处理记录',priority:'P1',tier:'Next',state:'待开始',condition:'等待本轮容量释放',goal:'复用处理结果'},
{id:'R3',name:'请求进度提醒',priority:'P2',tier:'Later',state:'待评估',condition:'确认提醒需求与干扰成本',goal:'减少反复查询'}
];
export function getScenario(key){if(!Object.hasOwn(scenarios,key))throw Error('Unknown scenario');return structuredClone(scenarios[key]);}
export function getPlan(event){
 const items=structuredClone(base);
 let reason='先恢复提交可靠性，同时启动条件就绪的搜索。导出等待容量，提醒保留为后续评估。',changes=['基线计划：依据重要程度、依赖与现有容量安排。'];
 if(event==='urgent'){
 items.unshift({id:'BUG2',name:'修复请求无法提交',priority:'P0',tier:'Now',state:'待处理',condition:'优先恢复核心入口',goal:'可靠地提交请求'});
 items.find(x=>x.id==='BUG1').tier='Next'; items.find(x=>x.id==='BUG1').condition='紧急修复后恢复原工作'; items.find(x=>x.id==='R1').tier='Next'; items.find(x=>x.id==='R1').condition='接口已就绪，等待紧急修复释放容量';
 reason='核心入口故障优先恢复。演示假设本轮容量只能容纳紧急修复，原工作顺延；需由项目负责人确认。';
 changes=['新增 BUG2 → Now：提交入口不可用。','BUG1、R1：Now → Next；优先级保持不变。','这是安排提案，尚未替项目作出决定。'];
 }else if(event==='delay'){
 const item=items.find(x=>x.id==='R1'); item.tier='Next';item.state='受阻';item.condition='检索接口延期，等待新的就绪依据';
 reason='搜索依赖的检索接口延期，因此暂移至 Next。重要程度仍为 P1；依赖就绪后再评估进入 Now。';
 changes=['R1：Now → Next；P1 保持不变。','开始条件：接口已就绪 → 等待接口就绪依据。','相关交付日期需要复核；没有依据时不编造新日期。'];
 }else if(event==='complete'){
 const item=items.find(x=>x.id==='BUG1');item.state='验收通过';item.condition='演示依据：回归与验收记录；尚未发布';
 items.find(x=>x.id==='R2').tier='Now'; items.find(x=>x.id==='R2').condition='容量已释放，导出前提已核对';
 reason='重复提交修复已通过验收。演示假设容量释放、导出前提就绪，提出将导出纳入 Now；发布状态仍需独立证据。';
 changes=['BUG1：进行中 → 验收通过，保留原 Now 记录。','R2：Next → Now，依据容量释放与条件就绪。','验收通过不代表已发布。'];
 }else if(event!=='base')throw Error('Unknown event');
 return {items,reason,changes};
}
