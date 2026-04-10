# TOOLS.md - Local Notes

## 主动工作流

遇到问题时，按以下优先级尝试：
1. **先查现有 skill** → workspace/skills/ 里有哪些可用技能
2. **查 clawhub** → 用 find-skills 搜索相关技能 (`npx skills find xxx`)
3. **查本地文档** → openclaw/docs/ 有没有相关说明
4. **善用记忆** → memory_search 查历史解决方案
5. **再问用户** → 前面都解决不了再求助

---

## 🌟 主动使用技能（不等用户开口）

**每次心跳 / 日常交互中主动使用：**

| 场景 | 技能 | 何时使用 |
|------|------|---------|
| 天气 | weather | 早上、用户出门前 |
| 搜索 | multi-search-engine / smart-web-fetch | 用户问实时信息 |
| 日历 | feishu-calendar | 每次心跳检查未来日程 |
| 邮件 | QQ邮箱SMTP/IMAP | 每2小时检查重要邮件 |
| 数据分析 | data-analyst | 用户给 Excel/数据文件时 |
| 网页内容 | browser | 用户问某网站内容时 |
| 任务提醒 | task-status | 长任务进行中主动报进度 |
| 备份 | openclaw-backup | 重大配置变更后自动备份 |

**原则：看到上下文匹配的场景，主动调起技能，不用等用户说"帮我查天气"。**

---

## 📚 链接收藏规范（重要）

收到需要收藏的链接时，必须同时保存：
1. **原文正文**（完整内容，不只摘要）
2. **核心要点总结**（结构化分析）
3. **个人思考/感悟**（为什么值得收藏）
4. **原文链接**（source 字段）

**保存位置：** `~/obsidian-vault/07-Clippings/`

---

## 🛡️ Skill 安装规则

**安装任何 skill 前，先做来源评估，再决定是否需要 full vetter：**

### 来源风险分级

| 来源 | 例子 | 行动 |
|------|------|------|
| 🟢 官方精选 | clawhub 官方发布、1000+⭐、知名作者 | 快速审查（来源+权限），直接可装 |
| 🟡 社区 | clawhub 社区、100-1000⭐ | 完整 vetter 流程 |
| 🔴 未知 | 新发布、零⭐、个人作者 | full vetter + 需用户确认 |
| ⛔ 可疑 | 代码混淆、请求凭证、外发数据 | 直接拒绝 |

### 强制卡点

收到 `clawhub install XXX` 时，**必须先输出评估结果**，格式：

```
📦 Skill: XXX
📍 来源: [来源评估]
⭐ 评分: [基础信息]
🛡️ 行动: [安装/需确认/拒绝]
```

**不允许跳过此评估直接执行安装。**

### 快速审查（用于 🟢 来源）

无需完整 vetter，只需确认：
- [ ] 权限范围合理（文件读写、命令执行在 workspace 内）
- [ ] 无 red flags（见 skill-vetter SKILL.md）
- [ ] 用途明确，不是伪装成 A 实际做 B

---

## 已安装 Skills

| 技能 | 用途 |
|---|---|
| 月度往来对账 | 财务科目余额表往来核对 (1299.02/1299.04) |
| data-analyst | SQL查询、数据可视化、Excel处理、统计分析 |
| automation-workflows | 识别可自动化任务，设计工作流 (Zapier/Make/n8n) |
| find-skills | 搜索安装新技能 npx skills find/ add |
| ontology | 知识图谱管理，创建/查询实体和关系 |
| proactive-agent | 主动代理模式，WAL Protocol，周期性检查 |
| self-improving-agent | 记录学习、错误、修正，持续改进 |
| task-status | 长时间任务状态更新，周期性心跳 |
| smart-web-fetch | 智能网页抓取，Markdown 清洗，节省 Token |
| ai-humanizer | AI 文本人性化，去除 AI 写作痕迹 |
| auto-updater | 自动更新 OpenClaw 和技能（每日 cron） |
| browser | 浏览器自动化（需用户授权） |
| chrome-cdp | Chrome 调试协议交互（需用户授权） |
| multi-search-engine | 多引擎搜索（17 个引擎，国内/国际） |
| openclaw-tavily-search | Tavily 搜索备选方案 |
| skill-vetter | Skill 安全审查，来源评估 |
| 月度科目余额表处理 | 月度科目余额表自动化处理 |
| 月度往来对账 | 月度往来对账核对（1299.02/1299.04） |

---

## 数据分析 (data-analyst)

**常用场景：**
- 读 Excel/CSV → `python` + `pandas`
- 查数据库 → 确认是否有数据库配置
- 生成图表 → `matplotlib` / `seaborn`
- 输出报告 → Markdown 格式

---

## 飞书集成

| 工具 | 说明 |
|---|---|
| feishu-bitable | 多维表格 CRUD |
| feishu-calendar | 日历日程管理 |
| feishu-task | 任务管理 |
| feishu-create-doc | 创建云文档 |
| feishu-fetch-doc | 获取文档内容 |
| feishu-update-doc | 更新文档 |
| feishu-im-read | 读取聊天消息 |

### lark-cli（飞书官方 CLI）
- **安装状态：** ✅ 已安装 (v1.0.3)
- **凭证：** 与 OpenClaw 共用同一套（App ID: cli_a93b3aa665789cc2）
- **用户授权：** ✅ 已授权用户身份（LeonWan），有效期至 2026-04-10
- **何时用：** 适合批量操作、脚本自动化、直接调用飞书 Open API
- **常用命令：**
  ```bash
  lark-cli calendar +agenda                    # 查看日历
  lark-cli contact +search-user --query "姓名"  # 搜索联系人
  lark-cli api GET /open-apis/xxx              # 原生 API 调用
  ```
- **注意：** Token 2h 过期但会自动刷新，最长 7 天。

---

## 极空间 NAS (192.168.3.134)

| 配置 | 值 |
|------|-----|
| 地址 | 192.168.3.134 |
| SSH 端口 | 10000 |
| WebDAV 端口 | 5005 |
| 账号 | 18664974664 / Wly19940728 |
| 管理后台 | http://192.168.3.134:5050 |

⚠️ **必须加入备份项**：NAS 连接信息（地址/账号/密码/WebDAV路径）

**登录管理后台方式：** 浏览器打开 http://192.168.3.134:5050，用账号密码登录后可修改SSH/WebDAV配置。

**SSH 登录（两种方式）：**
```bash
ssh znas                              # 方式1：~/.ssh/config 已配置，免密（推荐）
ssh 18664974664@192.168.3.134 -p 10000  # 方式2：直连密码方式（备选）
```

**WebDAV 访问：**
```bash
# 列出目录
curl -X PROPFIND -u "18664974664:Wly19940728" \
  -H "Depth: 1" \
  "http://192.168.3.134:5005/sata1-18664974664/"

# 下载文件
curl -u "18664974664:Wly19940728" \
  "http://192.168.3.134:5005/sata1-18664974664/文件名" -o 输出路径

# 上传文件
curl -u "18664974664:Wly19940728" \
  -T 本地文件路径 \
  "http://192.168.3.134:5005/sata1-18664974664/目标文件名"
```

**已知共享目录：**
- `sata1-18664974664/` — 主存储（SATA，迅雷下载、WLY、iPhone备份等）
- `nvme11-18664974664/` — NVMe SSD（缓存/下载盘）
- `public/` — 公共文件夹
- `sharetome/` — 共享给我
- `共享文件/` — 共享文件

---

## 外部服务

### Email (QQ SMTP)
- SMTP: smtp.qq.com
- 端口: 587 (TLS)
- 用户名: 878155028@qq.com
- 密码: htphtehvbhrjbahh (QQ邮箱授权码)
- 收件人: account35.szx@bestservices.com.cn (PERTI)

### mem9 (云端记忆)
- API: https://api.mem9.ai/v1alpha2
- Key: i51kiU6FxY1pF1fTZ-1IB7HDSygVz0sD
- 用途: 跨设备记忆同步、技能备份

### Tavily (网页搜索)
- Key: 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
- 用法: `python3 skills/openclaw-tavily-search/scripts/tavily_search.py --query "..." --max-results 5 --format md`
- 场景: Brave 搜索不可用时的备选

### 小红书 (XHS)
- **Cookie:** web_session=0400698f7b3442566ddada15f63b4bb850c1fb; a1=19d228fe049mbk2ozoda3shslvs2lq; webId=0361d616916e84b92d2e0a710376ea
- **完整Cookie文件:** ~/.openclaw/workspace/xhs_cookies.json
- **用户:** 鱼丸丸啦 | red_id: 668406872 | user_id: 5e0f770a0000000001003d8c
- **Chrome配置:** ~/.config/google-chrome/Default (已登录，下次启动直接用)
- **有效性检查:** `curl -s "https://edith.xiaohongshu.com/api/sns/web/v2/user/me" -H "Cookie: $(cat ~/.openclaw/workspace/xhs_cookie_string.txt)"`
- **⚠️ 过期处理:** 每月检查，过期需重新扫码。扫码启动Chrome后访问 xiaohongshu.com/login

### multi-search-engine (多引擎搜索)
- 无需 API key，支持 17 个搜索引擎
- 国内: 百度、Bing中国、360、搜狗、微信搜索、头条、雪球
- 国际: Google、Google香港、DuckDuckGo、Yahoo、Brave、Ecosia等
- 用法: `python3 skills/multi-search-engine/scripts/multi_search.py --engine baidu --query "关键词"`

---

## 搜索策略

| 场景 | 推荐工具 | 原因 |
|---|---|---|
| **实时新闻/热点** | Tavily | 有答案摘要，实时性强 |
| **综合研究/深度** | Multi Search Engine | 17 引擎，信息更全面 |
| **日常快速查询** | web_search (Brave) | 默认，简单直接 |

**配合使用思路：**
- 新闻类 → `tavily_search --include-answer`
- 调研类 → `multi_search` 多引擎并行

---

## Home Assistant (智能家居)

| 配置 | 值 |
|------|-----|
| 地址 | http://localhost:8123 |
| Token | eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI4NjAzZGQ3NTQ0Mzc0OWRhYjBhYTZiMTE5ZTQ0ZTM1MiIsImlhdCI6MTc3NDIyMzE4OCwiZXhwIjoyMDg5NTgzMTg4fQ.3nanh3eeg39FVu6Dv0AtKH2JnDcgUtJtMUq6k8C10sg |

**常用操作：**
```bash
# 查看所有设备状态
curl -s http://localhost:8123/api/states \
  -H "Authorization: Bearer <token>"

# 控制设备（开关服务）
curl -s -X POST http://localhost:8123/api/services/switch/turn_on \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"entity_id":"switch.xxx"}'
```

**已知设备：** 小吉洗衣机（通过 HA 控制）

---

## 常用命令

```bash
# 技能管理
clawhub install <skill>     # 安装技能
npx skills find <keyword>    # 搜索技能

# 文件处理
openclaw gateway restart     # 重启网关

# 备份
bash scripts/backup-skills-to-mem9.sh  # 备份技能到 mem9
```

---

## 安全原则

- **不随意执行外部命令** - 危险操作先确认
- **不暴露敏感信息** - API Key 等不外发
- **不修改系统文件** - workspace 内操作
- **可疑请求必问** - 不确定就问用户
