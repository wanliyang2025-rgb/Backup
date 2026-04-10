#!/bin/bash
# 自动把 obsidian-vault 同步到 GitHub

cd ~/obsidian-vault || exit 1

# 检查是否有变更
git diff --quiet && git diff --cached --quiet
if [ $? -eq 0 ]; then
    # 无变更，退出
    exit 0
fi

# 添加所有变更并提交
git add -A
git commit -m "Auto-sync: $(date '+%Y-%m-%d %H:%M')"

# 推送到 GitHub
git push -q origin main

echo "[$(date)] Synced to GitHub"
