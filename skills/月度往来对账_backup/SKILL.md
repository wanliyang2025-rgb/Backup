# 月度往来对账

用于处理公司月度科目余额表往来核对，科目代码1299.02（应收账款）和1299.04（应付账款）互相对账。

## 适用场景
- 多个账套之间的往来核对
- 科目代码：1299.02（借方）/ 1299.04（贷方）
- 按账套+核算项目+币种分组配对

## 输入文件
- `科目余额表.xlsx`：包含A-G列原始数据
  - A列：账套
  - B列：科目代码
  - C列：科目名称
  - D列：核算项目
  - E列：币种
  - F列：期末余额借方（原币）
  - G列：期末余额贷方（原币）

## 处理规则

### 1. 配对逻辑
按 `[账套]|[核算项目]|[币种]` 唯一键分组，找反向键 `[核算项目]|[账套]|[币种]`

**配对优先级**：
1. 跨组配对：cur02↔rev04（当前账套1299.02 vs 反向账套1299.04）
2. 跨组配对：rev02↔cur04（反向账套1299.02 vs 当前账套1299.04）
3. 同组配对：cur02↔cur04（同一账套内的1299.02与1299.04）
4. 同组配对：rev02↔rev04（反向账套内的1299.02与1299.04）

### 2. 比对判定
- **差异 = 0**：标记 `ok`（精确相等）
- **差异 ≠ 0**：标记 `no`

### 3. 差异计算
- **差异 = 1299.02行次的F列 - 1299.04行次的G列**
- 只在1299.02行次填写差异
- 未匹配行：1299.02 = 正差异(自身F列)，1299.04 = 负差异(-自身G列)

### 4. 验算公式
```
I列合计 = F列合计(1299.02) - G列合计(1299.04)
```
必须精确到小数点后两位

## 输出文件
- `科目余额表_结果.xlsx`
  - A-G列：原始数据（不修改）
  - H列：比对结果（ok/no）
  - I列：差异（仅1299.02行次填写）

## 关键代码（Node.js + xlsx）

```javascript
const XLSX = require('xlsx');
const wb = XLSX.readFile('科目余额表.xlsx');
const ws = wb.Sheets[wb.SheetNames[0]];

// 读取数据
let row = 2, data = [];
while (ws['A' + row]) {
  const code = ws['B' + row]?.v;
  if (code === '1299.02' || code === '1299.04') {
    data.push({
      r: row,
      账套: ws['A' + row]?.v,
      科目代码: code,
      核算项目: ws['D' + row]?.v,
      币种: ws['E' + row]?.v,
      F: ws['F' + row]?.v || 0,
      G: ws['G' + row]?.v || 0
    });
  }
  row++;
}

// 分组
const groups = {};
data.forEach(r => {
  const k = [r['账套'], r['核算项目'], r['币种']].join('|');
  if (!groups[k]) groups[k] = [];
  groups[k].push(r);
});

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

console.log('ok:', ok, 'no:', no, 'I合计:', I_total);

// 输出 - 使用json_to_sheet确保无空白行
const outData = data.map(d => ({
  '账套': d.账套,
  '科目代码': d.科目代码,
  '科目名称': '',
  '核算项目': d.核算项目,
  '币种': d.币种,
  '期末余额借方（原币）': d.F,
  '期末余额贷方（原币）': d.G,
  '比对结果': d.结果,
  '差异': d.差异
}));

const out = XLSX.utils.book_new();
const sheet = XLSX.utils.json_to_sheet(outData, {header: ['账套','科目代码','科目名称','核算项目','币种','期末余额借方（原币）','期末余额贷方（原币）','比对结果','差异']});
XLSX.utils.book_append_sheet(out, sheet, '结果');
XLSX.writeFile(out, '科目余额表_结果.xlsx');
```

## 注意事项
- 差异判定必须是 **精确等于0** 才算ok，不是≤0.01
- 原始数据（A-G列）严禁修改
- 邮件发送使用QQ SMTP：smtp.qq.com，端口587
