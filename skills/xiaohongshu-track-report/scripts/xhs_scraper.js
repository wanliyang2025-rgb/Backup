#!/usr/bin/env node
/**
 * 小红书赛道数据抓取脚本
 * 用法: node xhs_scraper.js <tab_id> <关键词>
 * 
 * 通过 Chrome DevTools Protocol 抓取小红书搜索结果
 */

const WebSocket = require('ws');

const TAB_ID = process.argv[2];
const KEYWORD = process.argv[3] || '家居';
const BASE_URL = `ws://localhost:9222/devtools/page/${TAB_ID}`;

console.error(`Connecting to Chrome tab: ${TAB_ID}`);
console.error(`Target keyword: ${KEYWORD}`);

const ws = new WebSocket(BASE_URL);

ws.on('open', () => {
  console.error('WebSocket connected, navigating...');
  const searchUrl = `https://www.xiaohongshu.com/search_result?keyword=${encodeURIComponent(KEYWORD)}&source=web_explore_feed&type=51`;
  ws.send(JSON.stringify({ id: 1, method: 'Page.navigate', params: { url: searchUrl } }));
});

ws.on('message', (data) => {
  const msg = JSON.parse(data.toString());
  
  if (msg.id === 1) {
    console.error('Navigation sent, waiting for page load...');
    setTimeout(() => {
      // 提取笔记数据
      const script = `
        (function() {
          const results = [];
          const items = document.querySelectorAll('.note-item, .feeds-page > div > div');
          
          items.forEach((item, i) => {
            if (i >= 30) return;
            
            const linkEl = item.querySelector('a[href*="/explore/"]');
            const titleEl = item.querySelector('.title, h2, .desc');
            const likesEl = item.querySelector('.liked-count, .count, [class*="count"]');
            const authorEl = item.querySelector('.author, .name, [class*="user"]');
            
            if (linkEl && titleEl) {
              let href = linkEl.href || linkEl.getAttribute('href');
              // 修复重复域名
              href = href.replace(/^https:\/\/www\.xiaohongshu\.comhttps:\/\/www\.xiaohongshu\.com/, 'https://www.xiaohongshu.com');
              results.push({
                title: titleEl.innerText.substring(0, 80).trim(),
                url: href,
                likes: likesEl ? likesEl.innerText.replace(/[^0-9万]/g, '') : 'N/A',
                author: authorEl ? authorEl.innerText.split('\\n')[0].substring(0, 20) : 'N/A'
              });
            }
          });
          
          // 也获取搜索联想词
          const suggestions = [];
          document.querySelectorAll('.hot-word, .suggest-item, [class*="suggest"]').forEach(el => {
            const text = el.innerText.trim();
            if (text && text.length < 20) suggestions.push(text);
          });
          
          return JSON.stringify({ notes: results, suggestions: suggestions.slice(0, 15) });
        })()
      `;
      ws.send(JSON.stringify({ id: 2, method: 'Runtime.evaluate', params: { expression: script } }));
    }, 6000);
  }
  
  if (msg.id === 2 && msg.result) {
    try {
      const data = JSON.parse(msg.result.result.value);
      
      // 输出结构化数据
      console.log('=== XHS_DATA ===');
      console.log(JSON.stringify(data, null, 2));
      console.log('=== END_XHS_DATA ===');
    } catch (e) {
      console.error('Parse error:', e.message);
    }
    ws.close();
  }
});

ws.on('error', (e) => {
  console.error('WebSocket error:', e.message);
  process.exit(1);
});

ws.on('close', () => {
  process.exit(0);
});

setTimeout(() => {
  console.error('Timeout, closing...');
  ws.close();
  process.exit(0);
}, 40000);
