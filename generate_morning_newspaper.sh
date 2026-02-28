#!/bin/bash
# 溫馨晨報生成腳本
# 每天上午8點（香港時間）運行

echo "📰 $(date) - 開始生成溫馨晨報"
echo "=================================="

WORKSPACE="/home/node/.openclaw/workspace"
cd "$WORKSPACE"

# 設置日誌
LOG_DIR="$WORKSPACE/memory/morning_newspaper_logs"
mkdir -p "$LOG_DIR"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$LOG_DIR/morning_newspaper_${TIMESTAMP}.log"

echo "日誌文件: $LOG_FILE" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 運行晨報生成器
echo "運行晨報編輯器..." | tee -a "$LOG_FILE"
python3 "$WORKSPACE/skills/morning_newspaper_editor.py" 2>&1 | tee -a "$LOG_FILE"

EXIT_CODE=${PIPESTATUS[0]}

echo "" | tee -a "$LOG_FILE"
echo "生成完成時間: $(date)" | tee -a "$LOG_FILE"
echo "退出碼: $EXIT_CODE" | tee -a "$LOG_FILE"

# 檢查結果
TODAY=$(date +"%Y%m%d")
NEWSPAPER_FILE="$WORKSPACE/memory/morning_newspapers/morning_newspaper_${TODAY}.txt"

if [ $EXIT_CODE -eq 0 ] && [ -f "$NEWSPAPER_FILE" ]; then
    echo "✅ 晨報生成成功: $NEWSPAPER_FILE" | tee -a "$LOG_FILE"
    
    # 顯示報紙統計
    LINE_COUNT=$(wc -l < "$NEWSPAPER_FILE")
    FILE_SIZE=$(du -h "$NEWSPAPER_FILE" | cut -f1)
    
    echo "" | tee -a "$LOG_FILE"
    echo "📊 晨報統計:" | tee -a "$LOG_FILE"
    echo "• 行數: $LINE_COUNT" | tee -a "$LOG_FILE"
    echo "• 文件大小: $FILE_SIZE" | tee -a "$LOG_FILE"
    
    # 發送到Telegram
    echo "" | tee -a "$LOG_FILE"
    echo "📤 準備發送到Telegram (7027796937)..." | tee -a "$LOG_FILE"
    
    # 讀取晨報內容
    NEWSPAPER_CONTENT=$(cat "$NEWSPAPER_FILE")
    
    # 發送消息
    echo "發送晨報內容..." | tee -a "$LOG_FILE"
    echo "內容長度: ${#NEWSPAPER_CONTENT} 字符" | tee -a "$LOG_FILE"
    
    # 這裡實際發送消息
    # message action=send to=7027796937 message="$NEWSPAPER_CONTENT"
    
    echo "💡 提示: 晨報已準備好發送" | tee -a "$LOG_FILE"
    echo "使用命令: message action=send to=7027796937 message=\"晨報內容\"" | tee -a "$LOG_FILE"
    
else
    echo "❌ 晨報生成失敗或文件未創建" | tee -a "$LOG_FILE"
    
    # 創建簡易晨報
    SIMPLE_PAPER="$WORKSPACE/memory/morning_newspapers/simple_morning_${TODAY}.txt"
    cat > "$SIMPLE_PAPER" << SIMPLEEOF
📰 溫馨晨報 - $(date +"%Y年%m月%d日")

🌤️ 【今日天氣】
天氣數據暫時無法獲取
建議查看天文台最新資訊

💡 【溫馨提示】
記得按時食藥
保持心情愉快
多與家人聯繫

🎯 【今日建議】
• 適當室內活動
• 均衡飲食
• 充足休息

生成時間: $(date)
註：完整晨報服務稍後恢復
SIMPLEEOF
    
    echo "✅ 已生成簡易晨報: $SIMPLE_PAPER" | tee -a "$LOG_FILE"
fi

# 清理舊日誌（保留30天）
find "$LOG_DIR" -name "morning_newspaper_*.log" -mtime +30 -delete 2>/dev/null
find "$WORKSPACE/memory/morning_newspapers" -name "morning_newspaper_*.txt" -mtime +30 -delete 2>/dev/null
find "$WORKSPACE/memory/morning_newspapers" -name "simple_morning_*.txt" -mtime +7 -delete 2>/dev/null

echo "" | tee -a "$LOG_FILE"
echo "🧹 已清理30天前的舊文件" | tee -a "$LOG_FILE"

exit $EXIT_CODE