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

// 分析所有数据，看看 F-G 的分布
let f_only_sum = 0; // 只有F有值
let g_only_sum = 0; // 只有G有值
let both_sum_f = 0; // 两个都有，F列
let both_sum_g = 0; // 两个都有，G列
let count_f_only = 0, count_g_only = 0, count_both = 0;

rows.forEach(row => {
  const code = String(row[COL_CODE]);
  const f = getNum(row[COL_CREDIT]);
  const g = getNum(row[COL_DEBIT]);
  
  if (code === '1299.04') {
    if (f > 0 && g === 0) {
      f_only_sum += f;
      count_f_only++;
    } else if (f > 0 || g > 0) {
      both_sum_f += f;
      both_sum_g += g;
      count_both++;
    }
  }
});

console.log("1299.04数据分析:");
console.log(`  只有F有值: ${count_f_only}行, 金额=${f_only_sum.toFixed(2)}`);
console.log(`  F和G都有值: ${count_both}行, F合计=${both_sum_f.toFixed(2)}, G合计=${both_sum_g.toFixed(2)}`);
console.log(`  F - G = ${(both_sum_f - both_sum_g).toFixed(2)}`);

console.log("\n现在检查：是不是有些1299.04没有对应的1299.02？");

// 看看有多少1299.04行没有对应的1299.02
const pairs = {};
rows.forEach(row => {
  const key = `${row[COL_ACCOUNT]}|${row[COL_PROJECT]}|${row[COL_CURRENCY]}`;
  if (!pairs[key]) pairs[key] = [];
  pairs[key].push(row);
});

let unmatched_04 = 0;
let unmatched_04_sum = 0;

for (const [key, groupRows] of Object.entries(pairs)) {
  const [account, project, currency] = key.split('|');
  const reverseKey = `${project}|${account}|${currency}`;
  
  const has02 = groupRows.some(r => String(r[COL_CODE]) === '1299.02');
  const has04 = groupRows.some(r => String(r[COL_CODE]) === '1299.04');
  
  // 如果这组有1299.04但没有对应的反方向1299.02
  if (has04 && !pairs[reverseKey]) {
    const row04 = groupRows.find(r => String(r[COL_CODE]) === '1299.04');
    unmatched_04++;
    unmatched_04_sum += getNum(row04[COL_CREDIT]);
  }
}

console.log(`  没有对应1299.02的1299.04行: ${unmatched_04}行, 贷方合计=${unmatched_04_sum.toFixed(2)}`);
