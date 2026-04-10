const XLSX = require('xlsx');

const workbook = XLSX.readFile('/home/leonwan/.openclaw/workspace/科目余额表.xlsx');
const sheetName = workbook.SheetNames[0];
const worksheet = workbook.Sheets[sheetName];
const data = XLSX.utils.sheet_to_json(worksheet, { header: 1 });

const headers = data[0];
const rows = data.slice(1).map((row, idx) => ({ ...row, _rowIdx: idx + 2 }));

const COL_ACCOUNT = 0;
const COL_CODE = 1;
const COL_PROJECT = 3;
const COL_CURRENCY = 4;
const COL_DEBIT = 5;
const COL_CREDIT = 6;
const COL_RESULT = 7;
const COL_DIFF = 8;

const getNum = (val) => {
  if (val === undefined || val === null || val === '') return 0;
  const num = Number(val);
  return isNaN(num) ? 0 : num;
};

const pairs = {};
rows.forEach(row => {
  const key = `${row[COL_ACCOUNT]}|${row[COL_PROJECT]}|${row[COL_CURRENCY]}`;
  if (!pairs[key]) pairs[key] = [];
  pairs[key].push(row);
});

console.log(`找到 ${Object.keys(pairs).length} 个组合`);

let okCount = 0;
let noCount = 0;
const processed = new Set();

for (const [key, groupRows] of Object.entries(pairs)) {
  if (processed.has(key)) continue;
  
  const [account, project, currency] = key.split('|');
  const reverseKey = `${project}|${account}|${currency}`;
  
  if (!pairs[reverseKey]) {
    processed.add(key);
    continue;
  }
  processed.add(key);
  processed.add(reverseKey);
  
  const reverseGroup = pairs[reverseKey];
  
  const getByCode = (list, code) => list.find(r => String(r[COL_CODE]) === code);
  
  const fwd_02 = getByCode(groupRows, '1299.02');
  const fwd_04 = getByCode(groupRows, '1299.04');
  const rev_02 = getByCode(reverseGroup, '1299.02');
  const rev_04 = getByCode(reverseGroup, '1299.04');
  
  // 比较1: A的1299.02借方 vs B的1299.04贷方
  if (fwd_02 && rev_04) {
    const g_val = getNum(fwd_02[COL_DEBIT]);
    const f_val = getNum(rev_04[COL_CREDIT]);
    const diff = f_val - g_val;
    
    if (Math.abs(diff) < 0.01) {
      fwd_02[COL_RESULT] = 'ok';
      okCount++;
    } else {
      fwd_02[COL_RESULT] = 'no';
      fwd_02[COL_DIFF] = diff;
      noCount++;
    }
  }
  
  // 比较2: B的1299.02借方 vs A的1299.04贷方
  if (rev_02 && fwd_04) {
    const g_val = getNum(rev_02[COL_DEBIT]);
    const f_val = getNum(fwd_04[COL_CREDIT]);
    const diff = f_val - g_val;
    
    if (Math.abs(diff) < 0.01) {
      rev_02[COL_RESULT] = 'ok';
      okCount++;
    } else {
      rev_02[COL_RESULT] = 'no';
      rev_02[COL_DIFF] = diff;
      noCount++;
    }
  }
}

// 处理没有对应的行：金额就是差异
console.log("\n处理没有对应的行...");

rows.forEach(row => {
  if (row[COL_RESULT]) return; // 已经有结果
  
  const account = row[COL_ACCOUNT];
  const project = row[COL_PROJECT];
  const currency = row[COL_CURRENCY];
  const code = String(row[COL_CODE]);
  
  const reverseKey = `${project}|${account}|${currency}`;
  const reverseGroup = pairs[reverseKey];
  
  if (!reverseGroup) {
    // 完全没有反向数据
    row[COL_RESULT] = 'no';
    if (code === '1299.02') {
      // 1299.02没有对应，差异 = 0 - G = -G
      row[COL_DIFF] = -getNum(row[COL_DEBIT]);
    } else if (code === '1299.04') {
      // 1299.04没有对应，差异 = F - 0 = F
      row[COL_DIFF] = getNum(row[COL_CREDIT]);
    }
    noCount++;
  }
});

console.log(`最终: ok=${okCount}, no=${noCount}`);

// 验算
let sumF = 0, sumG = 0, sumI = 0;

rows.forEach(row => {
  const code = String(row[COL_CODE]);
  if (code === '1299.04') {
    sumF += getNum(row[COL_CREDIT]);
  } else if (code === '1299.02') {
    sumG += getNum(row[COL_DEBIT]);
  }
  sumI += getNum(row[COL_DIFF]);
});

console.log(`\n验算:`);
console.log(`  F列 = ${sumF.toFixed(2)}`);
console.log(`  G列 = ${sumG.toFixed(2)}`);
console.log(`  F - G = ${(sumF - sumG).toFixed(2)}`);
console.log(`  I列 = ${sumI.toFixed(2)}`);
console.log(`  差异 = ${(sumF - sumG - sumI).toFixed(2)}`);
console.log(`  结果: ${Math.abs((sumF - sumG) - sumI) < 0.01 ? '✓ 通过' : '✗ 未通过'}`);

// 保存结果
const resultData = [headers, ...rows.map(row => [
  row[COL_ACCOUNT],
  row[COL_CODE],
  row[2],
  row[COL_PROJECT],
  row[COL_CURRENCY],
  row[COL_DEBIT],
  row[COL_CREDIT],
  row[COL_RESULT] || '',
  row[COL_DIFF] || ''
])];

const resultSheet = XLSX.utils.aoa_to_sheet(resultData);
const resultWorkbook = XLSX.utils.book_new();
XLSX.utils.book_append_sheet(resultWorkbook, resultSheet, 'Sheet1');
XLSX.writeFile(resultWorkbook, '/home/leonwan/.openclaw/workspace/科目余额表_结果.xlsx');

console.log("\n结果已保存");
