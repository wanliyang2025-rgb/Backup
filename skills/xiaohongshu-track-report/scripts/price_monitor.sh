#!/bin/bash
# 团购套餐价格监控脚本
# 用于抓取大众点评/美团/抖音的汤泉/温泉套餐价格

set -e

TODAY=$(date +%Y-%m-%d)
OUTPUT_FILE="/tmp/taoquan_prices_${TODAY}.json"
COOKIES_DIR="/tmp/chrome-cookies"

# 检查 Chrome 调试端口
check_chrome() {
    curl -s http://localhost:9222/json/list > /dev/null 2>&1 || {
        echo "Chrome not running with debug port, starting..."
        nohup /opt/google/chrome/chrome \
            --user-data-dir=/tmp/chrome-controlled \
            --remote-debugging-port=9222 \
            --no-sandbox \
            --enable-features=WebMCPTesting \
            > /dev/null 2>&1 &
        sleep 4
    }
}

# 从浏览器获取 Cookie
get_cookies() {
    local domain=$1
    node << NODEJS
const WebSocket = require('ws');
const tabs = JSON.parse(require('child_process').execSync('curl -s http://localhost:9222/json/list').toString());
const ws = new WebSocket('ws://localhost:9222/devtools/page/' + tabs[0].id);
ws.on('open', () => {
    ws.send(JSON.stringify({id: 1, method: 'Network.getAllCookies'}));
});
ws.on('message', (data) => {
    const msg = JSON.parse(data.toString());
    if (msg.id === 1) {
        const cookies = msg.result.cookies.filter(c => 
            !c.domain || c.domain.includes('$domain')
        );
        console.log(JSON.stringify(cookies.map(c => c.name + '=' + c.value)));
        ws.close();
    }
});
ws.on('error', () => ws.close());
setTimeout(() => process.exit(0), 5000);
NODEJS
}

# 抓取大众点评
scrape_dianping() {
    local keyword=$1
    node << NODEJS
const WebSocket = require('ws');
const tabs = JSON.parse(require('child_process').execSync('curl -s http://localhost:9222/json/list').toString());
const ws = new WebSocket('ws://localhost:9222/devtools/page/' + tabs[0].id);

ws.on('open', () => {
    const url = 'https://www.dianping.com/search/keyword/4/10_' + encodeURIComponent('$keyword');
    ws.send(JSON.stringify({id: 1, method: 'Page.navigate', params: {url}}));
});

ws.on('message', (data) => {
    const msg = JSON.parse(data.toString());
    if (msg.id === 1) {
        // 等待页面加载
        setTimeout(() => {
            ws.send(JSON.stringify({id: 2, method: 'Runtime.evaluate', params: {expression: `
                (function() {
                    const results = [];
                    document.querySelectorAll('.shop-list li, .tuan-item').forEach((item, i) => {
                        if (i >= 15) return;
                        const nameEl = item.querySelector('.title, h3, .shop-name');
                        const priceEl = item.querySelector('.price, [class*="price"]');
                        const addrEl = item.querySelector('.addr, .address');
                        if (nameEl) {
                            results.push({
                                name: nameEl.innerText.trim().split('\\n')[0].substring(0, 60),
                                price: priceEl ? priceEl.innerText.trim().split('\\n')[0] : 'N/A',
                                addr: addrEl ? addrEl.innerText.trim().substring(0, 50) : 'N/A'
                            });
                        }
                    });
                    return JSON.stringify(results);
                })()
            `}}));
        }, 8000);
    }
    if (msg.id === 2 && msg.result) {
        try {
            console.log(msg.result.result.value);
        } catch(e) {
            console.log('[]');
        }
        ws.close();
    }
});

ws.on('error', (e) => { console.error('WS error:', e.message); process.exit(1); });
setTimeout(() => { ws.close(); process.exit(0); }, 25000);
NODEJS
}

# 主流程
echo "=== 汤泉套餐价格抓取 $(date) ==="

check_chrome

echo "[1/2] 抓取大众点评..."
DP_RESULT=$(scrape_dianping "汤泉中心")
echo "$DP_RESULT" | python3 -m json.tool 2>/dev/null | head -50 || echo "Parse failed, raw: $DP_RESULT"

echo "[2/2] 抓取抖音..."
# 抖音需要特殊处理
node << NODEJS
const WebSocket = require('ws');
const tabs = JSON.parse(require('child_process').execSync('curl -s http://localhost:9222/json/list').toString());
const ws = new WebSocket('ws://localhost:9222/devtools/page/' + tabs[0].id);

ws.on('open', () => {
    ws.send(JSON.stringify({id: 1, method: 'Page.navigate', params: {
        url: 'https://www.douyin.com/search/%E6%B1%B6%E6%B3%89%E4%B8%AD%E5%BF%83%20%E5%A5%97%E9%A4%90'
    }}));
});

ws.on('message', (data) => {
    const msg = JSON.parse(data.toString());
    if (msg.id === 1) {
        setTimeout(() => {
            ws.send(JSON.stringify({id: 2, method: 'Runtime.evaluate', params: {expression: `
                (function() {
                    // 等待商品卡片出现
                    const items = document.querySelectorAll('[class*="product-card"], [class*="shop-card"], [class*="deal-card"]');
                    const results = [];
                    items.forEach((item, i) => {
                        if (i >= 10) return;
                        const nameEl = item.querySelector('[class*="title"], [class*="name"], h3, span');
                        const priceEl = item.querySelector('[class*="price"]');
                        if (nameEl && nameEl.innerText.trim()) {
                            results.push({
                                name: nameEl.innerText.trim().substring(0, 50),
                                price: priceEl ? priceEl.innerText.trim() : 'N/A'
                            });
                        }
                    });
                    return JSON.stringify(results.length ? results : [{note: 'No items found, page may still loading or requires login'}]);
                })()
            `}}));
        }, 10000);
    }
    if (msg.id === 2 && msg.result) {
        try {
            console.log(msg.result.result.value);
        } catch(e) {
            console.log('[]');
        }
        ws.close();
    }
});

ws.on('error', (e) => { console.error(e.message); process.exit(1); });
setTimeout(() => { ws.close(); process.exit(0); }, 30000);
NODEJS

echo "=== 完成 ==="
