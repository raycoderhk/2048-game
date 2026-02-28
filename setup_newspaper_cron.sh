#!/bin/bash
# 安裝新聞報紙生成 Cron Job

echo "安裝新聞報紙定時任務..."
echo "Cron job: 0 8 * * * /home/node/.openclaw/workspace/generate_daily_newspaper.sh >> /home/node/.openclaw/workspace/memory/newspaper_logs/cron.log 2>&1"

# 這裡可以添加實際的crontab設置代碼
# 由於環境限制，我們創建一個替代方案

# 創建一個每小時檢查的簡單定時器
HOURLY_CHECK="/home/node/.openclaw/workspace/check_and_generate_hourly.sh"

cat > "$HOURLY_CHECK" << 'HOURLYEOF'
#!/bin/bash
# 每小時檢查並生成報紙（如果尚未生成）

WORKSPACE="/home/node/.openclaw/workspace"
TODAY=$(date +"%Y%m%d")
TODAY_PAPER="$WORKSPACE/memory/newspapers/newspaper_${TODAY}.txt"

# 如果今天還沒有報紙，並且是上午8-9點，則生成
if [ ! -f "$TODAY_PAPER" ]; then
    HOUR=$(date +"%H")
    if [ "$HOUR" -ge 8 ] && [ "$HOUR" -le 9 ]; then
        echo "$(date) - 生成今日報紙" >> "$WORKSPACE/memory/newspaper_logs/hourly_check.log"
        "$WORKSPACE/generate_daily_newspaper.sh"
    fi
fi
HOURLYEOF

chmod +x "$HOURLY_CHECK"
echo "✅ 創建每小時檢查腳本: $HOURLY_CHECK"

echo ""
echo "📋 手動運行命令:"
echo "  $WORKSPACE/generate_newspaper_now.sh - 立即生成報紙"
echo "  $WORKSPACE/view_newspaper.sh - 查看報紙"
echo ""
echo "💡 建議將 $HOURLY_CHECK 添加到啟動項中"
