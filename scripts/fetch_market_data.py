#!/usr/bin/env python3
"""
统一金融数据获取脚本
数据源: 新浪财经 / 腾讯财经 / 东方财富基金估值
用法:
  python3 fetch_market_data.py gold           # 现货黄金
  python3 fetch_market_data.py indices        # A股指数
  python3 fetch_market_data.py funds          # 持仓基金估值
  python3 fetch_market_data.py stock 600519   # 指定股票
"""

import subprocess
import json
import sys
import re
from datetime import datetime

# ========== 数据源 ==========

def fetch_sina(codes: list[str]) -> dict:
    """新浪财经: 股票/指数/基金实时行情"""
    results = {}
    query = ','.join(codes)
    r = subprocess.run(
        ['curl', '-s', '--max-time', '10',
         f'https://hq.sinajs.cn/list={query}',
         '-H', 'Referer: https://finance.sina.com.cn',
         '-H', 'User-Agent: Mozilla/5.0'],
        capture_output=True
    )
    if r.returncode != 0:
        return {'error': 'request failed'}
    
    raw = r.stdout.decode('gbk', errors='replace')
    # 格式: var hq_str_xxx="名称,现价,涨跌,..."
    for line in raw.split('\n'):
        m = re.search(r'hq_str_(\w+)="([^"]+)"', line)
        if not m:
            continue
        code, data = m.group(1), m.group(2).split(',')
        if len(data) < 6:
            continue
        name = data[0]
        try:
            price = float(data[1])
            prev = float(data[2])
            chg = (price - prev) / prev * 100 if prev else 0
            results[code] = {
                'name': name,
                'price': price,
                'change': chg,
                'source': 'sina'
            }
        except (ValueError, IndexError):
            results[code] = {'name': name, 'raw': data, 'source': 'sina'}
    return results

def fetch_tencent(codes: list[str]) -> dict:
    """腾讯财经: 股票/基金(带f_前缀)实时行情"""
    results = {}
    query = ','.join([f'sh{c}' if not c.startswith(('sh','sz')) else c for c in codes])
    r = subprocess.run(
        ['curl', '-s', '--max-time', '10',
         f'https://qt.gtimg.cn/q={query}',
         '-H', 'Referer: https://finance.qq.com'],
        capture_output=True
    )
    if r.returncode != 0:
        return {'error': 'request failed'}
    
    raw = r.stdout.decode('gbk', errors='replace')
    # 格式: v_sh600519="1~名称~代码~现价~昨收~今开~..."
    for line in raw.split('\n'):
        m = re.search(r'v_(\w+)="([^"]+)"', line)
        if not m:
            continue
        code, data = m.group(1), m.group(2).split('~')
        if len(data) < 10:
            continue
        name = data[1]
        try:
            price = float(data[3])
            prev = float(data[4])
            chg = (price - prev) / prev * 100 if prev else 0
            results[code] = {
                'name': name,
                'price': price,
                'change': chg,
                'source': 'tencent'
            }
        except (ValueError, IndexError):
            results[code] = {'name': name, 'raw': data[:10], 'source': 'tencent'}
    return results

def fetch_eastmoney_fund(fund_code: str) -> dict:
    """东方财富基金估值 API"""
    r = subprocess.run(
        ['curl', '-s', '--max-time', '10',
         f'https://fundgz.1234567.com.cn/js/{fund_code}.js?rt={int(datetime.now().timestamp())}',
         '-H', 'Referer: https://fund.eastmoney.com'],
        capture_output=True
    )
    if r.returncode != 0:
        return {'error': 'request failed'}
    
    raw = r.stdout.decode('utf-8', errors='replace').strip()
    if raw.startswith('jsonpgz'):
        raw = raw.replace('jsonpgz(', '').replace(');', '').replace(');', '')
    try:
        d = json.loads(raw)
        return {
            'name': d.get('name', ''),
            'code': d.get('fundcode', ''),
            'net_value': float(d.get('dwjz', 0)),       # 单位净值
            'est_value': float(d.get('gsz', 0)),         # 估算净值
            'est_change': float(d.get('gszzl', 0)),      # 估算涨跌幅%
            'date': d.get('jzrq', ''),                   # 净值日期
            'update_time': d.get('gztime', ''),          # 估算时间
            'source': 'eastmoney_fund'
        }
    except (json.JSONDecodeError, ValueError, KeyError):
        return {'error': 'parse failed', 'raw': raw[:100]}

# ========== 便捷封装 ==========

def get_gold() -> dict:
    """现货黄金 (XAU/USD 盎司)"""
    data = fetch_sina(['gb_xau'])
    if 'gb_xau' in data:
        return data['gb_xau']
    # fallback: 伦敦金
    data2 = fetch_tencent(['gb_xau'])
    return data2.get('gb_xau', {'error': 'gold data unavailable'})

def get_indices() -> dict:
    """A股主要指数"""
    codes = ['sh000001', 'sz399001', 'sz399006', 'sh000300', 'sh000016']
    return fetch_sina(codes)

def get_fund_est(fund_code: str) -> dict:
    """基金实时估算: 优先EM(有估算), 兜底Sina(收盘价)"""
    # 先试EM
    em = fetch_eastmoney_fund(fund_code)
    if 'est_value' in em and em.get('est_value', 0) > 0 and em.get('est_change', '') != '':
        return em
    # EM无估算，用Sina f_接口
    r = subprocess.run(
        ['curl', '-s', '--max-time', '10',
         f'https://hq.sinajs.cn/list=f_{fund_code}',
         '-H', 'Referer: https://finance.sina.com.cn',
         '-H', 'User-Agent: Mozilla/5.0'],
        capture_output=True
    )
    if r.returncode == 0:
        raw = r.stdout.decode('gbk', errors='replace')
        m = raw.split('"')[1] if '"' in raw else ''
        if m:
            parts = m.split(',')
            if len(parts) >= 3:
                try:
                    price = float(parts[1])
                    prev = float(parts[2])
                    chg = (price - prev) / prev * 100 if prev else 0
                    return {
                        'code': fund_code,
                        'name': parts[0],
                        'price': price,
                        'prev': prev,
                        'change': chg,
                        'source': 'sina'
                    }
                except (ValueError, IndexError):
                    pass
    return {'error': f'no data for {fund_code}'}

def get_stock_price(code: str) -> dict:
    """个股价格 (支持 sh/sz 前缀)"""
    if not code.startswith(('sh', 'sz')):
        code = ('sh' if code.startswith(('6', '5')) else 'sz') + code
    data = fetch_sina([code])
    return data.get(code.lower(), {'error': f'{code} not found'})

def format_result(data: dict, label: str = '') -> str:
    """格式化输出"""
    if 'error' in data:
        return f"❌ {label}: {data['error']}"
    
    if 'price' in data:
        chg = data['change']
        emoji = '📈' if chg >= 0 else '📉'
        sign = '+' if chg >= 0 else ''
        return f"{emoji} {data['name']}: {data['price']} ({sign}{chg:.2f}%) [新浪]"
    
    if 'est_value' in data:
        chg = data['est_change']
        emoji = '📈' if chg >= 0 else '📉'
        sign = '+' if chg >= 0 else ''
        return (f"{emoji} {data['name']}({data['code']}): "
                f"估算净值={data['est_value']}({sign}{chg}%) | "
                f"单位净值={data['net_value']} | "
                f"更新时间={data['update_time']} [东方财富]")
    
    return f"✅ {label}: {data}"

# ========== 命令行入口 ==========

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'help'
    fund_codes = {
        '红利': '501029',   # 华宝标普中国A股红利机会ETF联接A(LOF)
        'AI': '008585',     # 华夏人工智能ETF联接A
        '标普500': '050025', # 博时标普500ETF联接A
        '纳指': '160213',    # 国泰纳斯达克100指数
    }

    if cmd == 'gold':
        print(format_result(get_gold(), '现货黄金'))
    
    elif cmd == 'indices':
        print("=== A股指数 ===")
        for code, name in [('sh000001','上证'),('sz399001','深证'),('sz399006','创业板'),('sh000300','沪深300'),('sh000016','上证50')]:
            r = fetch_sina([code]).get(code, {})
            if 'price' in r:
                chg = r['change']
                emoji = '📈' if chg >= 0 else '📉'
                sign = '+' if chg >= 0 else ''
                print(f"  {emoji} {r['name']}: {r['price']} ({sign}{chg:.2f}%)")

    elif cmd == 'funds':
        print("=== 持仓基金估值 ===")
        for name, code in fund_codes.items():
            r = get_fund_est(code)
            print(f"  {format_result(r, name)}")

    elif cmd == 'stock' and len(sys.argv) > 2:
        code = sys.argv[2]
        print(format_result(get_stock_price(code), code))

    elif cmd == 'all':
        print(f"=== 市场数据 {datetime.now().strftime('%Y-%m-%d %H:%M')} ===\n")
        print("【黄金】")
        print(format_result(get_gold(), '现货黄金'), '\n')
        print("【A股指数】")
        for code, name in [('sh000001','上证'),('sz399006','创业板'),('sh000300','沪深300')]:
            r = fetch_sina([code]).get(code, {})
            if 'price' in r:
                chg = r['change']
                emoji = '📈' if chg >= 0 else '📉'
                sign = '+' if chg >= 0 else ''
                print(f"  {emoji} {r['name']}: {r['price']} ({sign}{chg:.2f}%)")
        print("\n【持仓基金】")
        for name, code in fund_codes.items():
            r = get_fund_est(code)
            print(f"  {format_result(r, name)}")

    else:
        print(__doc__)
