#!/usr/bin/env python3
"""
下载飞书文件并处理Excel
"""
import json
import os
import sys

# 尝试从 openclaw 获取飞书配置
# 使用 SDK 方式调用飞书 API

# 读取飞书扩展的 node_modules
lark_sdk_path = '/home/leonwan/.openclaw/extensions/openclaw-lark/node_modules/@larksuiteoapi/node-sdk'

if os.path.exists(lark_sdk_path):
    sys.path.insert(0, lark_sdk_path)
    print(f"Found Lark SDK at: {lark_sdk_path}")
    
    # 列出目录
    for item in os.listdir(lark_sdk_path):
        print(f"  {item}")
else:
    print("Lark SDK not found")

