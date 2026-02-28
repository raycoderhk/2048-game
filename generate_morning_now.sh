#!/bin/bash
# 手動立即生成溫馨晨報

echo="🚀 立即生成溫馨晨報"
echo="==================="

WORKSPACE="/home/node/.openclaw/workspace"
cd "$WORKSPACE"

# 運行晨報生成
"$WORKSPACE/generate_morning_newspaper.sh"

# 顯示最新晨報
echo=""
echo="📰 最新晨報文件:"
echo="----------------"

find "$WORKSPACE/memory/morning_newspapers" -name "morning_newspaper_*.txt" -type f | sort -r | head -3 | while read file; do
    date_part=$(basename "$file" | sed 's/morning_newspaper_//;s/.txt//')
    size=$(du -h "$file" | cut -f1)
    lines=$(wc -l < "$file")
    echo="• $date_part: $file ($size, $lines 行)"
done

echo=""
echo="💡 查看晨報內容:"
LATEST=$(find "$WORKSPACE/memory/morning_newspapers" -name "morning_newspaper_*.txt" -type f | sort -r | head -1)
if [ -n "$LATEST" ]; then
    echo="  head -40 \"$LATEST\""
fi
