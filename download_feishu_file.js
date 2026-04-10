const https = require('https');
const fs = require('fs');
const { URL } = require('url');

// 配置
const appId = 'cli_a93b3aa665789cc2';
const appSecret = 'd4lvhry3RZcCtDfGekHbyeNTy00TXjv0';

// 要下载的文件信息
const messageId = process.argv[2] || 'om_x100b54e4300bd4a4b3571190aa07430';
const fileKey = process.argv[3] || 'file_v3_00vv_a8c170eb-6dcb-4583-ae07-d0d692a5c87g';
const savePath = process.argv[4] || '/home/leonwan/.openclaw/workspace/科目余额表-豆包2512.xlsx';

async function getTenantAccessToken() {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify({
      app_id: appId,
      app_secret: appSecret,
    });

    const options = {
      hostname: 'open.feishu.cn',
      path: '/open-apis/auth/v3/tenant_access_token/internal',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': data.length,
      },
    };

    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', (chunk) => body += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(body);
          if (result.tenant_access_token) {
            resolve(result.tenant_access_token);
          } else {
            reject(new Error('No token: ' + body));
          }
        } catch (e) {
          reject(e);
        }
      });
    });

    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

async function getDownloadUrl(token, messageId, fileKey) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'open.feishu.cn',
      path: `/open-apis/im/v1/messages/${messageId}/resources/${fileKey}?type=file`,
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    };

    const req = https.request(options, (res) => {
      // 检查content-type，如果是application/json则解析，否则直接下载
      const contentType = res.headers['content-type'] || '';
      
      if (contentType.includes('application/json')) {
        let body = '';
        res.on('data', (chunk) => body += chunk);
        res.on('end', () => {
          try {
            const result = JSON.parse(body);
            if (result.data && result.data.download_url) {
              resolve(result.data.download_url);
            } else {
              reject(new Error('No download URL: ' + body));
            }
          } catch (e) {
            reject(e);
          }
        });
      } else {
        // 直接返回response让调用方处理
        resolve(res);
      }
    });

    req.on('error', reject);
    req.end();
  });
}

function downloadFile(url, savePath) {
  return new Promise((resolve, reject) => {
    // 如果是已解析的http.IncomingMessage，直接pipe
    if (url && url.pipe) {
      url.pipe(fs.createWriteStream(savePath));
      url.on('end', () => {
        console.log('File saved to:', savePath);
        resolve();
      });
      url.on('error', reject);
      return;
    }
    
    // 否则作为URL字符串处理
    const file = fs.createWriteStream(savePath);
    
    https.get(url, (res) => {
      res.pipe(file);
      file.on('finish', () => {
        file.close();
        console.log('File saved to:', savePath);
        resolve();
      });
    }).on('error', (err) => {
      fs.unlink(savePath, () => {});
      reject(err);
    });
  });
}

async function main() {
  try {
    console.log('Getting token...');
    const token = await getTenantAccessToken();
    console.log('Token obtained');

    console.log('Getting download URL...');
    const result = await getDownloadUrl(token, messageId, fileKey);
    
    // 检查返回类型
    if (typeof result === 'string') {
      console.log('Download URL:', result);
      console.log('Downloading file...');
      await downloadFile(result, savePath);
    } else {
      console.log('Direct download stream...');
      await downloadFile(result, savePath);
    }
    console.log('Done!');
  } catch (error) {
    console.error('Error:', error.message);
  }
}

main();
