#!/usr/bin/env node
/**
 * 大众点评汤泉套餐抓取
 * 从已登录的 Chrome 浏览器提取数据
 */
const WebSocket = require('ws');

// 获取任意一个 Chrome tab
const tabs = JSON.parse(require('child_process').execSync('curl -s http://localhost:9222/json/list').toString());
const TAB_ID = tabs[0].id;
console.error('Using tab:', TAB_ID);

const ws = new WebSocket(`ws://localhost:9222/devtools/page/${TAB_ID}`);

const KEYWORD = process.argv[2] || '汤泉中心';

ws.on('open', () => {
  const url = `https://www.dianping.com/search/keyword/4/10_${encodeURIComponent(KEYWORD)}`;
  console.error('Navigating to:', url);
  ws.send(JSON.stringify({id: 1, method: 'Page.navigate', params: {url}}));
});

ws.on('message', (data) => {
  const msg = JSON.parse(data.toString());
  if (msg.id === 1) {
    console.error('Page loading...');
    setTimeout(() => {
      ws.send(JSON.stringify({id: 2, method: 'Runtime.evaluate', params: {expression: `
        (function() {
          const results = [];
          document.querySelectorAll('.shop-list li, .tuan-item, .J_shop').forEach((item, i) => {
            if (i >= 15) return;
            const nameEl = item.querySelector('.title, h3, .shop-name');
            const priceEl = item.querySelector('.price, [class*="price"]');
            const addrEl = item.querySelector('.addr, .address');
            if (nameEl) {
              const name = nameEl.innerText.trim().split('\\n')[0].substring(0, 60);
              const price = priceEl ? priceEl.innerText.trim().split('\\n')[0] : 'N/A';
              const addr = addrEl ? addrEl.innerText.trim().substring(0, 50) : 'N/A';
              results.push({name, price, addr});
            }
          });
          return JSON.stringify(results);
        })()
      `}}));
    }, 8000);
  }
  if (msg.id === 2 && msg.result) {
    try {
      const result = JSON.parse(msg.result.result.value);
      console.log(JSON.stringify(result, null, 2));
    } catch(e) {
      console.log('[]');
    }
    ws.close();
  }
});

ws.on('error', (e) => { console.error('Error:', e.message); process.exit(1); });
setTimeout(() => { ws.close(); process.exit(0); }, 25000);
