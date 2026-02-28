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
