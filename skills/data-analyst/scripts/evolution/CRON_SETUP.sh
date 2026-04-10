#!/bin/bash
# 数据分析技能自我进化 cron 任务
# 放在系统 crontab 里（避免 session 启动超时）
#
# 设置方式：
# 1. 运行: crontab -e
# 2. 添加以下行（每月第一个周四 09:00 执行）:
#    0 9 * * 4 grep -q "first Thu" && bash /home/leonwan/.openclaw/workspace/skills/data-analyst/scripts/evolution/run_evolution.sh >> ~/.openclaw/logs/da-evolution.log 2>&1
#
# 或者更简单的方式 - 固定每月1日09:00:
#    0 9 1 * * bash /home/leonwan/.openclaw/workspace/skills/data-analyst/scripts/evolution/run_evolution.sh >> ~/.openclaw/logs/da-evolution.log 2>&1

SCRIPT_DIR="/home/leonwan/.openclaw/workspace/skills/data-analyst/scripts/evolution"
LOG_DIR="/home/leonwan/.openclaw/logs"

mkdir -p "$LOG_DIR"
echo "[$(date)] Evolution cron triggered" >> "$LOG_DIR/da-evolution.log"

# 启动 isolated session 做调研
openclaw run --session isolated --timeout 300 "$SCRIPT_DIR/research_trends.py" >> "$LOG_DIR/da-evolution.log" 2>&1

echo "[$(date)] Evolution completed" >> "$LOG_DIR/da-evolution.log"
