#!/bin/bash
# 設置技能監控 Cron Job

echo "🔧 設置技能監控系統"
echo "===================="

# 1. 修復發現的問題
echo "1. 修復檢查發現的問題..."
echo "------------------------"

# 安裝 ping 工具（如果缺失）
if ! command -v ping &> /dev/null; then
    echo "安裝 ping 工具..."
    apt-get update && apt-get install -y iputils-ping 2>/dev/null | tail -5
    if command -v ping &> /dev/null; then
        echo "✅ ping 安裝成功"
    else
        echo "⚠️  ping 安裝可能失敗，但不會影響主要功能"
    fi
else
    echo "✅ ping 已安裝"
fi

# 2. 創建 cron job 腳本
echo ""
echo "2. 創建 cron job 腳本..."
echo "------------------------"

CRON_SCRIPT="/home/node/.openclaw/workspace/skills_monitor.sh"

cat > "$CRON_SCRIPT" << 'EOF'
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
EOF

chmod +x "$CRON_SCRIPT"
echo "✅ Cron job 腳本創建完成: $CRON_SCRIPT"

# 3. 設置 crontab
echo ""
echo "3. 設置 crontab..."
echo "------------------"

# 創建 crontab 文件
CRONTAB_FILE="/tmp/openclaw_crontab"

# 檢查現有 crontab
if crontab -l 2>/dev/null; then
    crontab -l > "$CRONTAB_FILE"
    echo "✅ 讀取現有 crontab"
else
    echo "# OpenClaw Skill Monitor Crontab" > "$CRONTAB_FILE"
    echo "✅ 創建新 crontab 文件"
fi

# 添加我們的 cron job（每天上午9點運行）
CRON_JOB="0 9 * * * $CRON_SCRIPT"

# 檢查是否已經存在
if ! grep -q "$CRON_SCRIPT" "$CRONTAB_FILE"; then
    echo "" >> "$CRONTAB_FILE"
    echo "# OpenClaw 技能監控" >> "$CRONTAB_FILE"
    echo "$CRON_JOB" >> "$CRONTAB_FILE"
    echo "✅ 添加 cron job: $CRON_JOB"
else
    echo "⚠️  Cron job 已存在，跳過添加"
fi

# 安裝 crontab
if crontab "$CRONTAB_FILE"; then
    echo "✅ Crontab 安裝成功"
else
    echo "❌ Crontab 安裝失敗"
    exit 1
fi

# 4. 測試 cron job
echo ""
echo "4. 測試 cron job..."
echo "-------------------"

echo "手動運行一次測試..."
if "$CRON_SCRIPT"; then
    echo "✅ Cron job 測試運行成功"
else
    TEST_EXIT_CODE=$?
    echo "⚠️  Cron job 測試退出碼: $TEST_EXIT_CODE"
    echo "檢查日誌文件了解詳細信息"
fi

# 5. 顯示設置摘要
echo ""
echo "📊 設置摘要"
echo "==========="
echo "✅ 技能檢查腳本: /home/node/.openclaw/workspace/skills_check_cron.py"
echo "✅ Cron job 腳本: $CRON_SCRIPT"
echo "✅ 運行時間: 每天上午 9:00"
echo "✅ 日誌目錄: /home/node/.openclaw/workspace/memory/skill_checks"
echo ""
echo "📋 下次運行時間: 明天上午 9:00"
echo "📋 手動運行命令: $CRON_SCRIPT"
echo ""
echo "🔧 監控內容:"
echo "  - 基本工具 (Python, pip, Tesseract, curl)"
echo "  - 技能目錄結構"
echo "  - smart_ocr 技能完整性"
echo "  - 網絡連接狀態"
echo ""
echo "💡 擴展建議:"
echo "  1. 添加郵件通知功能"
echo "  2. 添加 Telegram/Slack 通知"
echo "  3. 添加自動修復功能"
echo "  4. 添加性能監控"
echo ""
echo "🎉 技能監控系統設置完成！"