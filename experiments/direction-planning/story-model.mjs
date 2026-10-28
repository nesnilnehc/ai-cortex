import {stages,findSkills,getGateState} from './workflow.mjs?v=topic-local-branches';
export const chapterIds=Object.freeze(['research','planning','design','build','quality','commit','release']);
const chapters={
 research:{label:'问清楚',title:'先找到真正的问题。',body:'用户说：“我找不到以前提过的请求。”先看看哪里难用，再决定值不值得改。',result:'弄清谁遇到什么问题。',alt:'放大镜正在查看一叠用户请求，表示先理解真实问题。',tile:0},
 planning:{label:'定方向',title:'目标帮助判断，计划可以调整。',body:'目标是让用户找到历史请求。搜索和提醒都可以考虑，这次先做条件就绪的搜索。',result:'知道为什么做，以及先做哪件事。',alt:'图钉落在目标上，旁边的卡片通过连线关联，表示目标连接工作。',tile:1},
 design:{label:'说清楚',title:'说明和实现，要相互核对。',body:'搜索哪些内容？没有结果时怎么办？动手前，把这些问题讲清楚，再检查有没有遗漏。',result:'留下可以照着做、照着检查的说明。',alt:'纸上的设计草图与直尺，表示把预期行为说清楚。',tile:2},
 build:{label:'做出来',title:'把想法做成能用的东西。',body:'在项目里写代码、补测试，再实际运行，看看能不能找到想要的请求。',result:'得到可运行的改动和检查记录。',alt:'一台笔记本电脑和扳手，表示在项目中实施并运行改动。',tile:3},
 quality:{label:'检查好',title:'边做边检查，有问题再修。',body:'代码有没有问题？是不是做了原本要做的事？实际用起来行不行？这三件事都要看。',result:'分别留下代码、功能和实际运行的依据。',alt:'放大镜查看带勾选记录的检查单，表示核对质量与实际结果。',tile:4},
 commit:{label:'存一版',title:'把这次改动，清楚地存一版。',body:'只存这次相关的改动，写清楚改了什么、为什么改。需要时，再把分支整合到主线。',result:'形成便于别人理解和检查的提交。',alt:'用夹子固定的整齐版本纸叠和文件夹，表示保存清楚的改动版本。',tile:5},
 release:{label:'交出去',title:'让用户真的用上它。',body:'准备发布材料，按项目约定发布，再告诉用户哪里变了。发布后还要听听：现在好找了吗？',result:'拿到真实发布结果，继续观察是否有用。',alt:'两只手传递完成的卡片，旁边有一架橙色纸飞机，表示交付并获取反馈。',tile:6}
};
const groupLabels={research:'先了解问题',planning:'方向、目标与计划',design:'动手前检查说明',build:'测试与本地运行',quality:'代码审查与修复',commit:'提交与分支整合',release:'发布与公告',foundation:'让项目更好协作',collaboration:'与别人交换信息'};
export function getChapter(id){if(!Object.hasOwn(chapters,id))throw Error('Unknown chapter');return structuredClone(chapters[id]);}
export function getSimpleGate(id){
 const gate=getGateState(id);
 const copy={missing:{title:'还缺一次实际检查。',body:'代码看起来没问题，还不能说明用户真的能找到记录。先补上实际检查的依据。'},fail:{title:'有问题，回去修一修。',body:'先修好发现的问题，再检查受影响的地方。不能忽略失败就交给别人。'},pass:{title:'这组检查通过了。',body:'这里仅假设适用检查已完成。是否保存、整合或发布，还要分别核对本次操作的范围与前提。'}};
 return {...structuredClone(copy[id]),checksComplete:id==='pass',checks:[gate.engineering,gate.alignment,gate.verification]};
}
export function getToolGroups(query=''){
 const matches=findSkills({query});
 return stages.map(stage=>({id:stage.id,title:groupLabels[stage.id],skills:matches.filter(skill=>stage.skills.includes(skill.id))})).filter(group=>group.skills.length>0);
}
