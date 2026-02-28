#!/bin/bash
# 家長日提醒檢查腳本

echo "🏫 家長日提醒檢查"
echo "=================="
echo "檢查時間: $(date)"
echo ""

WORKSPACE="/home/node/.openclaw/workspace"
cd "$WORKSPACE"

# 讀取HEARTBEAT.md中的提醒
echo "📋 當前提醒列表:"
echo "----------------"
grep -A1 "## Reminders" HEARTBEAT.md | tail -n +2 | while read line; do
    if [[ -n "$line" ]]; then
        echo "• $line"
    fi
done

echo ""
echo "📅 家長日詳細信息:"
echo "----------------"

# 提取家長日信息
PARENT_TEACHER_INFO=$(grep "女兒學校家長日" HEARTBEAT.md)
if [[ -n "$PARENT_TEACHER_INFO" ]]; then
    echo "✅ 家長日提醒已設置"
    echo ""
    
    # 解析日期和時間
    DATE_PART=$(echo "$PARENT_TEACHER_INFO" | grep -o "February [0-9]*, 2026")
    TIME_PART=$(echo "$PARENT_TEACHER_INFO" | grep -o "[0-9]*:[0-9]* [AP]M HKT")
    
    echo "📅 日期: $DATE_PART"
    echo "⏰ 時間: $TIME_PART"
    echo "👥 參與者: 媽咪同女兒去"
    echo "🏫 活動: 女兒學校家長日"
    
    # 計算距離時間
    CURRENT_UTC=$(date -u +"%s")
    # 家長日時間 (假設2月28日10:50 AM HKT = 2月28日02:50 UTC)
    PTC_UTC=$(date -u -d "2026-02-28 02:50:00" +"%s" 2>/dev/null || date -u -j -f "%Y-%m-%d %H:%M:%S" "2026-02-28 02:50:00" +"%s")
    
    if [[ -n "$PTC_UTC" ]]; then
        SECONDS_LEFT=$((PTC_UTC - CURRENT_UTC))
        
        if [[ $SECONDS_LEFT -gt 0 ]]; then
            DAYS=$((SECONDS_LEFT / 86400))
            HOURS=$(( (SECONDS_LEFT % 86400) / 3600 ))
            MINUTES=$(( (SECONDS_LEFT % 3600) / 60 ))
            
            echo ""
            echo "⏳ 距離家長日還有:"
            echo "   $DAYS 天 $HOURS 小時 $MINUTES 分鐘"
            
            # 提醒邏輯
            if [[ $DAYS -eq 0 ]] && [[ $HOURS -lt 24 ]]; then
                echo ""
                echo "🔔 溫馨提示: 家長日就在明天！"
                echo "• 準備好女兒的成績單和作品"
                echo "• 確認學校地址和交通方式"
                echo "• 準備想問老師的問題"
            elif [[ $DAYS -eq 1 ]]; then
                echo ""
                echo "📝 提前準備: 家長日還有1天"
                echo "• 提醒女兒準備好書包"
                echo "• 確認媽咪時間安排"
                echo "• 查看天氣預報"
            fi
        else
            echo ""
            echo "✅ 家長日已過去"
        fi
    fi
else
    echo "❌ 未找到家長日提醒"
fi

echo ""
echo "📱 其他提醒:"
echo "-----------"

# 檢查Pickleball提醒
PICKLEBALL_INFO=$(grep "Pickleball" HEARTBEAT.md)
if [[ -n "$PICKLEBALL_INFO" ]]; then
    echo "🎾 Pickleball活動:"
    echo "$PICKLEBALL_INFO" | sed 's/- \*\*//g; s/\*\*://g'
fi

echo ""
echo "💡 家長日準備建議:"
echo "----------------"
echo "1. 📚 帶齊女兒的成績單和作業"
echo "2. 🎨 準備女兒的優秀作品展示"
echo "3. ❓ 列出想問老師的問題"
echo "4. 🚗 提前規劃交通路線"
echo "5. ⏰ 提前10-15分鐘到達學校"
echo "6. 📱 保持手機暢通"
echo "7. 🎯 關注女兒的學習進度和需求"
echo "8. 🤝 與老師建立良好溝通"

echo ""
echo "🎯 家長日目標:"
echo "------------"
echo "• 了解女兒在校表現"
echo "• 與老師建立聯繫"
echo "• 獲取學習建議"
echo "• 支持女兒成長"

echo ""
echo "📅 下次檢查: 系統會定期檢查提醒"
echo "📍 當前時區: UTC (香港時間需+8小時)"