#!/bin/bash
# 小红书定投 - 每日行情推送脚本
# 每天 8:00 (周一~周五) 自动执行

WORKSPACE="/home/leonwan/.openclaw/workspace"
OUTPUT="$WORKSPACE/daily-market-update.md"
LOG="$WORKSPACE/logs/daily-market.log"

mkdir -p "$WORKSPACE/logs"

echo "[$(date '+%Y-%m-%d %H:%M')] 开始获取行情..." >> "$LOG"

# --- 获取黄金行情（简洁标题） ---
GOLD_NEWS=$(python3 - << 'EOF'
try:
    from urllib.request import urlopen, Request
    import re
    
    url = "https://www.gold.org.cn/hjbindex/ttlb/"
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urlopen(req, timeout=10) as r:
        content = r.read().decode('utf-8')
    
    # 提取带日期的新闻标题
    pattern = r'\[(\d{4}-\d{2}-\d{2})\]\s*([^<\n]{5,60})'
    matches = re.findall(pattern, content)
    
    results = []
    keywords = ['金价', '黄金', '下跌', '上涨', '跌破', '突破', '避险', '央行', '暴跌', '大涨', '单周', '连跌']
    for date, title in matches:
        for kw in keywords:
            if kw in title and title.strip() not in results:
                results.append(f"[{date}] {title.strip()}")
                break
    
    for r in results[:3]:
        print(f"• {r}")
        
except Exception as e:
    print(f"  获取失败: {e}")
EOF
)

# --- 获取美股动态（简洁标题） ---
US_NEWS=$(python3 - << 'EOF'
try:
    from urllib.request import urlopen, Request
    import re
    
    urls = [
        "https://finance.sina.com.cn/stock/",
        "https://finance.sina.com.cn/roll/index.d.html?cid=56907"
    ]
    
    all_titles = []
    for url in urls:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req, timeout=10) as r:
            content = r.read().decode('utf-8', errors='ignore')
        
        pattern = r'<a[^>]+href="[^"]*"[^>]*>([^<]{5,60})</a>'
        matches = re.findall(pattern, content)
        
        keywords = ['纳斯达克', '标普', '美股', '特朗普', '关税', '美联储', '道指', '大跌', '大涨', '华尔街']
        for title in matches:
            title = title.strip()
            for kw in keywords:
                if kw in title and title not in all_titles and len(title) > 8:
                    all_titles.append(title)
                    break
    
    for t in all_titles[:4]:
        print(f"• {t}")
        
except Exception as e:
    print(f"  获取失败: {e}")
EOF
)

# --- 生成行情文档 ---
cat > "$OUTPUT" << EOF
# 📊 每日行情速览 - $(date '+%Y年%m月%d日 %A')
> 生成时间：$(date '+%H:%M:%S')

---

## 🥇 黄金市场

$GOLD_NEWS

---

## 📈 美股动态

$US_NEWS

---

💡 **发帖提示**：复制以上行情到模板对应位置即可
EOF

echo "[$(date '+%Y-%m-%d %H:%M')] 完成" >> "$LOG"
echo "done"