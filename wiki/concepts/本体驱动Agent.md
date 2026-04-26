---
title: Harness Engineering 本体驱动方案
description: 用 Ontology 为 Agent Harness 提供语义基础设施，实现约束来自业务结构而非工程配置
source: https://mp.weixin.qq.com/s/QBSYdyOtxnPmzpI26BnNWQ
author: 周士雄（悦点科技 研发负责人）
tags: [AI Agent, Harness Engineering, Ontology, Agent可控性, 本体建模, 语义底座]
related_to: [[Agent Harness]] [[AI数据基础设施重塑]]
created: 2026-04-26
---

# Harness Engineering 本体驱动方案

## Overview

周士雄（悦点科技）提出核心命题：2025-2026 年 Agent 进入企业后，问题高度相似——「自信地做错事」。根本原因是 Agent 缺少「懂规矩的结构」。

解决方案：用 **Ontology（本体）** 为 Harness 提供语义基础设施，使约束直接来自业务结构本身，而非工程配置。

## Key Claims

- **Problem**：规则是「外加的」，语义是「隐式的」，合规依赖模型对规则的理解，而模型理解本身不可靠
- **Solution**：约束不来自工程配置，而来自业务结构本身——不是「围栏」，而是「内建骨架」
- **执行时机**：约束发生在 Agent 输出之后、操作落地之前，与本体比对后打回重推，不静默放行
- **本体 vs 知识图谱**：本体 + Action + Logic，把静态知识描述变成可执行的业务规范
- **三支柱协同**：架构约束 + 上下文工程 + 反馈闭环，完整闭环而非工程拼接

## 上下文工程：重构记忆方式

| 传统方式 | 本体驱动 |
|---|---|
| 线性文本堆叠 | 可查询的语义子图 |
| 全量注入上下文 | 精准检索，动态注入 |
| 信息过期/冲突难处理 | 统一语义网络，一致性保障 |
| 每场景独立重组织 | 跨任务复用「业务地图」 |

## 反馈闭环

- **硬约束**：本体直接校验（规则可形式化）
- **软约束**：LLM 评估 + 人工审核节点（互补而非互斥）
- **本体进化**：Agent 执行数据反哺本体，识别未覆盖概念和频繁出错位置
- **可解释性**：每次校验有明确结构依据，可追溯到具体规则节点

## 系统架构：Knora 三层

```
用户任务
    ↓
认知引擎：从本体抽取相关知识注入上下文
    ↓
Agent：在既定义业务地图中推理和执行
    ↓
认知引擎：本体约束校验
    ↓
通过 → 输出 | 不通过 → 打回重推 + 结构化错误报告
```

## 五大元模式（本体层）

- **Entity**：业务对象（工单、设备、人员）
- **Relation**：实体间语义连接
- **Event**：有意义的业务状态变化
- **Action**：可执行操作，含触发条件和参数约束
- **Logic**：DAG 编排引擎定义的执行流程

## Related

- [[Agent Harness]] — 同系列前篇：Harness 的 12 个组件，纯技术视角
- [[AI数据基础设施重塑]] — 数据侧视角：Agent 成为数据首要消费者，需要适配的数据平台

## Sources

- [原文：Harness Engineering 的语义底座](https://mp.weixin.qq.com/s/QBSYdyOtxnPmzpI26BnNWQ)，周士雄 @ DataFunSummit
