---
name: daily-report
description: AI 日报生成器。每天自动总结当日热点新闻（AI + 理财方向）、工作成果、经验教训，并生成飞书文档发送给自己。每周一到周五 18:00 自动执行。触发场景：(1) 每天 18:00 自动运行 (2) 用户要求生成日报 (3) 总结工作时
---

# 日报 Skill

## 工作流程

### 1. 搜集信息

**AI 新闻：**
```bash
# 使用 Tavily 或 multi-search 搜索今日 AI 热点
python3 ~/.openclaw/workspace/skills/openclaw-tavily-search/scripts/tavily_search.py \
  --query "AI 人工智能 2026年3月 最新进展" \
  --max-results 5 --format md

# GitHub Trending AI 项目
curl -s "https://api.github.com/search/repositories?q=created:$(date +%Y-%m-%d)&sort=stars&order=desc" \
  | python3 -c "import json,sys; d=json.load(sys.stdin); [print(f'- {r[\"full_name\"]}: {r[\"description\"]} ⭐{r[\"stargazers_count\"]}') for r in d.get('items',[])[:5]]"
```

**理财新闻：**
```bash
# 搜索今日金融市场热点
python3 ~/.openclaw/workspace/skills/multi-search-engine/scripts/multi_search.py \
  --engine baidu --query "今日A股 理财 市场热点 2026-03-22"
```

### 2. 读取今日工作记录

```bash
# 读取今日 memory
cat ~/.openclaw/memory/$(date +%Y-%m-%d).md 2>/dev/null || echo "(今日memory为空)"

# 读取会话历史（最后24小时）
```

### 3. 生成日报

**核心原则：深度 > 广度，反思 > 罗列。每个板块必须有真正思考，不能只写标题。**

报告结构：
```
# 📰 AI 每日热点 {日期}

## 🤖 AI & 科技圈热点（3-5条，每条要有一句话解读）
- [热点1] → [这句话背后意味着什么]
- [热点2] → [为什么这件事重要]
- [热点3] → [对普通人的影响]

## 💰 金融市场今日动态（2-4条，重点数据+背后逻辑）
- [市场1] 数据：[X] → [为什么会这样]
- [值得关注的信号]

---

# 💭 深度解读（必写，不能跳过）

## 今日最重要的一件事
[这件事是什么，为什么今天最重要]

## 这件事背后意味着什么
[深度分析，不只是陈述事实，要写出事件背后的逻辑和影响]

## 我从今天学到了什么
[可以是AI进展、市场规律、工作方法、人生感悟等，任选1-2个最感触的]

## 值得关注的信号（3个以内）
- [信号1]：为什么值得关注
- [信号2]：...

---

# 📋 鱼丸工作日报 {日期}

## ✅ 今日完成
- [工作1]
- [工作2]

## 💡 经验与反思
- [今日工作中学到什么？有什么可以改进的？]
- [对AI/科技领域的思考]
- [有没有哪个决定现在回头看觉得可以更好？]

## 📅 明日规划
- [规划1]
- [规划2]

## 📝 备注
[想记住的任何事]
```

### 4. 发送飞书消息

```bash
# 使用飞书 IM 发送日报摘要
# 通过 openclaw feishu_im 或直接调用 API
```

### 5. 存档

```bash
cp /tmp/daily_report.md ~/obsidian-vault/07-Clippings/daily-report-$(date +%Y-%m-%d).md
```

## 关键配置

| 配置 | 值 |
|------|-----|
| 发送时间 | 每天 18:00 (周一~周五) |
| 存档路径 | `~/obsidian-vault/07-Clippings/daily-report-YYYY-MM-DD.md` |
| 飞书接收人 | 自己 (open_id: ou_7122e19e040f7dc6fbb6e7ed89ddf873) |

## 注意事项

- 18:00 执行时确保摘要简洁（飞书消息长度限制）
- 长报告创建飞书文档，只发链接摘要到飞书消息
- 工作总结从 memory 文件读取今日记录
- GitHub Trending 取当天新上榜或 star 增长快的项目
