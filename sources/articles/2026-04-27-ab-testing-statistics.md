---
source: https://blog.tsingjyujing.com/ml/recsys/ab_testing
title: 关于AA测试和AB测试的一些思考
fetched: 2026-04-27 01:02
---

# 关于AA测试和AB测试的一些思考

**作者：** 清雨影
**来源：** 清雨影的 Blog

## 起因

AA/AB 测试的基本做法：取一部分用户分成两组，运行一段时间后比较结果。

实践中常见问题：AB 测试中两组天然存在指标差异，尤其是样本少时。AA 测试有时通不过，换个分组的 Salt Key 结果就不一样。随着采样数据上升，AA 测试中两组的方差都逐渐收敛，两组之间的天然差异被"固化"，AA 测试就失败了。

**核心改进思路：** 把 AA 测试从 Pass/Fail 变成标定 AB 测试的工具。

## 统计学原理

假设点击事件服从 Bernoulli 分布，即每次展示等价于抛一枚概率为 p 的硬币。

根据中心极限定理，当 n 足够大时，点击次数 C 服从正态分布 N(Np, Np(1-p))。

转化后得到点击率 x ~ N(p, p(1-p)/N)。

对于 AB 测试，设 x₃ = x₁ - x₂，则 x₃ ~ N(μ₁-μ₂, σ₁²+σ₂²)

## AA 测试实战

计算最少应提升的 CTR（最小可检测提升），使用单侧置信度。

```python
from scipy.stats import norm
from math import sqrt

def get_minimal_lift(C_1, N_1, C_2, N_2, confidence_level):
    mean_1 = C_1 / N_1
    mean_2 = C_2 / N_2
    delta_mean = mean_1 - mean_2
    var_1 = mean_1 * (1 - mean_1) / N_1
    var_2 = mean_2 * (1 - mean_2) / N_2
    return norm(delta_mean, sqrt(var_1 + var_2)).ppf(1 - confidence_level)
```

## AB 测试实战

用 AA 测试得到最小提升 ε，求 P(x₁-x₂ ≥ ε)，即测试组相对对照组有提升的置信度。

```python
def get_passed_prob(C_1, N_1, C_2, N_2, epsilon):
    mean_1 = C_1 / N_1
    mean_2 = C_2 / N_2
    delta_mean = mean_1 - mean_2
    var_1 = mean_1 * (1 - mean_1) / N_1
    var_2 = mean_2 * (1 - mean_2) / N_2
    return 1.0 - norm(delta_mean, sqrt(var_1 + var_2)).cdf(epsilon)
```

## Bayesian Approach

也可以用 Beta 分布对 CTR 建模（Thompson Sampling 的思路）：
- 通过数据求 C 组分布 x_c ~ Beta(a_c, b_c) 和 T 组分布 x_t ~ Beta(a_t, b_t)
- 用 scipy.stats.beta 的 rvs 生成样本，相减后获取新分布
- 采样频率调高可获取足够精度

[原文链接](https://blog.tsingjyujing.com/ml/recsys/ab_testing)
