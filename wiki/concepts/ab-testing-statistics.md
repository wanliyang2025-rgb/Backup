---
created: 2026-04-27
source: https://blog.tsingjyujing.com/ml/recsys/ab_testing
tags: [AB测试, 实验统计学, 数据分析]
---

# AB 测试与实验统计学实战

## Overview

深入讲解 AA 测试和 AB 测试的统计学原理与实战方法。核心创新思路：不把 AA 测试当作 Pass/Fail 的门禁，而是将其作为标定 AB 测试的工具——通过 AA 测试计算出最少提升 ε，再用这个 ε 作为 AB 测试的判定基准。

## Key Claims

- 实践中 AB 测试两组天然存在指标差异（尤其是小样本），误差量级一般在 0.1% 左右
- AA 测试随采样数据上升，方差收敛后两组间天然差异会被"固化"，导致 AA 测试失败
- 核心改进：用 AA 测试计算最小可检测提升 ε，再在 AB 测试中判断 P(x₁-x₂ ≥ ε)
- 基于 Beta 分布的 Bayesian 方法（Monte Carlo 采样）是正态近似法的有力补充

## Related

- [[bi-dashboard-cockpit]] — 数据分析与指标可视化
- [[consistency-dimension]] — 维度建模与数据分析
- [[zhihu-ai-product-dev]] — AI 产品中的实验方法

## Sources

- [关于AA测试和AB测试的一些思考](https://blog.tsingjyujing.com/ml/recsys/ab_testing)
