#!/bin/bash
# OpenClaw Backup Script (Optimized)
# 排除大文件：venv、npm-global、插件缓存、日志、n8n/nodered等
# Usage: ./backup.sh [backup_dir]

BACKUP_DIR="${1:-$HOME/openclaw-backups}"
DATE=$(date +%Y-%m-%d_%H%M)
BACKUP_FILE="$BACKUP_DIR/openclaw-$DATE.tar.gz"

mkdir -p "$BACKUP_DIR"

# Create backup - exclude large/unneeded dirs
# venv: Python packages, recreate with pip install
# npm-global: npm global packages, recreate with npm install -g
# extensions/openclaw-lark: Feishu plugin, reinstall via clawdhub
# agents/: agent identity and session configs
# media/: user uploads
# completions/: context completions cache
# flows/: flow configs
# logs/: log files
# n8n/, nodered/: self-hosted automation (separate backups)
# tasks/: task cache
tar -czf "$BACKUP_FILE" \
    --exclude='venv' \
    --exclude='npm-global' \
    --exclude='extensions/openclaw-lark' \
    --exclude='completions' \
    --exclude='flows' \
    --exclude='logs' \
    --exclude='n8n' \
    --exclude='nodered' \
    --exclude='tasks' \
    --exclude='*.log' \
    --exclude='workspace/node_modules' \
    --exclude='workspace/.cache' \
    -C "$HOME" .openclaw/

if [ $? -eq 0 ]; then
    SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    ORIGINAL=$(du -sh "$HOME/.openclaw" | cut -f1)

    # Rotate: keep only last 7 backups
    ls -t "$BACKUP_DIR"/openclaw-*.tar.gz 2>/dev/null | tail -n +8 | xargs -r rm

    COUNT=$(ls "$BACKUP_DIR"/openclaw-*.tar.gz 2>/dev/null | wc -l)

    echo "✅ Backup created: $BACKUP_FILE ($SIZE)"
    echo "📁 Original size: $ORIGINAL → Backup: $SIZE"
    echo "📁 Total backups: $COUNT (keeping last 7)"
    exit 0
else
    echo "❌ Backup failed"
    exit 1
fi
