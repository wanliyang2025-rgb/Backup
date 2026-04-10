#!/bin/bash
# 搜索 Obsidian Vault（关键词 + 上下文片段）
# 用法: bash vault-search.sh "关键词" [文件类型]

VAULT="$HOME/obsidian-vault"
QUERY="$1"
LIMIT="${2:-10}"

if [ -z "$QUERY" ]; then
  echo "用法: bash vault-search.sh \"关键词\" [结果数量]"
  exit 1
fi

echo "🔍 在笔记库中搜索: $QUERY"
echo "========================================"

# 搜索并显示上下文
results=$(grep -rn --include="*.md" -i "$QUERY" "$VAULT" 2>/dev/null | head -20)

if [ -z "$results" ]; then
  echo "未找到相关内容"
  exit 0
fi

count=0
echo "$results" | while IFS=: read -r file line content; do
  rel="${file#$VAULT/}"
  # 清理内容（去除多余空白）
  clean=$(echo "$content" | sed 's/^[[:space:]]*//' | cut -c1-150)
  echo "📄 $rel"
  echo "   第${line}行: ${clean}..."
  echo ""
  count=$((count+1))
  if [ $count -ge "$LIMIT" ]; then
    exit 0
  fi
done

echo "========================================"
echo "共找到 $(echo "$results" | wc -l) 条匹配"
