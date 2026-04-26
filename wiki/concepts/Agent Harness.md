---
title: Agent Harness
description: LLM 智能体的软件基础设施层，涵盖编排循环、工具、记忆、上下文管理等 12 个核心组件
source: https://blog.qiaomu.ai/2026-04-18-JgypqM
tags: [AI Agent, Agent Harness, LLM, 工程实践, 架构]
related_to: [[Karpathy知识库工作流]] [[AI高质量数据集]]
created: 2026-04-26
---

# Agent Harness

## Overview

Agent Harness 是包裹在 LLM 外围的完整软件基础设施层，是让 AI 从"聊天机器人"进化为"真正智能体"的关键。

**核心公式**：如果你不是模型，你就是 harness（LangChain）。

LLM 本身像没有内存/硬盘/I/O 的裸 CPU——上下文窗口是 RAM（快但有限），外部数据库是硬盘（大但慢），工具集成是设备驱动，而 **Harness 就是操作系统**。

LangChain 仅通过改进 harness（模型和权重完全不变），在 TerminalBench 2.0 从 30 名跃升至第 5 名——证明问题不在模型本身。

## Key Claims

- **Harness vs. Agent 区分**：Agent 是涌现的行为，Harness 是产生该行为的机械装置。"做 Agent"实际上是在做 Harness
- **三层工程**：提示词工程 → 上下文工程 → Harness 工程（逐层包含）
- **12 个生产组件**：编排循环、工具、记忆、上下文管理、提示词构建、输出解析、状态管理、错误处理、防护栏、验证循环、子智能体编排、生命周期管理
- **上下文腐烂**：关键内容落在窗口中间时性能下降 30%+
- **协同进化**：模型改进 → harness 复杂性降低，但 harness 本身不会消失
- **薄 harness 赌注**：Anthropic 押注模型进步，框架押注显式控制

## Architecture: 7 个核心决策

| # | 决策 | 关键权衡 |
|---|---|---|
| 1 | 单 vs. 多智能体 | 仅工具过载 >10 个或任务域明显独立时才拆分 |
| 2 | ReAct vs. 计划-执行 | LLMCompiler 比顺序 ReAct 快 3.6× |
| 3 | 上下文窗口策略 | 5 种：清除/总结/遮蔽/笔记/委托 |
| 4 | 验证循环设计 | 规则反馈 vs. LLM 评判 |
| 5 | 权限安全架构 | 宽松（快但风险）vs. 限制性（安全但慢）|
| 6 | 工具范围策略 | 更多工具 ≠ 更好性能 |
| 7 | Harness 厚度 | 薄（Harness 少）vs. 显式控制 |

## 框架横向对比

- **Claude Agent SDK**：哑循环，所有智能在模型
- **Claude Code**：收集-行动-验证循环，git 提交作检查点
- **OpenAI Agents SDK**：代码优先，Python 原生
- **LangGraph**：显式状态图
- **CrewAI**：角色型多智能体
- **AutoGen**：对话驱动，三层架构

## Related

- [[Karpathy知识库工作流]] — 知识管理方法论，AI 辅助工作流
- [[AI高质量数据集]] — 数据工程侧，模型能力的基础

## Sources

- [原文：Agent Harness：让AI从聊天机器人变成真正的智能体](https://blog.qiaomu.ai/2026-04-18-JgypqM)
