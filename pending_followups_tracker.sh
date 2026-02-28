#!/bin/bash
# 待辦事項跟進追蹤系統

echo "📋 待辦事項跟進追蹤"
echo "==================="
echo "檢查時間: $(date)"
echo ""

WORKSPACE="/home/node/.openclaw/workspace"
cd "$WORKSPACE"

# 讀取待辦事項
echo "🔍 當前待辦事項列表:"
echo "-------------------"

PENDING_SECTION=$(grep -A10 "## Pending Follow-ups" HEARTBEAT.md | tail -n +2)
if [[ -n "$PENDING_SECTION" ]]; then
    echo "$PENDING_SECTION" | while read line; do
        if [[ -n "$line" ]]; then
            echo "• $line"
        fi
    done
else
    echo "✅ 沒有待辦事項"
fi

echo ""
echo "🏫 兒子學校家長日詳細信息:"
echo "------------------------"

# 提取兒子家長日信息
SON_PTC_INFO=$(grep "兒子學校家長日" HEARTBEAT.md)
if [[ -n "$SON_PTC_INFO" ]]; then
    echo "📝 狀態: 待確認"
    echo ""
    
    # 解析信息
    DATE_PART="下星期六 (March 7, 2026)"
    STATUS="時間未定，需要跟進確認"
    
    echo "📅 預計日期: $DATE_PART"
    echo "⏰ 時間狀態: $STATUS"
    echo "👦 參與者: 兒子 (具體參與者待確認)"
    echo "🏫 活動: 兒子學校家長日"
    
    # 計算距離時間
    CURRENT_UTC=$(date -u +"%s")
    # 下星期六 (3月7日) 假設上午時間
    ESTIMATED_UTC=$(date -u -d "2026-03-07 02:00:00" +"%s" 2>/dev/null || date -u -j -f "%Y-%m-%d %H:%M:%S" "2026-03-07 02:00:00" +"%s")
    
    if [[ -n "$ESTIMATED_UTC" ]]; then
        SECONDS_LEFT=$((ESTIMATED_UTC - CURRENT_UTC))
        
        if [[ $SECONDS_LEFT -gt 0 ]]; then
            DAYS=$((SECONDS_LEFT / 86400))
            
            echo ""
            echo "⏳ 距離預計日期還有: $DAYS 天"
            
            # 提醒邏輯
            if [[ $DAYS -lt 7 ]]; then
                echo ""
                echo "🔔 緊急程度: 高"
                echo "💡 建議: 盡快確認具體時間"
            elif [[ $DAYS -lt 14 ]]; then
                echo ""
                echo "🔔 緊急程度: 中"
                echo "💡 建議: 本周內確認時間"
            else
                echo ""
                echo "🔔 緊急程度: 低"
                echo "💡 建議: 有時間時確認"
            fi
        fi
    fi
else
    echo "❌ 未找到兒子家長日信息"
fi

echo ""
echo "🎯 跟進行動建議:"
echo "---------------"
echo "1. 📞 聯絡學校: 查詢家長日具體時間安排"
echo "2. 📱 查看通知: 檢查學校APP或網站公告"
echo "3. 📧 查看郵件: 檢查學校發送的郵件通知"
echo "4. 📚 詢問老師: 通過通訊群組詢問班主任"
echo "5. 👥 詢問其他家長: 了解其他家長的安排"
echo "6. 🗓️ 確認參與者: 確定哪位家長陪同參加"
echo "7. ⏰ 更新系統: 獲得時間後立即更新提醒"

echo ""
echo "📋 確認清單:"
echo "-----------"
echo "□ 具體日期和時間"
echo "□ 學校地址和教室"
echo "□ 需要帶的文件"
echo "□ 預約時間段（如適用）"
echo "□ 交通安排"
echo "□ 參與家長確認"
echo "□ 準備的問題清單"

echo ""
echo "🏫 兒子家長日特別注意事項:"
echo "-------------------------"
echo "• 👦 關注兒子的學習特點和需求"
echo "• 🏀 了解兒子的課外活動參與情況"
echo "• 🤝 關注兒子的社交發展"
echo "• 📊 討論兒子的學業進步空間"
echo "• 🎯 設定適合兒子的學習目標"
echo "• 💪 鼓勵兒子的優勢和特長"

echo ""
echo "📊 待辦事項管理:"
echo "---------------"
echo "• 定期檢查HEARTBEAT.md更新狀態"
echo "• 獲得時間後立即更新提醒系統"
echo "• 設置確認時間的截止日期"
echo "• 考慮備用時間安排"

echo ""
echo "💡 時間確認後的下一步:"
echo "-------------------"
echo "1. 更新HEARTBEAT.md中的具體時間"
echo "2. 添加到日曆應用程序"
echo "3. 設置提前提醒（提前1天、1小時）"
echo "4. 準備家長日相關材料"
echo "5. 規劃交通和時間安排"

echo ""
echo "📅 下次跟進檢查: 系統會定期檢查待辦事項"
echo "⏰ 建議確認截止時間: 3月4日（下星期三）前"
echo "📍 當前時區: UTC (香港時間需+8小時)"