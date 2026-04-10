#!/usr/bin/env python3
"""Create Feishu doc for daily report 2026-03-28"""

import json
import urllib.request
import urllib.error

DOC_ID = "T7t5dpD1ooj41bx2nhxclImHnig"

def get_token():
    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        data=json.dumps({"app_id": "cli_a93b3aa665789cc2", "app_secret": "d4lvhry3RZcCtDfGekHbyeNTy00TXjv0"}).encode(),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())["tenant_access_token"]

def add_blocks(token, blocks, index=None):
    payload = {"children": blocks}
    if index is not None:
        payload["index"] = index
    req = urllib.request.Request(
        f"https://open.feishu.cn/open-apis/docx/v1/documents/{DOC_ID}/blocks/{DOC_ID}/children",
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read())

def text_run(content, bold=False):
    el = {"type": "text_run", "text_run": {"content": content}}
    if bold:
        el["text_run"]["bold"] = True
    return el

def para(elements):
    if isinstance(elements, str):
        elements = [text_run(elements)]
    return {"block_type": 2, "text": {"elements": elements, "style": {}}}

def heading(level, content):
    bt = {1: 3, 2: 4, 3: 5}.get(level, 3)
    key = f"heading{level}"
    return {"block_type": bt, key: {"elements": [text_run(content)], "style": {}}}

def bullet(content):
    el = text_run(content)
    return {"block_type": 12, "bullet": {"elements": [el], "style": {}}}

def callout(content):
    """Callout block - bg_color 2=blue, 4=yellow, 5=green, 6=red"""
    return {
        "block_type": 34,
        "callout": {
            "emoji_id": "💡",
            "background_color": 2,
            "border_color": 2,
            "elements": [text_run(content)]
        }
    }

def divider():
    return {"block_type": 25, "divider": {}}

token = get_token()
print("Token obtained")

blocks = []

# === Section 1: AI/科技 热点新闻（5条）===
blocks.append(heading(1, "📰 AI/科技 热点新闻（5条）"))
blocks.append(divider())

# News 1
blocks.append(heading(2, "1. 2026中关村论坛：众智FlagOS 2.0发布"))
blocks.append(para([text_run("一句话解读："), text_run("中国23家机构联合发布面向多AI芯片的统一开源系统软件FlagOS 2.0，并发布全球主权AI白皮书，意味着中国正从\"AI应用大国\"向\"AI基础设施强国\"深度转型，主权AI已成为全球博弈新维度。", bold=False)]))

# News 2
blocks.append(heading(2, "2. \"词元\"成为Token官方中文名"))
blocks.append(para([text_run("一句话解读：全国科学技术名词审定委员会正式将AI领域token定名为\"词元\"并发布试用，标志着国家层面对AI基础术语规范化的高度重视，AI名词体系\"中国化\"迈出里程碑一步。")]))

# News 3
blocks.append(heading(2, "3. 微软与OpenAI关系降温，亚马逊500亿美元入局"))
blocks.append(para([text_run("一句话解读：OpenAI与亚马逊建立战略合作并获500亿美元投资，微软与OpenAI\"甜蜜期\"结束。AWS将成为OpenAI Frontier独家第三方云分发渠道，云厂商的AI站队正在加速洗牌。")]))

# News 4
blocks.append(heading(2, "4. Token调用量今年预计增长100倍，中国或成世界Token工厂"))
blocks.append(para([text_run("一句话解读：小米MiMo负责人罗福莉的判断揭示关键趋势：OpenClaw等Agent框架让AI从\"对话机器人\"进化为\"任务执行者\"，词元消耗从\"对话\"走向\"任务\"，算力/推理芯片/能源成为新一轮竞争焦点。")]))

# News 5
blocks.append(heading(2, "5. Meta开源TRIBE v2：AI精准预测人类大脑多模态反应"))
blocks.append(para([text_run("一句话解读：Meta开源的TRIBE v2模型可无需实际测量即可预测大脑对图像/声音/文本的反应，将AI与神经科学深度融合，开创\"AI读脑\"研究新范式。")]))

# === Section 2: 金融市场动态 ===
blocks.append(divider())
blocks.append(heading(1, "📈 金融市场动态"))
blocks.append(divider())

blocks.append(heading(2, "核心数据一览"))
blocks.append(para([text_run("A股（3月25日收盘）：", bold=True), text_run("上证 +1.30% → 3931.84 | 深证 +1.95% → 13801 | 创业板 +2.01% → 3316.97 | 科创50 +1.91% → 1315.41 | 沪深300 +1.40% → 4537.47")]))
blocks.append(para([text_run("港股（3月25日收盘）：", bold=True), text_run("恒生 +1.09% → 25335.95 | 恒生科技 +1.91% → 4922.94")]))
blocks.append(para([text_run("美股（3月25日收盘）：", bold=True), text_run("道指 +0.66% → 46428 | 纳指 +0.77% → 21929 | 标普500 +0.54% → 6591")]))
blocks.append(para([text_run("欧洲主要指数：", bold=True), text_run("德国DAX +1.49% | 英国富时 +1.47% | 法国CAC +1.33%")]))

blocks.append(heading(2, "关键逻辑解读"))
blocks.append(bullet("华尔街三大预警信号同时拉响：IEEPA关税可能被推翻 + 美联储主席人选不确定性 + AI泡沫担忧——历史上每次三大预警同时出现都伴随两位数级别跌幅"))
blocks.append(bullet("AI巨头资本支出创历史高位：2025Q3 AI五巨头合计Capex达1057亿美元（同比+72.9%），自由现金流覆盖率下滑，Meta仅37.3%，存在明显流动性风险"))
blocks.append(bullet("甲骨文、Coreweave等公司信用违约掉期(CDS)利差扩大，私募信贷市场隐含风险不断累积"))
blocks.append(bullet("A股/港股/欧股周三整体反弹，显示全球资金在地缘风险下向非美资产分散配置"))
blocks.append(bullet("中国1-2月规模以上工业企业利润同比+15.2%，实体经济基本面仍有韧性")

# === Section 3: 深度解读 ===
blocks.append(divider())
blocks.append(heading(1, "💭 深度解读：今日最重要的一件事"))
blocks.append(divider())

blocks.append(callout("AI竞争从\"模型能力\"转向\"规模基础设施\"——词元调用量百倍增长、万亿瓦算力投产、\"能源即算力\"成新竞争逻辑。"))

blocks.append(heading(2, "这件事意味着什么？"))
blocks.append(para("今天最值得关注的事件，不是某个模型发布，而是一个趋势的确认：AI竞争的焦点，正在从\"谁家模型更强\"转向\"谁家有更多的算力和能源\"。"))
blocks.append(para([text_run("三个维度的变化：", bold=True)]))
blocks.append(bullet("需求侧：罗福莉预测\"今年Token调用量增长100倍\"——OpenClaw等Agent框架让AI从工具变执行者，词元消耗从\"对话\"走向\"任务自动化\""))
blocks.append(bullet("供给侧：马斯克TeaFab项目（年产能1万亿瓦AI算力，80%用于太空算力中心）；科大讯飞AIPC华东基地投产（年产能10万台），中国制造优势向AI硬件延伸"))
blocks.append(bullet("能源侧：从\"算法竞争\"到\"能源竞争\"——推理芯片、绿电智算、太空算力，所有新维度竞争都在指向核心瓶颈：电"))

blocks.append(para([text_run("背后更深的含义：", bold=True), text_run("AI正在进入\"工业革命式\"发展阶段——真正释放价值需要组织重构。就像19世纪电力革命初期，工厂只是简单替换了蒸汽机，AI的\"组织重构\"时刻正在到来。")]))

blocks.append(heading(2, "我从中学到了什么？"))
blocks.append(para("作为数据分析师，这个转变对我有两层意义："))
blocks.append(bullet("第一：数据分析的价值锚点在变——以前看\"模型指标\"（准确率、参数量），未来要看\"规模运营指标\"（词元消耗、推理成本、响应延迟），这些才是业务决策真正需要的"))
blocks.append(bullet("第二：避免\"技术傲娇\"——不是最新最炫的模型才有价值，能稳定支撑大规模应用的\"成熟\"技术栈，往往更可靠"))
blocks.append(para([text_run("最重要的认知更新：", bold=True), text_run("AI行业现在类似2015-2016年的云计算——真正赚到钱的不是\"最技术的\"，而是\"最能规模化、最能落地\"的。下一个周期，属于能把AI用到产业深处的人。")]))

blocks.append(heading(2, "值得关注的3个信号"))

callout_blocks = [
    ("🔔", "信号1：关注Token消耗量——如果业务中词元消耗出现10x级别增长，通常意味着应用范式正在发生质变，而非简单的用户增加。这是判断AI应用价值的领先指标。"),
    ("🔔", "信号2：关注AI公司的\"现金覆盖率\"——Meta的现金覆盖率只有37.3%，当AI叙事无法兑现为现金流时，行业会进入\"信仰修正\"期。这往往是最好的买入时机，也是最危险的分析陷阱。"),
    ("🔔", "信号3：关注能源基础设施——特斯拉太空算力、中国\"绿电智算\"等能源成本将成为AI规模化的硬约束。数据中心、电网、储能相关公司的异动，往往是AI行情的领先指标而非跟随指标。"),
]

for emoji, text in callout_blocks:
    blocks.append({"block_type": 34, "callout": {"emoji_id": emoji, "background_color": 3, "border_color": 3, "elements": [text_run(text)]}})

blocks.append(divider())

# === Section 4: 工作日报 ===
blocks.append(heading(1, "📋 工作日报"))
blocks.append(divider())

blocks.append(heading(2, "今日完成"))

blocks.append(para([text_run("1. 日报生成流程梳理", bold=True)]))
blocks.append(bullet("明确日报生成的完整流程：新闻搜索→信息整理→深度解读→飞书文档创建→发送"))
blocks.append(bullet("掌握Feishu API直接调用方法（tenant_access_token → 文档创建 → blocks API写入）"))
blocks.append(bullet("沉淀可复用日报生成脚本：~/.openclaw/workspace/scripts/create_report_doc.py"))

blocks.append(para([text_run("2. 金融市场数据获取", bold=True)]))
blocks.append(bullet("通过Tavily搜索获取今日金融市场的关键数据"))
blocks.append(bullet("整理A股/港股/美股/欧股主要指数表现，建立每日金融市场数据收集SOP"))

blocks.append(para([text_run("3. AI行业深度研究", bold=True)]))
blocks.append(bullet("阅读宋雪涛\"AI泡沫的内部熔点与外部拐点\"深度分析"))
blocks.append(bullet("建立对AI投资\"铁索连环\"结构脆弱性的系统性认知框架"))

blocks.append(heading(2, "经验反思"))
blocks.append({"block_type": 34, "callout": {"emoji_id": "🤔", "background_color": 3, "border_color": 3, "elements": [text_run("做得不够好的地方：今天在生成报告时，前期信息收集花费时间较长（多次搜索尝试），原因是Brave搜索API未配置。下次应该在TOOLS.md中提前标注可用的搜索工具优先级（Tavily/multi-search-engine）。")]}})

blocks.append(para([text_run("回头看可以更好的决定：", bold=True)]))
blocks.append(para("今天的新闻收集策略可以更高效——我同时搜索了多个关键词（AI/金融），但没有优先级排序。如果重新来过，我会先明确\"今日最重要的一件事\"，然后围绕这件事做深度挖掘，而不是追求新闻的广度。这与深度>广度的原则是一致的。"))

blocks.append(heading(2, "明日规划"))
blocks.append(bullet("继续完善日报生成的自动化程度，尝试将Python脚本注册为可复用工具"))
blocks.append(bullet("深入研究AI基础设施赛道的投资逻辑，特别是能源与算力结合的方向"))
blocks.append(bullet("跟进中国银行AI产业链授信超5500亿元这一数据背后的产业影响"))
blocks.append(bullet("思考如何将AI数据分析能力转化为可落地的产品或服务"))

blocks.append(divider())

# Footer
blocks.append(para([text_run("---", False)]))
blocks.append(para([text_run("📅 报告生成时间：2026年3月28日 18:00（北京时间）", False)]))
blocks.append(para([text_run("🤖 由 鱼丸（AI助手）自动生成 | 数据来源：新浪、Tavily、华尔街见闻、金十数据", False)]))

print(f"Total blocks to add: {len(blocks)}")

# Split into batches of 50
batch_size = 50
for i in range(0, len(blocks), batch_size):
    batch = blocks[i:i+batch_size]
    result = add_blocks(token, batch)
    code = result.get('code')
    if code != 0:
        print(f"Batch {i//batch_size + 1}: code={code}, msg={result.get('msg','')}")
        # Print field violations if any
        if 'error' in result and 'field_violations' in result.get('error', {}):
            for v in result['error']['field_violations']:
                print(f"  Violation: {v}")
        break
    else:
        print(f"Batch {i//batch_size + 1}: Added {len(batch)} blocks ✓")
