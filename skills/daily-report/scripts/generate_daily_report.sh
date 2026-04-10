#!/bin/bash
# 日报生成脚本 - 每天 18:00 自动执行
# 总结：AI/科技热点 + 金融市场 + GitHub Trending + 今日工作

# set -e  # 已禁用，允许各步骤独立失败，不阻断整体

SKILL_DIR="$HOME/.openclaw/workspace/skills/daily-report"
TODAY=$(date +%Y-%m-%d)
REPORT_FILE="/tmp/daily_report_${TODAY}.md"
ARCHIVE_DIR="$HOME/obsidian-vault/07-Clippings"
LOG_FILE="/tmp/daily_report_${TODAY}.log"

exec > "$LOG_FILE" 2>&1
echo "=== 日报任务开始: $(date) ==="

# ========== Step 1: 搜集 AI 新闻 ==========
echo "[1/6] 搜索 AI 热点..."
AI_NEWS=$(python3 -c "
import subprocess, json

# 使用 Tavily 搜索（如果可用）
try:
    result = subprocess.run([
        'python3', '$HOME/.openclaw/workspace/skills/openclaw-tavily-search/scripts/tavily_search.py',
        '--query', 'AI 人工智能 最新进展 2026',
        '--max-results', '5', '--format', 'md'
    ], capture_output=True, text=True, timeout=30, cwd='$HOME/.openclaw/workspace/skills/openclaw-tavily-search')
    if result.returncode == 0:
        print('## AI 科技热点\n' + result.stdout)
except:
    print('## AI 科技热点\n(Tavily 搜索不可用，跳过)')
" 2>/dev/null) || AI_NEWS="## AI 科技热点\n(搜索服务暂时不可用)"

# ========== Step 2: 搜集 GitHub Trending ==========
echo "[2/6] 获取 GitHub Trending..."

GITHUB_TRENDING=$(curl -s "https://api.github.com/search/repositories?q=created:>$(date -d '30 days ago' +%Y-%m-%d)+OR+stars:>100&sort=stars&order=desc&per_page=10" \
  2>/dev/null | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    items = d.get('items', [])[:8]
    if items:
        lines = ['## GitHub Trending AI 项目\n']
        for r in items:
            desc = r.get('description') or '无描述'
            lang = r.get('language') or ''
            stars = r.get('stargazers_count', 0)
            lines.append(f'- **{r[\"full_name\"]}** ⭐{stars} {lang}')
            lines.append(f'  {desc}')
        print('\n'.join(lines))
    else:
        print('## GitHub Trending\n(暂无数据)')
except Exception as e:
    print(f'## GitHub Trending\n(获取失败: {e})')
" 2>/dev/null) || GITHUB_TRENDING="## GitHub Trending\n(网络不可用)"


# ========== Step 3: 金融市场动态 ==========
echo "[3/6] 搜索金融市场热点..."

MARKET_NEWS=$(python3 -c "
import urllib.request, json

# 使用 Tavily 搜索金融新闻
try:
    import subprocess
    result = subprocess.run([
        'python3', '$HOME/.openclaw/workspace/skills/openclaw-tavily-search/scripts/tavily_search.py',
        '--query', '今日A股 理财 市场热点 $(date +%Y-%m-%d)',
        '--max-results', '3', '--format', 'md'
    ], capture_output=True, text=True, timeout=20, cwd='$HOME/.openclaw/workspace/skills/openclaw-tavily-search')
    if result.returncode == 0 and result.stdout.strip():
        print('## 金融市场今日动态\n' + result.stdout[:2000])
    else:
        print('## 金融市场今日动态\n(今日市场数据获取中...)')
except Exception as e:
    print('## 金融市场今日动态\n(暂时无法获取市场信息)')
" 2>/dev/null) || MARKET_NEWS="## 金融市场今日动态\n(服务不可用)"


# ========== Step 4: 读取今日工作记录 ==========
echo "[4/6] 读取今日工作记录..."

WORK_LOG=$(cat "$HOME/.openclaw/memory/${TODAY}.md" 2>/dev/null | head -100 || echo "(今日工作记录为空)")


# ========== Step 5: 生成完整报告 ==========
echo "[5/6] 生成日报..."

cat > "$REPORT_FILE" << REPORT_EOF
# 📰 AI 每日热点 · ${TODAY}

---

${AI_NEWS}

---

${MARKET_NEWS}

---

${GITHUB_TRENDING}

---

# 📋 鱼丸工作日报 · ${TODAY}

> 自动生成时间：$(date "+%H:%M:%S")

## ✅ 今日完成

${WORK_LOG:-（今日暂无工作记录）}

---

## 💡 经验与教训

- （根据今日工作自动总结）

---

## 📅 明日规划

- 继续监控小红书家居赛道数据
- 检查定时任务执行情况
- （其他待办）

---

## 📝 备注

本日报由 AI 助手鱼丸自动生成
REPORT_EOF

echo "日报已生成: $REPORT_FILE"


# ========== Step 6: 发送飞书消息 ==========
echo "[6/6] 发送飞书通知..."

# 获取飞书 token
APP_ID="cli_a93b3aa665789cc2"
APP_SECRET="d4lvhry3RZcCtDfGekHbyeNTy00TXjv0"

TOKEN=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
    -H "Content-Type: application/json" \
    -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}" \
    | python3 -c "import json,sys; print(json.load(sys.stdin)['tenant_access_token'])" 2>/dev/null)

if [ -n "$TOKEN" ]; then
    # 创建飞书文档
    DOC_RESP=$(curl -s -X POST "https://open.feishu.cn/open-apis/docx/v1/documents" \
        -H "Authorization: Bearer $TOKEN" \
        -H "Content-Type: application/json" \
        -d "{\"title\":\"📋 日报 ${TODAY} · 鱼丸\"}")
    
    DOC_ID=$(echo "$DOC_RESP" | python3 -c "import json,sys; print(json.load(sys.stdin)['data']['document']['document_id'])" 2>/dev/null)
    
    if [ -n "$DOC_ID" ]; then
        # 添加报告内容
        add_block() {
            curl -s -X POST "https://open.feishu.cn/open-apis/docx/v1/documents/$DOC_ID/blocks/$DOC_ID/children" \
                -H "Authorization: Bearer $TOKEN" \
                -H "Content-Type: application/json" \
                -d "$1" > /dev/null
        }
        
        add_block '{"children":[{"block_type":2,"text":{"elements":[{"text_run":{"content":"📰 今日 AI + 金融市场热点 + 工作日报 | '"$TODAY"'"}}],"style":{"align":1}}}],"index":-1}'
        add_block '{"children":[{"block_type":2,"text":{"elements":[{"text_run":{"content":"👉 完整报告已生成，点击上方链接查看","text_element_style":{"bold":true}}}],"style":{"align":1}}}],"index":-1}'
        
        MSG="📋 今日日报已生成
$(date '+%H:%M') · AI 热点 + 市场动态 + 工作总结
👉 $(echo "https://www.feishu.cn/docx/$DOC_ID")"
        
        # 发送消息给自己
        curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
            -H "Authorization: Bearer $TOKEN" \
            -H "Content-Type: application/json" \
            -d "{\"receive_id\":\"ou_7122e19e040f7dc6fbb6e7ed89ddf873\",\"msg_type\":\"text\",\"content\":\"{\\\"text\\\":\\\"$MSG\\\"}\"}" \
            > /dev/null 2>&1
        
        echo "飞书消息已发送: https://www.feishu.cn/docx/$DOC_ID"
    fi
fi


# ========== 存档 ==========
mkdir -p "$ARCHIVE_DIR"
cp "$REPORT_FILE" "$ARCHIVE_DIR/daily-report-${TODAY}.md"
echo "已存档: $ARCHIVE_DIR/daily-report-${TODAY}.md"


# ========== 完成 ==========
echo "=== 日报任务完成: $(date) ==="
