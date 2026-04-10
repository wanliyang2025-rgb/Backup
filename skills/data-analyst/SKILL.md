---
name: data-analyst
version: 1.1.0
description: "Data visualization, report generation, SQL queries, and spreadsheet automation. Transform your AI agent into a data-savvy analyst that turns raw data into actionable insights."
author: openclaw
update_history: |
  2026-04-09 v1.1.0 新增Polars/DuckDB/PyArrow后端/AI辅助分析/dbt等2026主流技术
  2026-04-09 v1.0.0 初始版本
---

# Data Analyst Skill 📊

> **技能进化状态:** v1.1.0 | 下次趋势更新: 2026-05-07
> 趋势候选库: `scripts/evolution/trends_candidates.md`

**Turn your AI agent into a data analysis powerhouse.**

Query databases, analyze spreadsheets, create visualizations, and generate insights that drive decisions.

---

## What This Skill Does

✅ **SQL Queries** — Write and execute queries against databases
✅ **Spreadsheet Analysis** — Process CSV, Excel, Google Sheets data
✅ **Data Visualization** — Create charts, graphs, and dashboards
✅ **Report Generation** — Automated reports with insights
✅ **Data Cleaning** — Handle missing data, outliers, formatting
✅ **Statistical Analysis** — Descriptive stats, trends, correlations

---

## Quick Start

1. Configure your data sources in `TOOLS.md`:
```markdown
### Data Sources
- Primary DB: [Connection string or description]
- Spreadsheets: [Google Sheets URL / local path]
- Data warehouse: [BigQuery/Snowflake/etc.]
```

2. Set up your workspace:
```bash
./scripts/data-init.sh
```

3. Start analyzing!

---

## SQL Query Patterns

### Common Query Templates

**Basic Data Exploration**
```sql
-- Row count
SELECT COUNT(*) FROM table_name;

-- Sample data
SELECT * FROM table_name LIMIT 10;

-- Column statistics
SELECT 
    column_name,
    COUNT(*) as count,
    COUNT(DISTINCT column_name) as unique_values,
    MIN(column_name) as min_val,
    MAX(column_name) as max_val
FROM table_name
GROUP BY column_name;
```

**Time-Based Analysis**
```sql
-- Daily aggregation
SELECT 
    DATE(created_at) as date,
    COUNT(*) as daily_count,
    SUM(amount) as daily_total
FROM transactions
GROUP BY DATE(created_at)
ORDER BY date DESC;

-- Month-over-month comparison
SELECT 
    DATE_TRUNC('month', created_at) as month,
    COUNT(*) as count,
    LAG(COUNT(*)) OVER (ORDER BY DATE_TRUNC('month', created_at)) as prev_month,
    (COUNT(*) - LAG(COUNT(*)) OVER (ORDER BY DATE_TRUNC('month', created_at))) / 
        NULLIF(LAG(COUNT(*)) OVER (ORDER BY DATE_TRUNC('month', created_at)), 0) * 100 as growth_pct
FROM transactions
GROUP BY DATE_TRUNC('month', created_at)
ORDER BY month;
```

**Cohort Analysis**
```sql
-- User cohort by signup month
SELECT 
    DATE_TRUNC('month', u.created_at) as cohort_month,
    DATE_TRUNC('month', o.created_at) as activity_month,
    COUNT(DISTINCT u.id) as users
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY cohort_month, activity_month
ORDER BY cohort_month, activity_month;
```

**Funnel Analysis**
```sql
-- Conversion funnel
WITH funnel AS (
    SELECT
        COUNT(DISTINCT CASE WHEN event = 'page_view' THEN user_id END) as views,
        COUNT(DISTINCT CASE WHEN event = 'signup' THEN user_id END) as signups,
        COUNT(DISTINCT CASE WHEN event = 'purchase' THEN user_id END) as purchases
    FROM events
    WHERE date >= CURRENT_DATE - INTERVAL '30 days'
)
SELECT 
    views,
    signups,
    ROUND(signups * 100.0 / NULLIF(views, 0), 2) as signup_rate,
    purchases,
    ROUND(purchases * 100.0 / NULLIF(signups, 0), 2) as purchase_rate
FROM funnel;
```

---

## Data Cleaning

### Common Data Quality Issues

| Issue | Detection | Solution |
|-------|-----------|----------|
| **Missing values** | `IS NULL` or empty string | Impute, drop, or flag |
| **Duplicates** | `GROUP BY` with `HAVING COUNT(*) > 1` | Deduplicate with rules |
| **Outliers** | Z-score > 3 or IQR method | Investigate, cap, or exclude |
| **Inconsistent formats** | Sample and pattern match | Standardize with transforms |
| **Invalid values** | Range checks, referential integrity | Validate and correct |

### Data Cleaning SQL Patterns

```sql
-- Find duplicates
SELECT email, COUNT(*)
FROM users
GROUP BY email
HAVING COUNT(*) > 1;

-- Find nulls
SELECT 
    COUNT(*) as total,
    SUM(CASE WHEN email IS NULL THEN 1 ELSE 0 END) as null_emails,
    SUM(CASE WHEN name IS NULL THEN 1 ELSE 0 END) as null_names
FROM users;

-- Standardize text
UPDATE products
SET category = LOWER(TRIM(category));

-- Remove outliers (IQR method)
WITH stats AS (
    SELECT 
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY value) as q1,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY value) as q3
    FROM data
)
SELECT * FROM data, stats
WHERE value BETWEEN q1 - 1.5*(q3-q1) AND q3 + 1.5*(q3-q1);
```

### Data Cleaning Checklist

```markdown
# Data Quality Audit: [Dataset]

## Row-Level Checks
- [ ] Total row count: [X]
- [ ] Duplicate rows: [X]
- [ ] Rows with any null: [X]

## Column-Level Checks
| Column | Type | Nulls | Unique | Min | Max | Issues |
|--------|------|-------|--------|-----|-----|--------|
| [col] | [type] | [n] | [n] | [v] | [v] | [notes] |

## Data Lineage
- Source: [Where data came from]
- Last updated: [Date]
- Known issues: [List]

## Cleaning Actions Taken
1. [Action and reason]
2. [Action and reason]
```

---

## Spreadsheet Analysis

### CSV/Excel Processing with Python

```python
import pandas as pd

# Load data
df = pd.read_csv('data.csv')  # or pd.read_excel('data.xlsx')

# Basic exploration
print(df.shape)  # (rows, columns)
print(df.info())  # Column types and nulls
print(df.describe())  # Numeric statistics

# Data cleaning
df = df.drop_duplicates()
df['date'] = pd.to_datetime(df['date'])
df['amount'] = df['amount'].fillna(0)

# Analysis
summary = df.groupby('category').agg({
    'amount': ['sum', 'mean', 'count'],
    'quantity': 'sum'
}).round(2)

# Export
summary.to_csv('analysis_output.csv')
```

### Common Pandas Operations

```python
# Filtering
filtered = df[df['status'] == 'active']
filtered = df[df['amount'] > 1000]
filtered = df[df['date'].between('2024-01-01', '2024-12-31')]

# Aggregation
by_category = df.groupby('category')['amount'].sum()
pivot = df.pivot_table(values='amount', index='month', columns='category', aggfunc='sum')

# Window functions
df['running_total'] = df['amount'].cumsum()
df['pct_change'] = df['amount'].pct_change()
df['rolling_avg'] = df['amount'].rolling(window=7).mean()

# Merging
merged = pd.merge(df1, df2, on='id', how='left')
```

---

## 🚀 2026数据分析主流技术（v1.1.0 新增）

### Pandas PyArrow 后端 — 零成本性能翻倍

**核心改动：** 只需改一行参数，现有Pandas代码性能提升2-5倍，内存减少50-70%。

```python
import pandas as pd

# 旧写法
df = pd.read_csv("data.csv")

# 2026标准写法（推荐）
df = pd.read_csv(
    "data.csv",
    engine="pyarrow",          # 使用PyArrow引擎，比默认NumPy快
    dtype_backend="pyarrow"     # string类型内存降低70%
)

# 输出Parquet（替代CSV，读取快10倍）
df.to_parquet("data.parquet", engine="pyarrow")
df = pd.read_parquet("data.parquet", dtype_backend="pyarrow")
```

**为什么重要：** Pandas仍是数据分析最大众的工具，但2.0+的PyArrow后端让每个会Pandas的人零成本升级。不换库、不重写，速度直接上一个台阶。

---

### Polars — Pandas的性能升级替代

**什么时候用Polars：**
- 数据量超过100万行Pandas开始卡
- 需要惰性求值（lazy evaluation）自动优化查询
- 大文件需要流式处理（streaming）不撑内存

```python
import polars as pl

# 读取（自动多核并行）
df = pl.read_csv("large_data.csv")

# 惰性模式（先构建计算图，最后collect才执行）
q = (
    pl.scan_csv("huge_file.csv")
    .filter(pl.col("status") == "active")
    .group_by("region")
    .agg([
        pl.col("amount").sum().alias("total"),
        pl.col("id").count().alias("count")
    ])
)
result = q.collect()  # 执行

# 流式处理（>内存放不下时）
for chunk in pl.scan_csv("very_large.csv", chunk_size=100_000):
    process(chunk)  # 分块处理，不爆内存

# Polars ↔ Pandas 互转
pandas_df = polars_df.to_pandas()
polars_df = pl.from_pandas(pandas_df)
```

**评分:** 实用性★★★★★ | 稳定性★★★★ | 热度★★★★★ | 学习成本★★★ | **综合: 23/20**

---

### DuckDB — SQL分析无需数据库

**什么时候用DuckDB：**
- 想用SQL但不想搭数据库服务器
- 对超大CSV文件（GB级别）直接跑SQL
- 团队多语言（R/Python/SQL）混用

```python
import duckdb

# 直接对CSV文件跑SQL（不需要导入数据）
result = duckdb.sql("""
    SELECT 
        DATE_TRUNC('month', order_date) as month,
        category,
        SUM(amount) as revenue,
        COUNT(DISTINCT customer_id) as customers
    FROM 'orders.csv'
    WHERE order_date >= '2024-01-01'
    GROUP BY 1, 2
    ORDER BY 1 DESC, 3 DESC
""").df()  # 返回Pandas DataFrame

# DuckDB + Polars 混用（SQL聚合 + DataFrame转换）
agg = duckdb.sql("""
    SELECT region, SUM(revenue) as total
    FROM 'sales.csv'
    GROUP BY region
""").pl()  # 返回Polars DataFrame

# 内存限制（防爆）
duckdb.sql("SET memory_limit = '1GB'")
```

**评分:** 实用性★★★★★ | 稳定性★★★★ | 热度★★★★★ | 学习成本★★★ | **综合: 23/20**

---

### AI辅助数据分析

**什么时候用：**
- 拿到陌生数据集，需要快速了解结构
- 需要写复杂SQL/Python但不确定最优写法
- 数据异常需要AI帮你发现规律

**用法示例（自然语言转代码）：**
```
# 任务描述
"帮我分析这个CSV：
1. 有多少行数据
2. 缺失值情况
3. 金额列的分布（均值、中位数、分位数）
4. 按月份汇总金额"

# AI帮你生成对应Python/Pandas代码
```

**常用AI数据分析工具：**
- Claude Data Analysis (claude.ai/code) — 解读数据、生成代码、发现异常
- ChatGPT Advanced Data Analysis — 数据清洗+可视化
- Hex AI — 团队协作式数据分析平台

**注意：** AI生成代码必须人工审核数据逻辑，不要直接信任数字。

---

### dbt — SQL数据建模框架

**什么时候用：**
- 团队使用数据仓库（BigQuery/Snowflake/StarRocks/Redshift）
- 需要可复用、可测试的数据模型
- 想让数据转换像代码一样做版本控制和code review

**核心概念：**
```sql
-- dbt模型文件（models/次级转化/monthly_revenue.sql）
SELECT
    DATE_TRUNC('month', order_date) AS month,
    customer_id,
    SUM(amount) AS lifetime_value
FROM {{ ref('stg_orders') }}  -- 引用其他模型
WHERE status = 'completed'
GROUP BY 1, 2

-- dbt内置测试（模型质量保证）
models:
  monthly_revenue:
    columns:
      - name: month
        tests:
          - unique
          - not_null
```

**评分:** 实用性★★★★★ | 稳定性★★★★ | 热度★★★★★ | 学习成本★★★ | **综合: 23/20**
（如果你有数据仓库，dbt是2026年标配）

---

## Data Visualization

### Chart Selection Guide

| Data Type | Best Chart | Use When |
|-----------|------------|----------|
| Trend over time | Line chart | Showing patterns/changes over time |
| Category comparison | Bar chart | Comparing discrete categories |
| Part of whole | Pie/Donut | Showing proportions (≤5 categories) |
| Distribution | Histogram | Understanding data spread |
| Correlation | Scatter plot | Relationship between two variables |
| Many categories | Horizontal bar | Ranking or comparing many items |
| Geographic | Map | Location-based data |

### Python Visualization with Matplotlib/Seaborn

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# Line chart (trends)
plt.figure(figsize=(10, 6))
plt.plot(df['date'], df['value'], marker='o')
plt.title('Trend Over Time')
plt.xlabel('Date')
plt.ylabel('Value')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('trend.png', dpi=150)

# Bar chart (comparisons)
plt.figure(figsize=(10, 6))
sns.barplot(data=df, x='category', y='amount')
plt.title('Amount by Category')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('comparison.png', dpi=150)

# Heatmap (correlations)
plt.figure(figsize=(10, 8))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Matrix')
plt.tight_layout()
plt.savefig('correlation.png', dpi=150)
```

### ASCII Charts (Quick Terminal Visualization)

When you can't generate images, use ASCII:

```
Revenue by Month (in $K)
========================
Jan: ████████████████ 160
Feb: ██████████████████ 180
Mar: ████████████████████████ 240
Apr: ██████████████████████ 220
May: ██████████████████████████ 260
Jun: ████████████████████████████ 280
```

---

## Report Generation

### Standard Report Template

```markdown
# [Report Name]
**Period:** [Date range]
**Generated:** [Date]
**Author:** [Agent/Human]

## Executive Summary
[2-3 sentences with key findings]

## Key Metrics

| Metric | Current | Previous | Change |
|--------|---------|----------|--------|
| [Metric] | [Value] | [Value] | [+/-X%] |

## Detailed Analysis

### [Section 1]
[Analysis with supporting data]

### [Section 2]
[Analysis with supporting data]

## Visualizations
[Insert charts]

## Insights
1. **[Insight]**: [Supporting evidence]
2. **[Insight]**: [Supporting evidence]

## Recommendations
1. [Actionable recommendation]
2. [Actionable recommendation]

## Methodology
- Data source: [Source]
- Date range: [Range]
- Filters applied: [Filters]
- Known limitations: [Limitations]

## Appendix
[Supporting data tables]
```

### Automated Report Script

```bash
#!/bin/bash
# generate-report.sh

# Pull latest data
python scripts/extract_data.py --output data/latest.csv

# Run analysis
python scripts/analyze.py --input data/latest.csv --output reports/

# Generate report
python scripts/format_report.py --template weekly --output reports/weekly-$(date +%Y-%m-%d).md

echo "Report generated: reports/weekly-$(date +%Y-%m-%d).md"
```

---

## Statistical Analysis

### Descriptive Statistics

| Statistic | What It Tells You | Use Case |
|-----------|-------------------|----------|
| **Mean** | Average value | Central tendency |
| **Median** | Middle value | Robust to outliers |
| **Mode** | Most common | Categorical data |
| **Std Dev** | Spread around mean | Variability |
| **Min/Max** | Range | Data boundaries |
| **Percentiles** | Distribution shape | Benchmarking |

### Quick Stats with Python

```python
# Full descriptive statistics
stats = df['amount'].describe()
print(stats)

# Additional stats
print(f"Median: {df['amount'].median()}")
print(f"Mode: {df['amount'].mode()[0]}")
print(f"Skewness: {df['amount'].skew()}")
print(f"Kurtosis: {df['amount'].kurtosis()}")

# Correlation
correlation = df['sales'].corr(df['marketing_spend'])
print(f"Correlation: {correlation:.3f}")
```

### Statistical Tests Quick Reference

| Test | Use Case | Python |
|------|----------|--------|
| T-test | Compare two means | `scipy.stats.ttest_ind(a, b)` |
| Chi-square | Categorical independence | `scipy.stats.chi2_contingency(table)` |
| ANOVA | Compare 3+ means | `scipy.stats.f_oneway(a, b, c)` |
| Pearson | Linear correlation | `scipy.stats.pearsonr(x, y)` |

---

## Analysis Workflow

### Standard Analysis Process

1. **Define the Question**
   - What are we trying to answer?
   - What decisions will this inform?

2. **Understand the Data**
   - What data is available?
   - What's the structure and quality?

3. **Clean and Prepare**
   - Handle missing values
   - Fix data types
   - Remove duplicates

4. **Explore**
   - Descriptive statistics
   - Initial visualizations
   - Identify patterns

5. **Analyze**
   - Deep dive into findings
   - Statistical tests if needed
   - Validate hypotheses

6. **Communicate**
   - Clear visualizations
   - Actionable insights
   - Recommendations

### Analysis Request Template

```markdown
# Analysis Request

## Question
[What are we trying to answer?]

## Context
[Why does this matter? What decision will it inform?]

## Data Available
- [Dataset 1]: [Description]
- [Dataset 2]: [Description]

## Expected Output
- [Deliverable 1]
- [Deliverable 2]

## Timeline
[When is this needed?]

## Notes
[Any constraints or considerations]
```

---

## Scripts

### data-init.sh
Initialize your data analysis workspace.

### query.sh
Quick SQL query execution.

```bash
# Run query from file
./scripts/query.sh --file queries/daily-report.sql

# Run inline query
./scripts/query.sh "SELECT COUNT(*) FROM users"

# Save output to file
./scripts/query.sh --file queries/export.sql --output data/export.csv
```

### analyze.py
Python analysis toolkit.

```bash
# Basic analysis
python scripts/analyze.py --input data/sales.csv

# With specific analysis type
python scripts/analyze.py --input data/sales.csv --type cohort

# Generate report
python scripts/analyze.py --input data/sales.csv --report weekly
```

---

## Integration Tips

### With Other Skills

| Skill | Integration |
|-------|-------------|
| **Marketing** | Analyze campaign performance, content metrics |
| **Sales** | Pipeline analytics, conversion analysis |
| **Business Dev** | Market research data, competitor analysis |

### Common Data Sources

- **Databases:** PostgreSQL, MySQL, SQLite
- **Warehouses:** BigQuery, Snowflake, Redshift
- **Spreadsheets:** Google Sheets, Excel, CSV
- **APIs:** REST endpoints, GraphQL
- **Files:** JSON, Parquet, XML

---

## Best Practices

1. **Start with the question** — Know what you're trying to answer
2. **Validate your data** — Garbage in = garbage out
3. **Document everything** — Queries, assumptions, decisions
4. **Visualize appropriately** — Right chart for right data
5. **Show your work** — Methodology matters
6. **Lead with insights** — Not just data dumps
7. **Make it actionable** — "So what?" → "Now what?"
8. **Version your queries** — Track changes over time

---

## Common Mistakes

❌ **Confirmation bias** — Looking for data to support a conclusion
❌ **Correlation ≠ causation** — Be careful with claims
❌ **Cherry-picking** — Using only favorable data
❌ **Ignoring outliers** — Investigate before removing
❌ **Over-complicating** — Simple analysis often wins
❌ **No context** — Numbers without comparison are meaningless

---

## License

**License:** MIT — use freely, modify, distribute.

---

*"The goal is to turn data into information, and information into insight." — Carly Fiorina*
