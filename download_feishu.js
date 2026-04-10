const path = require('path');
const fs = require('fs');

const APP_ID = 'cli_a93b3aa665789cc2';
const APP_SECRET = 'd4lvhry3RZcCtDfGekHbyeNTy00TXjv0';

const Lark = require('@larksuiteoapi/node-sdk');

const client = new Lark.Client({
  appId: APP_ID,
  appSecret: APP_SECRET,
  appType: Lark.AppType.SelfBuild,
  domain: Lark.Domain.Feishu
});

const fileToken = process.argv[2] || 'file_v3_00vu_5bfe5f3d-6cb8-4036-9813-eed6cbe8791g';
const outputPath = process.argv[3] || path.join(__dirname, 'downloaded.xlsx');

async function downloadFile() {
  try {
    // Get download info
    const response = await client.drive.file.get_download_info({
      file_token: fileToken
    });
    
    console.log('Response code:', response.code);
    
    if (response.code !== 0) {
      console.error('Error:', response.msg);
      process.exit(1);
    }
    
    const downloadUrl = response.data.download_url;
    console.log('Download URL:', downloadUrl);
    
    // Download the file using node-fetch or built-in https
    const https = require('https');
    const file = fs.createWriteStream(outputPath);
    
    https.get(downloadUrl, (res) => {
      res.pipe(file);
      file.on('finish', () => {
        file.close();
        console.log('Downloaded to:', outputPath);
      });
    }).on('error', (err) => {
      fs.unlink(outputPath, () => {});
      console.error('Download error:', err);
      process.exit(1);
    });
    
  } catch (error) {
    console.error('Error:', error);
    process.exit(1);
  }
}

downloadFile();
