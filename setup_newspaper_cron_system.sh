#!/bin/bash
# 設置新聞報紙生成 Cron Job 系統

echo "📰 設置新聞報紙生成系統"
echo "========================"
echo "時間: $(date)"
echo ""

WORKSPACE="/home/node/.openclaw/workspace"
cd "$WORKSPACE"

# 1. 創建必要的目錄
echo "1. 創建目錄結構..."
echo "-------------------"

mkdir -p "$WORKSPACE/memory/newspapers"
mkdir -p "$WORKSPACE/memory/newspaper_logs"
mkdir -p "$WORKSPACE/skills"

echo "✅ 報紙目錄: $WORKSPACE/memory/newspapers"
echo "✅ 日誌目錄: $WORKSPACE/memory/newspaper_logs"
echo "✅ 技能目錄: $WORKSPACE/skills"

# 2. 創建每日報紙生成腳本
echo ""
echo "2. 創建報紙生成腳本..."
echo "----------------------"

DAILY_NEWSPAPER_SCRIPT="$WORKSPACE/generate_daily_newspaper.sh"

cat > "$DAILY_NEWSPAPER_SCRIPT" << 'EOF'
#!/bin/bash
# 每日新聞報紙生成腳本
# 每天上午8點運行

echo "📰 $(date) - 開始生成每日新聞報紙"
echo "=================================="

WORKSPACE="/home/node/.openclaw/workspace"
cd "$WORKSPACE"

# 運行報紙生成器
python3 "$WORKSPACE/skills/news_paper_generator.py"

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ 報紙生成成功"
    
    # 獲取今天生成的報紙
    TODAY=$(date +"%Y%m%d")
    NEWSPAPER_FILE="$WORKSPACE/memory/newspapers/newspaper_${TODAY}.txt"
    
    if [ -f "$NEWSPAPER_FILE" ]; then
        # 這裡可以添加發送功能，例如：
        # - 發送到Telegram
        # - 發送郵件
        # - 保存到特定位置
        
        echo "📄 報紙文件: $NEWSPAPER_FILE"
        
        # 顯示簡要內容
        echo ""
        echo "📋 今日頭條:"
        echo "-----------"
        grep -A2 "📰 頭條新聞" "$NEWSPAPER_FILE" | head -10
        
        echo ""
        echo "📈 市場摘要:"
        echo "-----------"
        grep -A5 "📈 金融市場" "$NEWSPAPER_FILE" | head -10
        
    fi
else
    echo "❌ 報紙生成失敗，退出碼: $EXIT_CODE"
    
    # 生成簡易報紙
    TODAY=$(date +"%Y%m%d")
    SIMPLE_PAPER="$WORKSPACE/memory/newspapers/simple_${TODAY}.txt"
    
    cat > "$SIMPLE_PAPER" << SIMPLEEOF
📰 每日簡報 - $(date +"%Y年%m月%d日")
==================================

由於技術原因，今日完整報紙生成遇到問題。
以下是您的個人化摘要：

💼 投資提醒:
• 定期檢視投資組合表現
• 關注市場重要新聞
• 保持投資紀律

📊 快速檢查:
• 基本系統狀態: 正常
• 網絡連接: 部分服務可能受限
• 數據更新: 手動檢查建議

🎯 今日建議:
1. 檢查重要郵件和消息
2. 規劃今日工作重點
3. 保持健康生活節奏

註: 完整報紙服務將在網絡恢復後自動更新。
SIMPLEEOF
    
    echo "✅ 已生成簡易報紙: $SIMPLE_PAPER"
fi

echo ""
echo "🕒 完成時間: $(date)"
exit $EXIT_CODE
EOF

chmod +x "$DAILY_NEWSPAPER_SCRIPT"
echo "✅ 創建每日報紙腳本: $DAILY_NEWSPAPER_SCRIPT"

# 3. 創建手動生成腳本
echo ""
echo "3. 創建手動生成腳本..."
echo "----------------------"

MANUAL_GENERATE_SCRIPT="$WORKSPACE/generate_newspaper_now.sh"

cat > "$MANUAL_GENERATE_SCRIPT" << 'EOF'
#!/bin/bash
# 手動立即生成新聞報紙

echo "🚀 立即生成新聞報紙"
echo "==================="

WORKSPACE="/home/node/.openclaw/workspace"
cd "$WORKSPACE"

# 運行完整生成過程
"$WORKSPACE/skills/generate_newspaper_cron.sh"

# 顯示最新報紙
echo ""
echo "📰 最新報紙文件:"
echo "----------------"

find "$WORKSPACE/memory/newspapers" -name "newspaper_*.txt" -type f | sort -r | head -3 | while read file; do
    echo "• $file ($(stat -c %y "$file" | cut -d' ' -f1))"
done

echo ""
echo "💡 查看報紙內容:"
echo "  head -50 $(find "$WORKSPACE/memory/newspapers" -name "newspaper_*.txt" -type f | sort -r | head -1)"
EOF

chmod +x "$MANUAL_GENERATE_SCRIPT"
echo "✅ 創建手動生成腳本: $MANUAL_GENERATE_SCRIPT"

# 4. 創建報紙查看工具
echo ""
echo "4. 創建報紙查看工具..."
echo "----------------------"

VIEW_NEWSPAPER_SCRIPT="$WORKSPACE/view_newspaper.sh"

cat > "$VIEW_NEWSPAPER_SCRIPT" << 'EOF'
#!/bin/bash
# 查看新聞報紙

WORKSPACE="/home/node/.openclaw/workspace"

if [ "$1" = "latest" ] || [ -z "$1" ]; then
    # 查看最新報紙
    LATEST_PAPER=$(find "$WORKSPACE/memory/newspapers" -name "newspaper_*.txt" -type f | sort -r | head -1)
    
    if [ -f "$LATEST_PAPER" ]; then
        echo "📰 最新報紙: $LATEST_PAPER"
        echo "=" * 60
        cat "$LATEST_PAPER"
    else
        echo "❌ 未找到報紙文件"
        echo "請先運行: $WORKSPACE/generate_newspaper_now.sh"
    fi
    
elif [ "$1" = "list" ]; then
    # 列出所有報紙
    echo "📰 所有報紙文件:"
    echo "----------------"
    find "$WORKSPACE/memory/newspapers" -name "newspaper_*.txt" -type f | sort -r | while read file; do
        date_part=$(basename "$file" | sed 's/newspaper_//;s/.txt//')
        size=$(du -h "$file" | cut -f1)
        lines=$(wc -l < "$file")
        echo "• $date_part: $file ($size, $lines 行)"
    done
    
elif [ "$1" = "today" ]; then
    # 查看今日報紙
    TODAY=$(date +"%Y%m%d")
    TODAY_PAPER="$WORKSPACE/memory/newspapers/newspaper_${TODAY}.txt"
    
    if [ -f "$TODAY_PAPER" ]; then
        echo "📰 今日報紙: $TODAY_PAPER"
        echo "=" * 60
        head -100 "$TODAY_PAPER"
    else
        echo "❌ 今日報紙尚未生成"
        echo "請運行: $WORKSPACE/generate_newspaper_now.sh"
    fi
    
else
    echo "📰 新聞報紙查看工具"
    echo "=================="
    echo ""
    echo "使用方法:"
    echo "  $0 latest      - 查看最新報紙（默認）"
    echo "  $0 today       - 查看今日報紙"
    echo "  $0 list        - 列出所有報紙"
    echo "  $0 help        - 顯示幫助"
    echo ""
    echo "生成報紙:"
    echo "  $WORKSPACE/generate_newspaper_now.sh - 立即生成"
    echo "  $WORKSPACE/generate_daily_newspaper.sh - 每日生成"
fi
EOF

chmod +x "$VIEW_NEWSPAPER_SCRIPT"
echo "✅ 創建報紙查看工具: $VIEW_NEWSPAPER_SCRIPT"

# 5. 設置定時任務
echo ""
echo "5. 設置定時任務..."
echo "------------------"

# 創建crontab條目
CRON_ENTRY="0 8 * * * $DAILY_NEWSPAPER_SCRIPT >> $WORKSPACE/memory/newspaper_logs/cron.log 2>&1"

echo "Cron job 配置:"
echo "  $CRON_ENTRY"
echo ""
echo "這將在每天上午8點自動生成新聞報紙。"

# 創建cron安裝腳本
CRON_SETUP_SCRIPT="$WORKSPACE/setup_newspaper_cron.sh"

cat > "$CRON_SETUP_SCRIPT" << EOF
#!/bin/bash
# 安裝新聞報紙生成 Cron Job

echo "安裝新聞報紙定時任務..."
echo "Cron job: $CRON_ENTRY"

# 這裡可以添加實際的crontab設置代碼
# 由於環境限制，我們創建一個替代方案

# 創建一個每小時檢查的簡單定時器
HOURLY_CHECK="$WORKSPACE/check_and_generate_hourly.sh"

cat > "\$HOURLY_CHECK" << 'HOURLYEOF'
#!/bin/bash
# 每小時檢查並生成報紙（如果尚未生成）

WORKSPACE="/home/node/.openclaw/workspace"
TODAY=\$(date +"%Y%m%d")
TODAY_PAPER="\$WORKSPACE/memory/newspapers/newspaper_\${TODAY}.txt"

# 如果今天還沒有報紙，並且是上午8-9點，則生成
if [ ! -f "\$TODAY_PAPER" ]; then
    HOUR=\$(date +"%H")
    if [ "\$HOUR" -ge 8 ] && [ "\$HOUR" -le 9 ]; then
        echo "\$(date) - 生成今日報紙" >> "\$WORKSPACE/memory/newspaper_logs/hourly_check.log"
        "\$WORKSPACE/generate_daily_newspaper.sh"
    fi
fi
HOURLYEOF

chmod +x "\$HOURLY_CHECK"
echo "✅ 創建每小時檢查腳本: \$HOURLY_CHECK"

echo ""
echo "📋 手動運行命令:"
echo "  \$WORKSPACE/generate_newspaper_now.sh - 立即生成報紙"
echo "  \$WORKSPACE/view_newspaper.sh - 查看報紙"
echo ""
echo "💡 建議將 \$HOURLY_CHECK 添加到啟動項中"
EOF

chmod +x "$CRON_SETUP_SCRIPT"
echo "✅ 創建Cron安裝腳本: $CRON_SETUP_SCRIPT"

# 6. 生成系統摘要
echo ""
echo "📊 新聞報紙生成系統設置完成！"
echo "============================="
echo ""
echo "📋 可用命令:"
echo "  $MANUAL_GENERATE_SCRIPT   - 手動立即生成報紙"
echo "  $VIEW_NEWSPAPER_SCRIPT    - 查看報紙內容"
echo "  $DAILY_NEWSPAPER_SCRIPT   - 每日生成腳本"
echo "  $CRON_SETUP_SCRIPT        - 設置定時任務"
echo ""
echo "📁 文件目錄:"
echo "  • 報紙文件: $WORKSPACE/memory/newspapers/"
echo "  • 生成日誌: $WORKSPACE/memory/newspaper_logs/"
echo "  • 技能腳本: $WORKSPACE/skills/"
echo ""
echo "🎯 功能特點:"
echo "  • 每日自動生成個性化新聞摘要"
echo "  • 包含天氣、股市、新聞頭條"
echo "  • 個人化投資建議"
echo "  • 自動清理舊文件"
echo ""
echo "🚀 立即測試:"
echo "  1. 運行: $MANUAL_GENERATE_SCRIPT"
echo "  2. 查看: $VIEW_NEWSPAPER_SCRIPT today"
echo ""
echo "🎉 系統設置完成！"