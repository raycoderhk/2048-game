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
