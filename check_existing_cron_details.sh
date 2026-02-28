#!/bin/bash
# 檢查現有定時任務詳細信息

echo "📋 現有定時任務詳細信息"
echo "========================"
echo "檢查時間: $(date)"
echo ""

WORKSPACE="/home/node/.openclaw/workspace"

echo "1. 技能監控系統定時任務:"
echo "------------------------"

# 檢查技能監控相關腳本
echo "• 每小時檢查: $WORKSPACE/check_skills_hourly.sh"
if [ -f "$WORKSPACE/check_skills_hourly.sh" ]; then
    echo "  狀態: ✅ 存在"
    echo "  功能: 每小時運行基本技能檢查"
    echo "  預計運行: 每小時一次"
else
    echo "  狀態: ❌ 不存在"
fi

echo ""
echo "• 每日詳細檢查: $WORKSPACE/check_skills_daily.sh"
if [ -f "$WORKSPACE/check_skills_daily.sh" ]; then
    echo "  狀態: ✅ 存在"
    echo "  功能: 每日運行完整技能檢查"
    echo "  預計運行: 每天一次"
else
    echo "  狀態: ❌ 不存在"
fi

echo ""
echo "• 持續監控: $WORKSPACE/start_monitoring.sh"
if [ -f "$WORKSPACE/start_monitoring.sh" ]; then
    echo "  狀態: ✅ 存在"
    echo "  功能: 啟動持續監控（每小時檢查+循環）"
    echo "  運行方式: 手動啟動，持續運行"
else
    echo "  狀態: ❌ 不存在"
fi

echo ""
echo "2. 新聞報紙生成系統定時任務:"
echo "---------------------------"

echo "• 每日報紙生成: $WORKSPACE/generate_daily_newspaper.sh"
if [ -f "$WORKSPACE/generate_daily_newspaper.sh" ]; then
    echo "  狀態: ✅ 存在"
    echo "  功能: 生成每日新聞報紙"
    echo "  預計運行: 每天上午8點"
    
    # 檢查腳本內容
    if grep -q "8點" "$WORKSPACE/generate_daily_newspaper.sh"; then
        echo "  時間配置: 上午8點"
    fi
else
    echo "  狀態: ❌ 不存在"
fi

echo ""
echo "• 每小時檢查生成: $WORKSPACE/check_and_generate_hourly.sh"
if [ -f "$WORKSPACE/check_and_generate_hourly.sh" ]; then
    echo "  狀態: ✅ 存在"
    echo "  功能: 每小時檢查是否需要生成報紙"
    echo "  運行條件: 如果當天尚未生成報紙，且在上午8-9點"
else
    echo "  狀態: ❌ 不存在（將在設置cron時創建）"
fi

echo ""
echo "3. 手動執行腳本:"
echo "---------------"

echo "• 立即技能檢查: $WORKSPACE/check_skills_now.sh"
[ -f "$WORKSPACE/check_skills_now.sh" ] && echo "  狀態: ✅ 存在" || echo "  狀態: ❌ 不存在"

echo "• 立即生成報紙: $WORKSPACE/generate_newspaper_now.sh"
[ -f "$WORKSPACE/generate_newspaper_now.sh" ] && echo "  狀態: ✅ 存在" || echo "  狀態: ❌ 不存在"

echo "• 查看報紙: $WORKSPACE/view_newspaper.sh"
[ -f "$WORKSPACE/view_newspaper.sh" ] && echo "  狀態: ✅ 存在" || echo "  狀態: ❌ 不存在"

echo ""
echo "4. 設置腳本:"
echo "-----------"

echo "• 設置技能監控cron: $WORKSPACE/setup_skill_monitor_cron.sh"
[ -f "$WORKSPACE/setup_skill_monitor_cron.sh" ] && echo "  狀態: ✅ 存在" || echo "  狀態: ❌ 不存在"

echo "• 設置報紙生成cron: $WORKSPACE/setup_newspaper_cron.sh"
[ -f "$WORKSPACE/setup_newspaper_cron.sh" ] && echo "  狀態: ✅ 存在" || echo "  狀態: ❌ 不存在"

echo ""
echo "5. 實際的定時執行機制:"
echo "---------------------"

echo "由於系統crontab不可用，我們使用以下替代方案:"
echo ""
echo "a) 手動啟動持續監控:"
echo "   $WORKSPACE/start_monitoring.sh"
echo "   • 啟動後會每小時運行技能檢查"
echo "   • 需要手動啟動並保持運行"
echo ""
echo "b) 計劃的cron配置（需要手動設置）:"
echo "   0 8 * * * $WORKSPACE/generate_daily_newspaper.sh"
echo "   0 * * * * $WORKSPACE/check_skills_hourly.sh"
echo "   0 9 * * * $WORKSPACE/check_skills_daily.sh"
echo ""
echo "c) 替代定時器文件:"
if [ -f "$WORKSPACE/skills-monitor.timer" ]; then
    echo "   • skills-monitor.timer: systemd定時器（需要systemctl）"
fi
if [ -f "$WORKSPACE/skills-monitor.service" ]; then
    echo "   • skills-monitor.service: systemd服務（需要systemctl）"
fi

echo ""
echo "6. 日誌文件位置:"
echo "---------------"

echo "• 技能檢查日誌: $WORKSPACE/memory/skill_checks/"
if [ -d "$WORKSPACE/memory/skill_checks" ]; then
    echo "  狀態: ✅ 目錄存在"
    echo "  文件數: $(find "$WORKSPACE/memory/skill_checks" -type f 2>/dev/null | wc -l)"
else
    echo "  狀態: ❌ 目錄不存在"
fi

echo ""
echo "• 報紙生成日誌: $WORKSPACE/memory/newspaper_logs/"
if [ -d "$WORKSPACE/memory/newspaper_logs" ]; then
    echo "  狀態: ✅ 目錄存在"
    echo "  文件數: $(find "$WORKSPACE/memory/newspaper_logs" -type f 2>/dev/null | wc -l)"
else
    echo "  狀態: ❌ 目錄不存在"
fi

echo ""
echo "• 報紙文件: $WORKSPACE/memory/newspapers/"
if [ -d "$WORKSPACE/memory/newspapers" ]; then
    echo "  狀態: ✅ 目錄存在"
    echo "  文件數: $(find "$WORKSPACE/memory/newspapers" -type f 2>/dev/null | wc -l)"
    echo "  最新文件: $(find "$WORKSPACE/memory/newspapers" -name "*.txt" -type f -exec ls -lt {} + 2>/dev/null | head -1 | awk '{print $NF}')"
else
    echo "  狀態: ❌ 目錄不存在"
fi

echo ""
echo "7. 建議的完整cron配置:"
echo "---------------------"

cat << EOF
# OpenClaw 定時任務配置
# =====================

# 技能監控
0 * * * *   $WORKSPACE/check_skills_hourly.sh >> $WORKSPACE/memory/skill_checks/hourly.log 2>&1
0 9 * * *   $WORKSPACE/check_skills_daily.sh >> $WORKSPACE/memory/skill_checks/daily.log 2>&1

# 新聞報紙生成
0 8 * * *   $WORKSPACE/generate_daily_newspaper.sh >> $WORKSPACE/memory/newspaper_logs/daily.log 2>&1

# 文件清理
0 0 * * *   find $WORKSPACE/memory/skill_checks -name "*.log" -mtime +30 -delete
0 0 * * *   find $WORKSPACE/memory/newspaper_logs -name "*.log" -mtime +30 -delete
0 0 * * *   find $WORKSPACE/memory/newspapers -name "*.txt" -mtime +30 -delete

EOF

echo ""
echo "📊 總結:"
echo "------"
echo "✅ 已創建完整的定時任務腳本系統"
echo "⚠️  需要手動設置crontab或使用替代運行方式"
echo "💡 建議: 使用 start_monitoring.sh 啟動持續監控"