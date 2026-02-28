#!/bin/bash
# 智能Heartbeat檢查腳本 - 包含睡眠時間管理

echo "🤖 智能Heartbeat檢查系統"
echo "========================"
echo "檢查時間: $(date)"
echo "UTC時間: $(date -u)"
echo ""

WORKSPACE="/home/node/.openclaw/workspace"
cd "$WORKSPACE"

# 計算香港時間
UTC_HOUR=$(date -u +"%H")
HK_HOUR=$(( (UTC_HOUR + 8) % 24 ))

echo "⏰ 時間信息:"
echo "• UTC時間: $(date -u +'%H:%M')"
echo "• 香港時間: 約 $HK_HOUR:$(date -u +'%M') (估算)"
echo "• 睡眠時段: 23:00-08:00 HKT (15:00-00:00 UTC)"
echo ""

# 檢查是否在睡眠時間
IS_SLEEP_TIME=0
if [[ $HK_HOUR -ge 23 ]] || [[ $HK_HOUR -lt 8 ]]; then
    IS_SLEEP_TIME=1
    echo "💤 當前處於睡眠時間 (23:00-08:00 HKT)"
    echo "📴 將減少通知發送，除非有重要更新"
else
    echo "🌅 當前處於活動時間 (08:00-23:00 HKT)"
    echo "📢 正常發送通知"
fi

echo ""
echo "🔍 檢查提醒事項..."
echo "----------------"

# 讀取提醒事項
REMINDERS=$(grep -A10 "## Reminders" HEARTBEAT.md | tail -n +2)
if [[ -n "$REMINDERS" ]]; then
    echo "📋 當前提醒列表:"
    echo "$REMINDERS" | while read line; do
        if [[ -n "$line" ]]; then
            echo "  • $line"
        fi
    done
else
    echo "✅ 沒有設置提醒事項"
fi

echo ""
echo "📝 檢查待辦事項..."
echo "----------------"

# 讀取待辦事項
PENDING=$(grep -A10 "## Pending Follow-ups" HEARTBEAT.md | tail -n +2)
if [[ -n "$PENDING" ]]; then
    echo "📋 當前待辦事項:"
    echo "$PENDING" | while read line; do
        if [[ -n "$line" ]]; then
            echo "  • $line"
        fi
    done
else
    echo "✅ 沒有待辦事項"
fi

echo ""
echo "⚡ 檢查重要更新..."
echo "----------------"

IMPORTANT_UPDATES=0
UPDATE_REASONS=()

# 檢查是否有緊急提醒（<2小時）
check_urgent_reminders() {
    # 這裡可以添加具體的時間檢查邏輯
    # 目前先標記為需要實現
    echo "  ⏳ 緊急提醒檢查: 需要具體實現時間解析"
    return 0
}

# 檢查系統錯誤
check_system_errors() {
    # 檢查最近的錯誤日誌
    ERROR_LOG_COUNT=$(find "$WORKSPACE/memory" -name "*.log" -type f -mmin -60 2>/dev/null | xargs grep -l "error\|failed\|ERROR\|FAILED" 2>/dev/null | wc -l)
    
    if [[ $ERROR_LOG_COUNT -gt 0 ]]; then
        IMPORTANT_UPDATES=1
        UPDATE_REASONS+=("發現 $ERROR_LOG_COUNT 個系統錯誤")
        echo "  ❌ 發現系統錯誤: $ERROR_LOG_COUNT 個錯誤日誌"
    else
        echo "  ✅ 系統運行正常"
    fi
}

# 檢查Cron Job結果
check_cron_results() {
    # 檢查最近的Cron Job執行
    CRON_RESULTS=$(find "$WORKSPACE/memory" -name "*cron*" -type f -mmin -120 2>/dev/null | head -3)
    
    if [[ -n "$CRON_RESULTS" ]]; then
        echo "  ⚙️ 最近Cron Job執行:"
        echo "$CRON_RESULTS" | while read file; do
            echo "    • $(basename "$file")"
        done
    else
        echo "  ✅ 沒有最近的Cron Job需要關注"
    fi
}

# 執行檢查
check_urgent_reminders
check_system_errors
check_cron_results

echo ""
echo "📊 檢查結果摘要"
echo "=============="

if [[ $IS_SLEEP_TIME -eq 1 ]]; then
    echo "💤 睡眠時間模式"
    
    if [[ $IMPORTANT_UPDATES -eq 0 ]]; then
        echo "✅ 沒有重要更新需要通知"
        echo "📴 保持靜默，不發送heartbeat"
        echo ""
        echo "💡 提示: 非緊急信息將在08:00 HKT後報告"
        exit 0
    else
        echo "⚠️ 發現重要更新，需要通知:"
        for reason in "${UPDATE_REASONS[@]}"; do
            echo "  • $reason"
        done
        echo ""
        echo "📢 將發送重要更新通知"
        exit 1
    fi
else
    echo "🌅 活動時間模式"
    
    if [[ $IMPORTANT_UPDATES -eq 0 ]]; then
        echo "✅ 系統正常，沒有重要更新"
        echo "📢 將發送常規heartbeat報告"
        exit 1
    else
        echo "⚠️ 發現重要更新:"
        for reason in "${UPDATE_REASONS[@]}"; do
            echo "  • $reason"
        done
        echo ""
        echo "📢 將發送包含重要更新的heartbeat"
        exit 1
    fi
fi

echo ""
echo "🔄 下次檢查: 根據設定頻率"
echo "📍 當前策略: 睡眠時間(23:00-08:00 HKT)減少通知"