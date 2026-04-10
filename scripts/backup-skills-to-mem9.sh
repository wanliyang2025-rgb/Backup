#!/bin/bash
# 备份技能到 mem9（手动执行）
# 用法: bash scripts/backup-skills-to-mem9.sh

API_KEY="i51kiU6FxY1pF1fTZ-1IB7HDSygVz0sD"
SKILLS_DIR="$HOME/.openclaw/workspace/skills"

for skill in "$SKILLS_DIR"/*; do
  skill_name=$(basename "$skill")
  [[ "$skill_name" == *"backup"* ]] && continue
  [ ! -f "$skill/SKILL.md" ] && continue
  
  content=$(head -c 2500 "$skill/SKILL.md" | jq -Rs .)
  
  curl -s -X POST "https://api.mem9.ai/v1alpha2/mem9s/memories" \
    -H "Content-Type: application/json" \
    -H "X-API-Key: $API_KEY" \
    -d "{\"content\": $content, \"type\": \"skill\", \"labels\": [\"skill\", \"backup\", \"$skill_name\"]}" \
    > /dev/null
  
  echo "✓ $skill_name"
done

echo "✅ 备份完成"
