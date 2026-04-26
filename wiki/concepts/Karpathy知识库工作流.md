---
title: Karpathy LLM Wiki 工作流
description: Andrej Karpathy 的 LLM 知识库编译工作流
source: https://x.com/karpathy/status/2039805659525644595
created: 2026-04-12
tags: [LLM, 知识管理, Obsidian, 工作流, AI]
related_to: [[Andrej Karpathy博客]] [[index|🏠 回到索引]]
---

# Karpathy LLM Wiki 工作流

## 核心工作流

```
原始数据
  ↓
LLM 增量"编译"成 Markdown Wiki
 （摘要 + 反向链接 + 概念文章）
  ↓
Obsidian 前端
  ↓
LLM Agent 做 Q&A / Lint / 健康检查
  ↓
输出回流 Wiki
```

## 各环节说明

### 1. 原始数据 → LLM 增量编译
将原始文档（PDF、网页、笔记等）交给 LLM 处理，LLM 提取：
- **摘要**：核心要点提炼
- **反向链接**：与其他概念的相关性
- **概念文章**：结构化知识沉淀

### 2. Obsidian 前端
用 Obsidian 作为知识库的展示和浏览界面，利用其双向链接和图谱视图。

### 3. LLM Agent Q&A / Lint / 健康检查
Agent 定期扫描 Wiki，检查：
- **Q&A**：用问答方式验证知识正确性
- **Lint**：检查格式规范、链接完整性
- **健康检查**：反向链接是否完整、是否有孤立页面

### 4. 输出回流 Wiki
检查结果写回 Wiki，持续迭代优化。

---

## 与我们当前架构的对比

| 环节 | Karpathy 方案 | 我们现状 |
|------|--------------|---------|
| 原始数据 | 各种文档 | XHS + 网页 |
| LLM 编译 | Claude Code 自动化 | obsidian-ingest skill |
| Wiki 前端 | Obsidian | Obsidian ✓ |
| Q&A Agent | LLM Agent | 待建设 |
| Lint/健康检查 | LLM Agent | 待建设 |

---

## 待建设环节

我们已有的：Obsidian Vault + XHS ingest 链路

**缺失的：**
- Q&A Agent（定期用 LLM 验证 Wiki 知识正确性）
- Lint/健康检查 Agent（检查链接完整性、格式规范）
- 反向链接自动发现（目前手动维护 `related_to`）

**关联主题：** 一致性维度（[[一致性维度]]）虽然是数据工程内容，但其"维度版本化管理"思路与 Wiki 知识版本化相通。

---

## 参考文献

- [[Andrej Karpathy博客|Karpathy Blog]] — Karpathy 本人博客
- [Reddit 讨论：Implemented Karpathy's LLM Wiki Workflow](https://www.reddit.com/r/ObsidianMD/comments/1sdbq01/implemented_karpathys_llm_knowledge_base_workflow/)
- [MindStudio: What Is Andrej Karpathy's LLM Wiki?](https://www.mindstudio.ai/blog/andrej-karpathy-llm-wiki-knowledge-base-claude-code/)
