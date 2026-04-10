#!/usr/bin/env python3
"""
data-analyst 技能自我进化脚本
每月运行一次：搜索趋势数据，分析评分，写入候选知识库

评分公式：
  综合分 = 实用性×2 + 稳定性 + 热度 + (5-学习成本)×2
  范围：0-20，≥14 分入选

运行方式（isolated session）：
  openclaw run scripts/evolution/research_trends.py
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

TRENDS_FILE = Path(__file__).parent.parent / "trends_candidates.md"
TRACKING_FILE = Path(__file__).parent.parent / "evolution_log.json"
MAX_TOPICS = 10


def load_log():
    if TRACKING_FILE.exists():
        with open(TRACKING_FILE) as f:
            return json.load(f)
    return {"last_run": None, "candidates": [], "accepted": []}


def save_log(log):
    with open(TRACKING_FILE, "w") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)


def score_topic(name, description, maturity, learning_curve, popularity):
    """
    评分维度：
    - 实用性 (1-5): 这个技术在实际分析中的价值
    - 稳定性 (1-5): 是否成熟稳定，还是炒作阶段
    - 热度 (1-5): 社区关注度和活跃程度
    - 学习成本 (1-5): 越低越好，1=几小时可上手，5=需要大量时间
    """
    utility = min(max(实用性_from_desc(description, name), 1), 5)
    stability = min(max(maturity, 1), 5)
    trending = min(max(popularity, 1), 5)
    learn_cost = min(max(learning_curve, 1), 5)

    total = utility * 2 + stability + trending + (5 - learn_cost) * 2
    return round(total, 1), {
        "utility": utility,
        "stability": stability,
        "trending": trending,
        "learning_cost": learn_cost
    }


def 实用性_from_desc(desc, name):
    """根据描述估算实用性"""
    high_value = ["pandas", "sql", "jupyter", "可视化", "dashboard",
                  "api", "数据清洗", "自动化", "报表", "pipeline",
                  "etl", "dbt", "duckdb", "polars"]
    medium = ["机器学习", "ml", "统计", "时间序列", "forecast",
              "spark", "分布式", "大数据", "可视化"]
    desc_lower = (desc + name).lower()
    if any(k in desc_lower for k in high_value):
        return 5
    if any(k in desc_lower for k in medium):
        return 4
    return 3


def format_candidate(name, description, score, details, source):
    badge = "🔥 HOT" if score >= 16 else ("✅ OK" if score >= 14 else f"{score}")
    date = datetime.now().strftime("%Y-%m-%d")
    return f"""## {badge} {name}（综合分: {score}/20）

**来源:** {source}  
**评分明细:** 实用性={details['utility']} 稳定性={details['stability']} 热度={details['trending']} 学习成本={details['learning_cost']}/5

{description}

---
"""


def main():
    log = load_log()
    log["last_run"] = datetime.now().isoformat()

    print("=== data-analyst 技能自我进化 ===")
    print(f"运行时间: {log['last_run']}")
    print("注：实际搜索需要联网工具，此脚本为框架演示")
    print(f"评分标准：综合分≥14写入候选知识库")
    print(f"输出文件: {TRENDS_FILE}")

    # 演示候选（实际运行时由 subagent 填充真实数据）
    demo_candidates = []

    # 这里输出框架，实际内容由 subagent 填充
    with open(TRENDS_FILE, "w", encoding="utf-8") as f:
        f.write(f"# data-analyst 趋势候选知识库\n\n")
        f.write(f"> 自动生成 | 最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write("**评分规则:** 综合分 = 实用性×2 + 稳定性 + 热度 + (5-学习成本)×2，满分20，≥14入选\n\n")
        f.write("---\n\n")
        f.write("## 待评审候选\n\n")
        for c in demo_candidates:
            f.write(c)
        f.write("\n## 已接受项（已加入 SKILL.md）\n\n")
        for a in log.get("accepted", []):
            f.write(f"- {a}\n")

    save_log(log)
    print(f"完成，共{len(demo_candidates)}个候选写入待评审区")


if __name__ == "__main__":
    main()
