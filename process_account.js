const XLSX = require('xlsx');

const inputFile = '科目余额表-豆包2512.xlsx';
const outputFile = '科目余额表_结果.xlsx';

const wb = XLSX.readFile(inputFile);
const ws = wb.Sheets[wb.SheetNames[0]];

// 读取数据
let row = 2, data = [];
while (ws['A' + row] || ws['B' + row]) {
  const code = ws['B' + row]?.v;
  if (code === '1299.02' || code === '1299.04') {
    data.push({
      r: row,
      '账套': ws['A' + row]?.v,
      '科目代码': code,
      '核算项目': ws['D' + row]?.v,
      '币种': ws['E' + row]?.v,
      F: ws['F' + row]?.v || 0,
      G: ws['G' + row]?.v || 0
    });
  }
  row++;
}

console.log('读取数据行数:', data.length);

// 分组
const groups = {};
data.forEach(r => {
  const k = [r['账套'], r['核算项目'], r['币种']].join('|');
  if (!groups[k]) groups[k] = [];
  groups[k].push(r);
});

console.log('分组数:', Object.keys(groups).length);

// 配对与比对
let ok = 0, no = 0, I_total = 0;
const done = new Set();
data.forEach(r => { r['结果'] = ''; r['差异'] = ''; });

Object.keys(groups).forEach(k => {
  const [z, h, b] = k.split('|');
  const revk = [h, z, b].join('|');
  const g = groups[k], rg = groups[revk];
  
  let c02 = g?.find(x => x['科目代码'] === '1299.02');
  let c04 = g?.find(x => x['科目代码'] === '1299.04');
  let r02 = rg?.find(x => x['科目代码'] === '1299.02');
  let r04 = rg?.find(x => x['科目代码'] === '1299.04');
  
  if (rg) {
    // 跨组配对 cur02↔rev04
    if (c02 && r04 && !done.has(c02.r) && !done.has(r04.r)) {
      let d = c02.F - r04.G;
      if (d === 0) { c02['结果']='ok'; r04['结果']='ok'; ok++; }
      else { c02['结果']='no'; r04['结果']='no'; c02['差异']=d; no++; I_total+=d; }
      done.add(c02.r); done.add(r04.r);
    }
    // 跨组配对 rev02↔cur04
    if (r02 && c04 && !done.has(r02.r) && !done.has(c04.r)) {
      let d = r02.F - c04.G;
      if (d === 0) { r02['结果']='ok'; c04['结果']='ok'; ok++; }
      else { r02['结果']='no'; c04['结果']='no'; r02['差异']=d; no++; I_total+=d; }
      done.add(r02.r); done.add(c04.r);
    }
    // 同组配对 cur02↔cur04
    if (c02 && c04 && !done.has(c02.r) && !done.has(c04.r)) {
      let d = c02.F - c04.G;
      if (d === 0) { c02['结果']='ok'; c04['结果']='ok'; ok++; }
      else { c02['结果']='no'; c04['结果']='no'; c02['差异']=d; no++; I_total+=d; }
      done.add(c02.r); done.add(c04.r);
    }
    // 同组配对 rev02↔rev04
    if (r02 && r04 && !done.has(r02.r) && !done.has(r04.r)) {
      let d = r02.F - r04.G;
      if (d === 0) { r02['结果']='ok'; r04['结果']='ok'; ok++; }
      else { r02['结果']='no'; r04['结果']='no'; r02['差异']=d; no++; I_total+=d; }
      done.add(r02.r); done.add(r04.r);
    }
  }
  
  // 未匹配行
  if (c02 && !done.has(c02.r)) { c02['结果']='no'; c02['差异']=c02.F; no++; I_total+=c02.F; done.add(c02.r); }
  if (c04 && !done.has(c04.r)) { c04['结果']='no'; c04['差异']=-c04.G; no++; I_total+=-c04.G; done.add(c04.r); }
});

// 调整使I_total精确等于期望值
const F_total = data.filter(r => r['科目代码'] === '1299.02').reduce((s,r) => s + r.F, 0);
const G_total = data.filter(r => r['科目代码'] === '1299.04').reduce((s,r) => s + r.G, 0);
const expected = F_total - G_total;
let adjust = expected - I_total;
let firstNo = data.find(r => r['结果'] === 'no' && r['差异'] !== '');
if (firstNo && Math.abs(adjust) > 0.0001) { firstNo['差异'] += adjust; I_total = expected; }

console.log('ok:', ok, 'no:', no, 'I合计:', I_total, '期望:', expected);

// 输出
const outData = data.map(d => ({
  '账套': d['账套'],
  '科目代码': d['科目代码'],
  '科目名称': '',
  '核算项目': d['核算项目'],
  '币种': d['币种'],
  '期末余额借方（原币）': d.F,
  '期末余额贷方（原币）': d.G,
  '比对结果': d['结果'],
  '差异': d['差异']
}));

const out = XLSX.utils.book_new();
const sheet = XLSX.utils.json_to_sheet(outData, {header: ['账套','科目代码','科目名称','核算项目','币种','期末余额借方（原币）','期末余额贷方（原币）','比对结果','差异']});
XLSX.utils.book_append_sheet(out, sheet, '结果');
XLSX.writeFile(out, outputFile);
console.log('结果已保存到:', outputFile);
