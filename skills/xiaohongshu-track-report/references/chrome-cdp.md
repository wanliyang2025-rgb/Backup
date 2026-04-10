# Chrome DevTools Protocol 参考

## 启动 Chrome

```bash
/opt/google/chrome/chrome \
  --user-data-dir=/tmp/chrome-controlled \
  --remote-debugging-port=9222 \
  --no-sandbox \
  --enable-features=WebMCPTesting \
  --window-size=1280,900 \
  --start-fullscreen \
  > /tmp/chrome.log 2>&1 &
```

## 获取 Tab 列表

```bash
curl -s http://localhost:9222/json/list | python3 -m json.tool
```

返回：
```json
[{
  "id": "xxx",
  "title": "小红书",
  "url": "https://www.xiaohongshu.com/...",
  "webSocketDebuggerUrl": "ws://localhost:9222/devtools/page/xxx"
}]
```

## Node.js WebSocket 连接

```javascript
const WebSocket = require('ws');
const ws = new WebSocket('ws://localhost:9222/devtools/page/{tab_id}');

ws.on('open', () => {
  // 导航
  ws.send(JSON.stringify({
    id: 1,
    method: 'Page.navigate',
    params: { url: 'https://...' }
  }));
});

ws.on('message', (data) => {
  const msg = JSON.parse(data.toString());
  // 处理响应 msg.id === 1
  // 执行 JS
  ws.send(JSON.stringify({
    id: 2,
    method: 'Runtime.evaluate',
    params: { expression: 'document.title' }
  }));
});
```

## 常用 CDP 命令

| 命令 | 用途 |
|------|------|
| Page.navigate | 导航到 URL |
| Runtime.evaluate | 执行 JavaScript |
| Page.captureScreenshot | 截图 |
| DOM.getDocument | 获取 DOM |

## 页面滚动

```javascript
window.scrollBy(0, 1000);
```

## 等待页面加载

```javascript
// 等待元素出现
const el = document.querySelector('.target-class');
if (el) { /* found */ }

// 延时
await new Promise(r => setTimeout(r, 3000));
```

## 小红书页面选择器

| 内容 | 选择器 |
|------|--------|
| 笔记列表 | `.note-item, .feeds-page > div > div` |
| 标题 | `.title, h2, .desc` |
| 点赞数 | `.liked-count, .count` |
| 作者 | `.author, .name` |
| 原文链接 | `a[href*="/explore/"]` |
