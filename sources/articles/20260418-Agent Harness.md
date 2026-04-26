---
source: https://blog.qiaomu.ai/2026-04-18-JgypqM
title: Agent Harness：让AI从聊天机器人变成真正的智能体
fetch_time: 2026-04-26
tags: [AI Agent, Agent Harness, LLM, 工程实践]
---

你可能已经搭建过聊天机器人，甚至接入了几个工具，做出了能演示的原型。
但当你想把它推向生产环境时，问题就来了：模型会忘记三步之前做过什么，工具调用会失败，上下文窗口塞满了无用信息。

问题不在模型本身，而在模型周围的一切。

LangChain 用一个实验证明了这点：他们只改变了 LLM 的基础设施（模型和权重完全不变），在 TerminalBench 2.0 的排名就从 30 名开外跃升到第 5 名。

另一个研究项目让 LLM 自己优化基础设施，通过率达到 76.4%，超过了人工设计的系统。这套基础设施现在有了正式名称：**Agent Harness**。

## 什么是 Agent Harness

Harness 是包裹 LLM 的完整软件基础设施：编排循环、工具、记忆、上下文管理、状态持久化、错误处理和安全防护。

> "如果你不是模型，你就是 harness" — LangChain

**Agent** 是涌现出来的行为：那个有目标、会用工具、能自我纠错的实体。
**Harness** 是产生这种行为的"机械装置"。

Beren Millidge 的精确类比：原始 LLM 就像没有内存、没有硬盘、没有 I/O 的 CPU。上下文窗口 = RAM（快但有限），外部数据库 = 硬盘（大但慢），工具集成 = 设备驱动，Harness = 操作系统。

## 三层工程

- **提示词工程**：精心制作模型接收的指令
- **上下文工程**：管理模型看到什么、何时看到
- **Harness 工程**：涵盖前两者 + 整个应用基础设施

## 生产级 Harness 的 12 个组件

1. 编排循环（Orchestration Loop）— TAO/ReAct 循环
2. 工具（Tools）— 模式定义、注册、执行
3. 记忆（Memory）— 短期 + 长期
4. 上下文管理（Context Management）— 压缩、遮蔽、即时检索
5. 提示词构建（Prompt Construction）
6. 输出解析（Output Parsing）— 原生工具调用
7. 状态管理（State Management）— LangGraph 检查点/OpenAI Sessions
8. 错误处理（Error Handling）— 四种错误类型分级处理
9. 防护栏和安全（Guardrails and Safety）
10. 验证循环（Verification Loops）— 规则反馈、视觉反馈、LLM评判
11. 子智能体编排（Subagent Orchestration）
12. 持久化 & 生命周期管理

## 真实框架对比

| 框架 | 特点 |
|---|---|
| Claude Agent SDK | "哑循环"，所有智能在模型 |
| Claude Code | 收集-行动-验证循环 |
| OpenAI Agents SDK | "代码优先"，原生 Python |
| LangGraph | 显式状态图 |
| CrewAI | 基于角色的多智能体 |
| AutoGen | 对话驱动编排 |

## 七个核心架构决策

1. 单智能体 vs. 多智能体
2. ReAct vs. 计划-执行
3. 上下文窗口管理策略
4. 验证循环设计
5. 权限和安全架构
6. 工具范围策略
7. Harness 厚度（薄 harness vs. 显式控制）

## 关键洞察

> 下次你的 agent 失败时，别怪模型，看看 harness。

Harness 不是已解决的问题或商品层。这是艰苦工程所在：管理稀缺上下文、设计验证循环、构建连续性而不产生幻觉。

Manus 六个月内重建了五次，每次都删除了复杂性。领域正朝着更薄的 harness 发展——但 harness 本身不会消失。
