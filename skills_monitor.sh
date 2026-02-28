#!/bin/bash
# 技能監控 Cron Job
# 每天運行一次，檢查所有技能狀態

LOG_DIR="/home/node/.openclaw/workspace/memory/skill_checks"
mkdir -p "$LOG_DIR"

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$LOG_DIR/skill_monitor_${TIMESTAMP}.log"
JSON_REPORT="$LOG_DIR/skill_report_${TIMESTAMP}.json"

echo "🔧 技能監控檢查 - $(date)" > "$LOG_FILE"
echo "================================" >> "$LOG_FILE"

# 運行 Python 檢查腳本
cd /home/node/.openclaw/workspace
python3 skills_check_cron.py >> "$LOG_FILE" 2>&1
EXIT_CODE=$?

echo "" >> "$LOG_FILE"
echo "檢查完成時間: $(date)" >> "$LOG_FILE"
echo "退出碼: $EXIT_CODE" >> "$LOG_FILE"

# 如果有錯誤，發送通知（這裡可以擴展為發送郵件、Telegram等）
if [ $EXIT_CODE -ne 0 ]; then
    echo "⚠️  檢查發現問題，請查看詳細報告" >> "$LOG_FILE"
    
    # 這裡可以添加通知邏輯，例如：
    # - 發送郵件
    # - 發送 Telegram 消息
    # - 發送 Slack 通知
fi

# 保留最近30天的日誌
find "$LOG_DIR" -name "skill_monitor_*.log" -mtime +30 -delete
find "$LOG_DIR" -name "skill_report_*.json" -mtime +30 -delete
find "$LOG_DIR" -name "skill_check_*.json" -mtime +30 -delete

exit $EXIT_CODE
