---
created: 2026-04-27
source: https://www.cnblogs.com/cczlovexw/p/19695231
tags: [AI, Agent, Anthropic, 工程实践]
---

# Anthropic Agent 工程实战指南

## Overview

基于 Anthropic 官方 15 篇 Agent 工程博客的系统梳理，涵盖从 Agent 基础架构、工具开发、上下文管理、长任务执行、多智能体协作到生产环境评测与安全的全流程知识体系。所有经验来自 Anthropic 生产环境的实战沉淀。

## Key Claims

- Agent 与工作流的核心区别：工作流执行路径固定可预判，Agent 动态自主决策
- 构建 Agent 应始终从最简单方案起步，仅当复杂度带来可证明效果提升时才增加复杂度
- 三大高级工具调用特性（工具搜索工具、程序化工具调用、工具使用示例）可分别解决上下文溢出、执行效率低下、调用准确率不足的瓶颈
- Agent 上下文是宝贵资源，精良的工具设计比更多工具更重要
- Agent 安全的核心矛盾是安全与自治性的平衡，沙箱隔离是核心方案

## Related

- [[agent-harness]] — Agent 外围系统的设计
- [[harness-engineering-ontology]] — 本体驱动的 Agent 可控执行
- [[ai-agents-data-infrastructure]] — AI Agents 与数据基础设施

## Sources

- [Anthropic Agent 工程实战指南](https://www.cnblogs.com/cczlovexw/p/19695231)
