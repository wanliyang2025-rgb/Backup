#!/usr/bin/env python3
"""Process 科目余额表 according to comparison rules."""

import pandas as pd
import numpy as np

# Read the Excel file
df = pd.read_excel('/home/leonwan/.openclaw/workspace/科目余额表.xlsx')

print("原始数据列名:", df.columns.tolist())
print("原始数据形状:", df.shape)
print("\n前10行数据:")
print(df.head(10))

# Show unique values in key columns
print("\n账套唯一值:", df.iloc[:, 0].unique() if len(df.columns) > 0 else "N/A")
print("核算项目唯一值:", df.iloc[:, 3].unique() if len(df.columns) > 3 else "N/A")
print("币种唯一值:", df.iloc[:, 4].unique() if len(df.columns) > 4 else "N/A")
print("科目代码唯一值:", df.iloc[:, 1].unique() if len(df.columns) > 1 else "N/A")
