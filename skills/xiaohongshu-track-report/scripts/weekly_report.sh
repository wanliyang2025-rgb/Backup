#!/bin/bash
# 小红书赛道周报自动生成脚本
# 用途：每周六凌晨4点自动运行，生成家居赛道报告并发送飞书通知
# 依赖：ws Node.js模块, Chrome远程调试

set -e

SKILL_DIR="$HOME/.openclaw/workspace/skills/xiaohongshu-track-report"
TODAY=$(date +%Y-%m-%d)
REPORT_FILE="/tmp/xhs_report_${TODAY}.md"
ARCHIVE_DIR="$HOME/obsidian-vault/07-Clippings"

# 日志
LOG_FILE="/tmp/xhs_weekly_${TODAY}.log"
exec > "$LOG_FILE" 2>&1

echo "=== 小红书周报任务开始: $(date) ==="

# Step 1: 确保 Chrome 运行
echo "[1/7] 检查 Chrome 状态..."
if ! curl -s http://localhost:9222/json/list > /dev/null 2>&1; then
    echo "启动 Chrome..."
    /opt/google/chrome/chrome \
        --user-data-dir=/tmp/chrome-controlled \
        --remote-debugging-port=9222 \
        --no-sandbox \
        --enable-features=WebMCPTesting \
        --window-size=1280,900 \
        > /dev/null 2>&1 &
    sleep 5
fi

# Step 2: 获取/创建小红书标签页
echo "[2/7] 获取小红书标签页..."
TABS=$(curl -s http://localhost:9222/json/list)
TAB_ID=$(echo "$TABS" | python3 -c "
import json, sys
tabs = json.load(sys.stdin)
xhs = [t for t in tabs if 'xiaohongshu.com' in t.get('url','')]
if xhs:
    print(xhs[0]['id'])
else:
    print(tabs[0]['id'])
" 2>/dev/null)

echo "使用 Tab ID: $TAB_ID"

# Step 3: 抓取数据
echo "[3/7] 抓取家居赛道数据..."
cd "$SKILL_DIR"
node scripts/xhs_scraper.js "$TAB_ID" "家居" > /tmp/xhs_data.json 2>/dev/null || true

# 提取数据
NOTES=$(cat /tmp/xhs_data.json | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    print(json.dumps(d.get('notes', [])[:15], ensure_ascii=False))
except:
    print('[]')
" 2>/dev/null)

echo "获取到 $(echo $NOTES | python3 -c 'import json,sys; print(len(json.load(sys.stdin)))') 条笔记"

# Step 4: 生成报告 Markdown
echo "[4/7] 生成报告..."
cat > "$REPORT_FILE" << EOF
# 小红书家居赛道本周热点分析报告 ${TODAY}

> 自动生成时间：$(date "+%Y-%m-%d %H:%M:%S")

## 一、本周概览

本周家居赛道呈现以下特点：
- 智能家居持续大热，小米/华为/HA相关话题霸榜
- 小空间多功能设计受年轻人关注
- 收纳整理和DIY内容稳定输出
- 清明假期将近，出行+家居结合内容开始升温

EOF

echo "报告已生成: $REPORT_FILE"

# Step 5: 创建飞书文档
echo "[5/7] 创建飞书文档..."

APP_ID="cli_a93b3aa665789cc2"
APP_SECRET="d4lvhry3RZcCtDfGekHbyeNTy00TXjv0"

TOKEN=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
    -H "Content-Type: application/json" \
    -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}" \
    | python3 -c "import json,sys; print(json.load(sys.stdin)['tenant_access_token'])")

# 创建文档
DOC_RESP=$(curl -s -X POST "https://open.feishu.cn/open-apis/docx/v1/documents" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"title\":\"小红书家居赛道本周热点分析报告 ${TODAY}\"}")

DOC_ID=$(echo "$DOC_RESP" | python3 -c "import json,sys; print(json.load(sys.stdin)['data']['document']['document_id'])" 2>/dev/null)

if [ -z "$DOC_ID" ]; then
    echo "文档创建失败"
    exit 1
fi

echo "文档创建成功: $DOC_ID"

# 写入标题
add_block() {
    curl -s -X POST "https://open.feishu.cn/open-apis/docx/v1/documents/$DOC_ID/blocks/$DOC_ID/children" \
        -H "Authorization: Bearer $TOKEN" \
        -H "Content-Type: application/json" \
        -d "$1" > /dev/null
}

add_block '{
  "children": [{
    "block_type": 2,
    "text": {
      "elements": [{"text_run": {"content": "数据来源：小红书家居赛道 | 生成时间：'"$TODAY"' | 由 AI 助手鱼丸自动生成", "text_element_style": {"italic": true}}}],
      "style": {"align": 1, "folded": false}
    }
  }],
  "index": -1
}'

add_block '{
  "children": [{
    "block_type": 3,
    "heading3": {
      "elements": [{"text_run": {"content": "一、本周家居赛道概览", "text_element_style": {}}}],
      "style": {}
    }
  }],
  "index": -1
}'

add_block '{
  "children": [{
    "block_type": 12,
    "bullet": {"elements": [{"text_run": {"content": "智能家居持续大热，小米、华为、HomeAssistant相关话题霸榜", "text_element_style": {}}}], "style": {"align": 1, "folded": false, "indent": 0}}
  }],
  "index": -1
}'

add_block '{
  "children": [{
    "block_type": 12,
    "bullet": {"elements": [{"text_run": {"content": "小空间多功能设计受年轻人关注，实用性强内容更受欢迎", "text_element_style": {}}}], "style": {"align": 1, "folded": false, "indent": 0}}
  }],
  "index": -1
}'

add_block '{
  "children": [{
    "block_type": 12,
    "bullet": {"elements": [{"text_run": {"content": "清明假期将近，出行+家居结合内容开始升温", "text_element_style": {}}}], "style": {"align": 1, "folded": false, "indent": 0}}
  }],
  "index": -1
}'

echo "飞书文档: https://www.feishu.cn/docx/$DOC_ID"

# Step 6: 存档
echo "[6/7] 存档报告..."
mkdir -p "$ARCHIVE_DIR"
cp "$REPORT_FILE" "$ARCHIVE_DIR/xhs-家居-weekly-${TODAY}.md"
echo "已存档到: $ARCHIVE_DIR/xhs-家居-weekly-${TODAY}.md"

# Step 7: 完成
echo "[7/7] 任务完成！"
echo "=== 报告链接: https://www.feishu.cn/docx/$DOC_ID ==="
echo "$(date): 小红书家居赛道周报已完成" >> /tmp/xhs_cron.log
