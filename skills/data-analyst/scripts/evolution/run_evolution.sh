#!/bin/bash
# data-analyst 技能自我进化脚本
# 每月1日 09:00 自动执行（系统 crontab）
# 日志：~/.openclaw/logs/da-evolution.log

LOG_DIR="/home/leonwan/.openclaw/logs"
SKILL_DIR="/home/leonwan/.openclaw/workspace/skills/data-analyst/scripts/evolution"
mkdir -p "$LOG_DIR"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] === 数据分析技能进化开始 ===" >> "$LOG_DIR/da-evolution.log"

# 1. 运行评分框架（只产生框架，联网调研部分需要AI执行）
python3 "$SKILL_DIR/research_trends.py" >> "$LOG_DIR/da-evolution.log" 2>&1

# 2. 通知我（在主会话中完成实际调研和更新）
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 框架已运行，请在下次心跳时触发实际调研" >> "$LOG_DIR/da-evolution.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] === 进化任务排队完成 ===" >> "$LOG_DIR/da-evolution.log"
