#!/bin/bash
# 每日詳細技能檢查

LOG_DIR="/home/node/.openclaw/workspace/memory/skill_checks"
mkdir -p "$LOG_DIR"

TIMESTAMP=$(date +"%Y%m%d")
LOG_FILE="$LOG_DIR/daily_check_${TIMESTAMP}.log"

echo "每日技能詳細檢查 - $(date)" > "$LOG_FILE"
echo "==============================" >> "$LOG_FILE"

# 運行完整檢查
cd /home/node/.openclaw/workspace
python3 skills_check_cron.py >> "$LOG_FILE" 2>&1
EXIT_CODE=$?

echo "" >> "$LOG_FILE"
echo "檢查完成: $(date)" >> "$LOG_FILE"
echo "退出碼: $EXIT_CODE" >> "$LOG_FILE"

# 如果有錯誤，記錄到錯誤日誌
if [ $EXIT_CODE -ne 0 ]; then
    ERROR_LOG="$LOG_DIR/errors_${TIMESTAMP}.log"
    echo "發現錯誤 - $(date)" > "$ERROR_LOG"
    tail -20 "$LOG_FILE" >> "$ERROR_LOG"
    echo "⚠️  檢查發現問題，詳見: $ERROR_LOG" >> "$LOG_FILE"
fi

# 保留最近30天的日誌
find "$LOG_DIR" -name "daily_check_*.log" -mtime +30 -delete
find "$LOG_DIR" -name "errors_*.log" -mtime +30 -delete

exit $EXIT_CODE
