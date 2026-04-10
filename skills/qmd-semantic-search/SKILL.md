---
name: qmd-semantic-search
description: 本地语义搜索 Obsidian 笔记库。使用 QMD（本地 GGUF 向量模型）对笔记进行语义检索，支持语义搜索、关键词搜索和混合重排序三种模式。
homepage: https://github.com/tobi/qmd
---

# QMD 语义搜索

基于 QMD 的本地语义搜索引擎，为 Obsidian Vault 提供语义搜索能力。

## Vault 路径

- Obsidian Vault: `~/obsidian-vault`

## 可用命令

### 1. 语义搜索（推荐）
```bash
qmd vsearch "自然语言查询" --limit 10
```
使用向量嵌入进行语义相似度搜索，适合理解意图的查询。

### 2. 关键词搜索
```bash
qmd search "精确关键词" --limit 10
```
使用 BM25 算法进行关键词匹配。

### 3. 混合搜索（最精准）
```bash
qmd query "查询" --limit 10
```
结合向量搜索 + BM25 + LLM 重排序，质量最高但速度最慢。

### 4. 列出笔记
```bash
qmd list
```

## 使用场景

当用户询问以下问题时使用：
- "我之前在 Obsidian 里存的那个 XXX 文档在哪"
- "我有没有关于 XXX 的笔记"
- "搜索我的笔记库 XXX 相关内容"
- "我记得以前看过一个关于 XXX 的文章"

## 注意事项

- embed 需要先完成（首次运行会自动下载模型，约 300MB）
- 搜索前检查 embed 状态：`qmd list`
- 如果索引不存在，先运行 `qmd embed`
