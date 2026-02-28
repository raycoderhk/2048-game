#!/bin/bash
# 啟動技能監控系統

echo "🚀 啟動 OpenClaw 技能監控系統"
echo "=============================="

# 創建監控目錄
MONITOR_DIR="/home/node/.openclaw/workspace/memory/skill_checks"
mkdir -p "$MONITOR_DIR"

# 主監控腳本
MAIN_SCRIPT="/home/node/.openclaw/workspace/skills_monitor.sh"

# 檢查腳本是否存在
if [ ! -f "$MAIN_SCRIPT" ]; then
    echo "❌ 主監控腳本不存在: $MAIN_SCRIPT"
    exit 1
fi

# 運行一次測試
echo "運行初始測試..."
if "$MAIN_SCRIPT"; then
    echo "✅ 初始測試成功"
else
    echo "⚠️  初始測試有警告"
fi

# 創建簡單的定時執行機制
echo ""
echo "設置定時執行..."
echo "----------------"

# 創建一個每小時檢查的簡單機制
HOURLY_CHECK="/home/node/.openclaw/workspace/check_skills_hourly.sh"

cat > "$HOURLY_CHECK" << 'EOF'
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
EOF

chmod +x "$HOURLY_CHECK"
echo "✅ 創建每小時檢查腳本: $HOURLY_CHECK"

# 創建每日詳細檢查
DAILY_CHECK="/home/node/.openclaw/workspace/check_skills_daily.sh"

cat > "$DAILY_CHECK" << 'EOF'
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
EOF

chmod +x "$DAILY_CHECK"
echo "✅ 創建每日檢查腳本: $DAILY_CHECK"

# 創建啟動腳本
STARTUP_SCRIPT="/home/node/.openclaw/workspace/start_monitoring.sh"

cat > "$STARTUP_SCRIPT" << 'EOF'
#!/bin/bash
# 啟動技能監控

echo "啟動技能監控系統..."

# 運行每日檢查
/home/node/.openclaw/workspace/check_skills_daily.sh

# 設置定時任務（使用簡單的 sleep 循環）
while true; do
    # 每小時運行簡化檢查
    /home/node/.openclaw/workspace/check_skills_hourly.sh
    
    # 等待1小時
    sleep 3600
done
EOF

chmod +x "$STARTUP_SCRIPT"
echo "✅ 創建啟動腳本: $STARTUP_SCRIPT"

# 創建手動檢查腳本
MANUAL_CHECK="/home/node/.openclaw/workspace/check_skills_now.sh"

cat > "$MANUAL_CHECK" << 'EOF'
#!/bin/bash
# 手動立即檢查技能狀態

echo "🔧 立即技能檢查"
echo "================"

cd /home/node/.openclaw/workspace
python3 skills_check_cron.py

exit $?
EOF

chmod +x "$MANUAL_CHECK"
echo "✅ 創建手動檢查腳本: $MANUAL_CHECK"

echo ""
echo "📊 技能監控系統設置完成！"
echo "========================"
echo ""
echo "📋 可用命令:"
echo "  $MANUAL_CHECK      - 手動立即檢查"
echo "  $DAILY_CHECK       - 運行每日詳細檢查"
echo "  $HOURLY_CHECK      - 運行每小時簡化檢查"
echo "  $STARTUP_SCRIPT    - 啟動持續監控"
echo ""
echo "📁 日誌目錄: $MONITOR_DIR"
echo ""
echo "💡 建議:"
echo "  1. 手動運行一次檢查: $MANUAL_CHECK"
echo "  2. 可以將 $STARTUP_SCRIPT 添加到啟動項"
echo "  3. 定期檢查 $MONITOR_DIR 中的日誌"
echo ""
echo "🎉 所有設置完成！"