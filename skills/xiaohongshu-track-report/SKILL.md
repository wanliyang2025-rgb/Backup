---
name: xiaohongshu-track-report
description: 小红书赛道热点分析报告生成器。每周自动抓取小红书指定赛道（如家居、美食、装修等）的热门帖子，生成结构化分析报告，包含热门内容、关键词、趋势洞察、原文链接，并创建飞书文档。触发场景：(1) 用户要求生成小红书赛道报告 (2) 每周定时任务（周六凌晨4点） (3) 分析特定赛道热度 (4) 生成周报并发送飞书
---

# 小红书赛道分析报告 Skill

## 核心能力

1. 通过 Chrome DevTools Protocol 控制服务器 Chrome 抓取小红书数据
2. 提取热门帖子标题、作者、点赞数、原文链接
3. 生成结构化分析（关键词热度、内容类型、趋势洞察）
4. 创建飞书文档并写入完整报告

## 工作流程

### Step 1: 启动 Chrome（如未运行）

```bash
# 检查 Chrome 是否运行
ps aux | grep chrome | grep -v grep

# 如未运行，启动带远程调试的 Chrome
/opt/google/chrome/chrome \
  --user-data-dir=/tmp/chrome-controlled \
  --remote-debugging-port=9222 \
  --no-sandbox \
  --enable-features=WebMCPTesting \
  --window-size=1280,900 &
```

### Step 2: 连接 Chrome 获取 Tab

```bash
curl -s http://localhost:9222/json/list | python3 -c "
import json, sys
tabs = json.load(sys.stdin)
# 找小红书标签页，没有则创建
target = [t for t in tabs if 'xiaohongshu' in t.get('url','')]
if target:
    print(target[0]['id'], target[0]['webSocketDebuggerUrl'])
else:
    # 创建新标签
    new = [t for t in tabs if t.get('type')=='page'][0]
    print(new['id'], new['webSocketDebuggerUrl'])
"
```

### Step 3: 抓取数据

使用 `scripts/xhs_scraper.js` 脚本抓取：

```bash
node scripts/xhs_scraper.js <tab_id> <赛道关键词>
```

关键数据点：
- 帖子标题、作者、点赞数、发布日期
- 原文链接（格式：`https://www.xiaohongshu.com/explore/{id}`）
- 搜索联想词（热度词）

### Step 4: 生成报告

报告结构：
```
一、本周赛道概览
二、热门帖子 TOP15（含链接）
三、热门关键词分析
四、内容类型分布
五、趋势洞察
六、下周预测
七、内容互动数据
八、跨赛道对比
九、原帖链接
十、创作建议
```

### Step 5: 创建飞书文档

```bash
# 获取 token
TOKEN=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d '{"app_id":"cli_a93b3aa665789cc2","app_secret":"d4lvhry3RZcCtDfGekHbyeNTy00TXjv0"}' \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['tenant_access_token'])")

# 创建文档
DOC=$(curl -s -X POST "https://open.feishu.cn/open-apis/docx/v1/documents" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"title":"小红书家居赛道本周热点分析报告 YYYY-MM-DD"}')
DOC_ID=$(echo $DOC | python3 -c "import json,sys; print(json.load(sys.stdin)['data']['document']['document_id'])")

# 写入内容块（block_type=2 为文本段落）
curl -s -X POST "https://open.feishu.cn/open-apis/docx/v1/documents/$DOC_ID/blocks/$DOC_ID/children" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"children":[{"block_type":2,"text":{"elements":[{"text_run":{"content":"内容"}}],"style":{"align":1}}}],"index":-1}'
```

### Step 6: 存档报告

```bash
# 存档到 workspace
cp /tmp/xhs_report.md ~/obsidian-vault/07-Clippings/xhs-{track}-weekly-YYYY-MM-DD.md
```

## 关键配置

| 配置项 | 值 |
|--------|-----|
| Feishu App ID | `cli_a93b3aa665789cc2` |
| Feishu App Secret | `d4lvhry3RZcCtDfGekHbyeNTy00TXjv0` |
| Chrome 路径 | `/opt/google/chrome/chrome` |
| Chrome 调试端口 | `9222` |
| User Data Dir | `/tmp/chrome-controlled` |
| 文档默认存放 | 个人知识库（wiki_space: my_library）|

## 注意事项

- 小红书页面需要登录态，User Data Dir 使用 `/tmp/chrome-controlled`（用户需提前登录一次）
- CDP 导航需要 WebSocket 连接，使用 `ws` Node.js 模块
- 飞书文档 block_type：1=页面, 2=文本, 3=h3, 4=h4, 5=h5, 12=列表
- 热门帖子链接从 `a[href*="/explore/"]` 获取，需拼接完整 URL

## 参考资料

- 详细 Feishu API 见 `references/feishu-doc-api.md`
- Chrome CDP 用法见 `references/chrome-cdp.md`
