---
title: AI Agents 与数据基础设施重塑
description: AI Agents 如何从五个维度重塑数据基础设施，以及统一数据控制平面架构
source: https://mp.weixin.qq.com/s/XOMnWsmwBZCi_2_Ux5KblA
author: 堵俊平（Datastrato 创始人兼 CEO）
tags: [AI Agent, 数据基础设施, Agentic AI, 元数据, DataOps]
related_to: [[agent-harness]] [[ai-high-quality-dataset]]
created: 2026-04-26
---

# AI Agents 与数据基础设施重塑

## Overview

AI Agents 正在从"回答问题"进化到"执行任务"，并开始接管数据系统的操作权限。堵俊平在 DataFunSummit 提出核心命题：**Agents are becoming the new software operators**，而数据基础设施是为人类编写 SQL 设计的，不是为 Agents 操作系统的——这成为隐藏的瓶颈。

## Key Claims

- **演进三阶段**：LLM 革命（2022）→ RAG 热潮（2024）→ AI Agents（2025）
- **架构根本转变**：Agent 直接调用标准化工具套件，直接访问数据层，完全绕过传统应用中间层
- **数据五大转变**：Agent 驱动访问 / 机器可读元数据 / 自主 DataOps / 多模态平台 / Agent 感知治理
- **元数据即大脑**：Metadata becomes the context layer for AI，Agent 依赖元数据理解数据含义和用法
- **统一数据控制平面**：连接多引擎（Spark/Trino/Flink/Ray），Lakehouse + Vector DB 存储
- **下一代特征**：Agent 原生 + 元数据驱动 + 多引擎 + 多模态

## 五大架构转变

| 维度 | 变化 |
|---|---|
| 数据消费者 | 人类 → AI Agents |
| 元数据 | 人类可读 → 机器可读 |
| DataOps | 人工运维 → 自主智能化 |
| 数据类型 | 结构化 → 结构化+向量+非结构化 |
| 数据治理 | 规则固定 → 适应自主系统 |

## 关键公式

> Agents spend most of their time interacting with data.
> 如果数据系统没有做好准备，Agent 的操作将是错误的、危险的、不安全的。

## Related

- [[agent-harness]] — 同一个故事的技术侧：Harness 是 LLM 的操作系统，本文是从数据侧看 Agent 如何重塑数据平台
- [[ai-high-quality-dataset]] — 数据工程侧，高质量数据集是 AI 能力的基石

## Sources

- [原文：当 OpenClaw 遇见数据](https://mp.weixin.qq.com/s/XOMnWsmwBZCi_2_Ux5KblA)，堵俊平 @ DataFunSummit
