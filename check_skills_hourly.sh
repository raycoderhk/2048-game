#!/bin/bash
# 每小時檢查技能狀態（簡化版）

LOG_DIR="/home/node/.openclaw/workspace/memory/skill_checks"
mkdir -p "$LOG_DIR"

TIMESTAMP=$(date +"%Y%m%d_%H")
LOG_FILE="$LOG_DIR/hourly_check_${TIMESTAMP}.log"

# 只運行基本檢查
echo "每小時技能檢查 - $(date)" > "$LOG_FILE"

# 檢查基本工具
echo "1. 基本工具檢查:" >> "$LOG_FILE"
for cmd in python3 pip3 tesseract curl; do
    if command -v "$cmd" &> /dev/null; then
        echo "  ✅ $cmd: 可用" >> "$LOG_FILE"
    else
        echo "  ❌ $cmd: 不可用" >> "$LOG_FILE"
    fi
done

# 檢查技能目錄
echo "" >> "$LOG_FILE"
echo "2. 技能目錄檢查:" >> "$LOG_FILE"
SKILLS_DIR="/home/node/.openclaw/workspace/skills"
if [ -d "$SKILLS_DIR" ]; then
    echo "  ✅ 技能目錄存在" >> "$LOG_FILE"
    for skill in "$SKILLS_DIR"/*; do
        if [ -d "$skill" ]; then
            skill_name=$(basename "$skill")
            echo "  📁 $skill_name" >> "$LOG_FILE"
        fi
    done
else
    echo "  ❌ 技能目錄不存在" >> "$LOG_FILE"
fi

echo "" >> "$LOG_FILE"
echo "檢查完成: $(date)" >> "$LOG_FILE"

# 保留最近7天的日誌
find "$LOG_DIR" -name "hourly_check_*.log" -mtime +7 -delete

exit 0
