# 月度科目余额表处理

用于处理包含多个sheet的科目余额表文件，按要求合并、添加字段、过滤数据。

## 适用场景
- 科目余额表导出文件包含多个分公司/账套sheet
- 需要合并所有sheet到总表
- 需要添加账套列（值为sheet名称）
- 需要删除特定条件的空行

## 输入文件
- 飞书消息中的Excel文件（.xlsx格式）
- 包含多个sheet，每个sheet代表一个分公司/账套

## 处理步骤

### 步骤1：添加【账套】列
- 给文件中**每一个**sheet新增一列
- 列标题为【账套】
- 把该sheet的名称填充到对应表【账套】列的每一行

### 步骤2：合并所有sheet
- 把原文件所有sheet合并到一个新sheet
- 新sheet命名为【总表】

### 步骤3：删除核算项目为空的行
- 删除【总表】中，列标题为【核算项目】列，数据为空的行次

### 步骤4：删除期末余额都为空的行
- 删除【总表】中，**同时**满足以下条件的行：
  - 【期末余额借方（原币）】为空
  - 【期末余额贷方（原币）】为空
- 注意：只有**两列都为空**才删除，任何一列有值都不删除

## 输出文件
- 文件名：科目余额表_合并结果.xlsx
- 包含一个sheet：【总表】

## 代码实现

```javascript
const XLSX = require('xlsx');

function processExcel(inputPath, outputPath) {
  // 读取Excel文件
  const wb = XLSX.readFile(inputPath);
  const sheets = wb.SheetNames;
  
  // 步骤1+2: 给每个sheet添加【账套】列，值为sheet名称
  sheets.forEach(sheetName => {
    const ws = wb.Sheets[sheetName];
    const data = XLSX.utils.sheet_to_json(ws);
    const newData = data.map(row => ({ '账套': sheetName, ...row }));
    const newSheet = XLSX.utils.json_to_sheet(newData);
    wb.Sheets[sheetName] = newSheet;
  });
  
  // 步骤3: 合并所有sheet到总表
  let allData = [];
  sheets.forEach(sheetName => {
    const ws = wb.Sheets[sheetName];
    const data = XLSX.utils.sheet_to_json(ws);
    allData = allData.concat(data);
  });
  
  // 步骤4: 删除核算项目为空的行
  let filtered1 = allData.filter(r => 
    r['核算项目'] && r['核算项目'].toString().trim() !== ''
  );
  
  // 步骤5: 删除期末余额借方和贷方都为空的行
  let filtered2 = filtered1.filter(r => {
    const 借 = r['期末余额借方（原币）'];
    const 贷 = r['期末余额贷方（原币）'];
    const 借空 = !借 || 借 === '' || 借 === 0;
    const 贷空 = !贷 || 贷 === '' || 贷 === 0;
    return !(借空 && 贷空);  // 只有两者都为空才删除
  });
  
  // 保存结果
  const out = XLSX.utils.book_new();
  const sheet = XLSX.utils.json_to_sheet(filtered2);
  XLSX.utils.book_append_sheet(out, sheet, '总表');
  XLSX.writeFile(out, outputPath);
  
  return {
    totalSheets: sheets.length,
    mergedRows: allData.length,
    afterFilter1: filtered1.length,
    finalRows: filtered2.length
  };
}
```

## 邮件发送
- 收件人：account35.szx@bestservices.com.cn
- 主题：科目余额表_合并结果.xlsx
- 附件：输出文件

```javascript
const nodemailer = require('nodemailer');
const transporter = nodemailer.createTransport({
  host: 'smtp.qq.com', 
  port: 587, 
  secure: false,
  auth: { 
    user: '878155028@qq.com', 
    pass: 'htphtehvbhrjbahh'  // QQ邮箱授权码
  }
});

transporter.sendMail({
  from: '878155028@qq.com',
  to: 'account35.szx@bestservices.com.cn',
  subject: '科目余额表_合并结果.xlsx',
  text: `处理完成：\n- ${sheets.length}个sheet添加账套列\n- 合并到总表\n- 删除核算项目为空的行\n- 删除期末余额借方和贷方都为空的行\n- 结果：${filtered2.length}行`,
  attachments: [{ 
    filename: '科目余额表_合并结果.xlsx', 
    path: outputPath 
  }]
});
```
