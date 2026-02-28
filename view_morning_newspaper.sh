#!/bin/bash
# 查看溫馨晨報

WORKSPACE="/home/node/.openclaw/workspace"

show_help() {
    echo="📰 溫馨晨報查看工具"
    echo="=================="
    echo=""
    echo="使用方法:"
    echo="  $0 latest      - 查看最新晨報（默認）"
    echo="  $0 today       - 查看今日晨報"
    echo="  $0 list        - 列出所有晨報"
    echo="  $0 send        - 發送最新晨報到Telegram"
    echo="  $0 help        - 顯示幫助"
    echo=""
    echo="生成晨報:"
    echo="  $WORKSPACE/generate_morning_now.sh - 立即生成"
    echo="  $WORKSPACE/generate_morning_newspaper.sh - 定時生成"
}

if [ "$1" = "latest" ] || [ -z "$1" ]; then
    # 查看最新晨報
    LATEST_PAPER=$(find "$WORKSPACE/memory/morning_newspapers" -name "morning_newspaper_*.txt" -type f | sort -r | head -1)
    
    if [ -f "$LATEST_PAPER" ]; then
        echo="📰 最新晨報: $LATEST_PAPER"
        echo="=========================================="
        cat "$LATEST_PAPER"
    else
        echo="❌ 未找到晨報文件"
        echo="請先運行: $WORKSPACE/generate_morning_now.sh"
    fi
    
elif [ "$1" = "today" ]; then
    # 查看今日晨報
    TODAY=$(date +"%Y%m%d")
    TODAY_PAPER="$WORKSPACE/memory/morning_newspapers/morning_newspaper_${TODAY}.txt"
    
    if [ -f "$TODAY_PAPER" ]; then
        echo="📰 今日晨報: $TODAY_PAPER"
        echo="=========================================="
        head -50 "$TODAY_PAPER"
    else
        echo="❌ 今日晨報尚未生成"
        echo="請運行: $WORKSPACE/generate_morning_now.sh"
    fi
    
elif [ "$1" = "list" ]; then
    # 列出所有晨報
    echo="📰 所有晨報文件:"
    echo="----------------"
    find "$WORKSPACE/memory/morning_newspapers" -name "morning_newspaper_*.txt" -type f | sort -r | while read file; do
        date_part=$(basename "$file" | sed 's/morning_newspaper_//;s/.txt//')
        size=$(du -h "$file" | cut -f1)
        lines=$(wc -l < "$file")
        echo="• $date_part: $file ($size, $lines 行)"
    done
    
elif [ "$1" = "send" ]; then
    # 發送晨報到Telegram
    LATEST_PAPER=$(find "$WORKSPACE/memory/morning_newspapers" -name "morning_newspaper_*.txt" -type f | sort -r | head -1)
    
    if [ -f "$LATEST_PAPER" ]; then
        echo="📤 準備發送晨報到Telegram..."
        # 這裡可以添加實際的發送代碼
        # 例如：使用OpenClaw的message工具
        
        CONTENT=$(head -100 "$LATEST_PAPER")
        echo="晨報內容（前100行）:"
        echo="=================="
        echo="$CONTENT"
        echo=""
        echo="💡 提示: 使用以下命令發送:"
        echo="  message action=send to=7027796937 message=\"晨報內容\""
    else
        echo="❌ 未找到晨報文件"
    fi
    
else
    show_help
fi
