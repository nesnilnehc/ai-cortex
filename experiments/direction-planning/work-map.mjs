/* One work relationship map with contextual help; no alternate perspective state. */
const labels={
  "label": "工作与配合",
  "point": "这项工作",
  "line": "怎样配合",
  "plane": "共同依据"
};
const help={
  "direction": {
    "point": "明确一个目标，说明希望带来什么改变。",
    "line": "把目标与候选工作联系起来，新证据也可以带回目标。",
    "plane": "让不同工作有共同的取舍依据，不必每次重定方向。"
  },
  "planning": {
    "point": "为候选事项判断优先级和推进条件。",
    "line": "连接目标、待办、依赖与路线图；变化时只调整受影响的安排。",
    "plane": "保留已有决定与承诺，让整轮规划有共同依据。"
  },
  "design": {
    "point": "审查一份已有需求，找出影响实施的缺口。",
    "line": "需求、设计、任务相互核对，发现遗漏就回到相应资料修订。",
    "plane": "让相关工作采用共同的文档结构和质量要求。"
  },
  "build": {
    "point": "运行适用测试，必要时补智能体测试或更新本地环境。",
    "line": "把获准任务、代码变更和实际运行结果连接起来。",
    "plane": "沿用项目测试与运行约定，减少交接时的重复猜测。"
  },
  "quality": {
    "point": "对当前改动做适用的工程审查或实现对齐检查。",
    "line": "发现问题后定向修复，再复核受影响的检查。",
    "plane": "工程质量、批准意图与实际验收各有依据，不能互相代替。"
  },
  "commit": {
    "point": "把范围清楚的改动保存为便于审阅的提交。",
    "line": "按需要整合分支，核对差异、检查和当前操作条件。",
    "plane": "让多人或多分支的工作可以清楚交接；提交不等于发布。"
  },
  "release": {
    "point": "准备并验证当前发布包，按授权执行发布或公告。",
    "line": "准备、实际发布与公告分别核对前提，反馈可以回到相关工作。",
    "plane": "让版本、交付事实和对外表达保持一致。"
  },
  "research": {
    "point": "针对一个问题核实来源，或评估已有研究支持的机会。",
    "line": "研究结论为机会判断、目标和候选工作提供依据。",
    "plane": "区分事实、推断与缺口，帮助团队形成有依据的取舍。"
  },
  "foundation": {
    "point": "补齐当前需要的文档入口、约定、自动化或凭据支持。",
    "line": "让人和智能体能找到并复用已有依据。",
    "plane": "形成持续可维护的项目基础，按需补齐而非强制初始化清单。"
  },
  "collaboration": {
    "point": "核实一次沟通的产品事实、共享范围或消息契约。",
    "line": "让文档、参与方和消息系统按具体约定交接。",
    "plane": "保留事实与授权边界，避免把一次沟通当成通用承诺。"
  }
};
const map={
  "nodes": {
    "direction": {
      "title": "方向与目标",
      "subtitle": "为什么做，希望有什么改变"
    },
    "planning": {
      "title": "待办与计划",
      "subtitle": "需求、缺陷与路线图"
    },
    "design": {
      "title": "把事情说清楚",
      "subtitle": "需求、设计和任务"
    },
    "build": {
      "title": "实现与运行",
      "subtitle": "边做边测，必要时修改"
    },
    "quality": {
      "title": "检查与修复",
      "subtitle": "代码、原意和实际结果"
    },
    "commit": {
      "title": "保存与整合",
      "subtitle": "可以多次保存，不等于发布"
    },
    "release": {
      "title": "发布给用户",
      "subtitle": "发布与公告分别核对"
    },
    "research": {
      "title": "研究与了解问题"
    },
    "foundation": {
      "title": "文档、约定与工具"
    },
    "collaboration": {
      "title": "沟通与交换信息"
    }
  },
  "edges": {
    "planning-design": "互相核对",
    "design-build": "补充说明",
    "build-quality": "修复后复核",
    "quality-planning": "重看安排"
  },
  "boundary": "围绕同一件工作，反复核对和调整",
  "center": "同一件工作",
  "centerDetail": "让用户找到历史请求",
  "guide": "提供判断依据",
  "feedback": "用户反馈：带回新问题，也可以重新审视目标",
  "support": "随时可用",
  "supportDetail": "遇到需要就用，不排在末尾",
  "delivery": "按本次需要，各自核对前提",
  "legend": [
    "↔ 来回核对和修改",
    "┄→ 先核对前提",
    "↶ 反馈可以改变目标与工作"
  ],
  "note": "看工作怎样配合：可以往返核对，每次操作各有前提。"
};
export function getHelpLabels(){return {...labels};}
export function getWorkHelp(id){
 if(!Object.hasOwn(help,id))throw new Error('Unknown work context');
 return {...help[id]};
}
export function getMapProjection(){return structuredClone(map);}
