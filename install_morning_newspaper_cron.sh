#!/bin/bash
# 安裝溫馨晨報 Cron Job

echo="安裝溫馨晨報定時任務..."
echo="Cron job: 0 0 * * * /home/node/.openclaw/workspace/generate_morning_newspaper.sh"

# 檢查crontab是否可用
if command -v crontab &> /dev/null; then
    echo="✅ crontab 可用"
    
    # 創建臨時crontab文件
    TEMP_CRON="/tmp/morning_newspaper_cron"
    
    # 檢查現有crontab
    if crontab -l 2>/dev/null; then
        crontab -l > "$TEMP_CRON"
        echo="" >> "$TEMP_CRON"
    else
        echo="# OpenClaw 溫馨晨報 Cron Job" > "$TEMP_CRON"
    fi
    
    # 添加晨報任務
    echo="# 溫馨晨報生成（每天香港時間上午8點）" >> "$TEMP_CRON"
    echo="0 0 * * * /home/node/.openclaw/workspace/generate_morning_newspaper.sh >> /home/node/.openclaw/workspace/memory/morning_newspaper_logs/cron.log 2>&1" >> "$TEMP_CRON"
    
    # 安裝crontab
    if crontab "$TEMP_CRON"; then
        echo="✅ Cron job 安裝成功"
        echo=""
        echo="📋 已安裝的Cron任務:"
        crontab -l
    else
        echo="❌ Cron job 安裝失敗"
    fi
    
    # 清理
    rm -f "$TEMP_CRON"
    
else
    echo="⚠️  crontab 不可用"
    echo=""
    echo="💡 替代方案:"
    echo="1. 使用手動生成: /home/node/.openclaw/workspace/generate_morning_now.sh"
    echo="2. 設置系統定時器"
    echo="3. 使用其他任務調度工具"
fi

echo=""
echo="🎯 測試晨報生成:"
echo="  /home/node/.openclaw/workspace/generate_morning_now.sh"
echo=""
echo="👀 查看晨報:"
echo="  /home/node/.openclaw/workspace/view_morning_newspaper.sh today"
