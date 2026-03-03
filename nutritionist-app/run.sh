#!/bin/bash
# 營養師 App - 快速啟動腳本
# 自動載入 .env 環境變數

set -a  # 自動 export 所有變量
source .env 2>/dev/null || . ./.env 2>/dev/null
set +a

# 檢查 API Key
if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "❌ 錯誤：OPENROUTER_API_KEY 未設定"
    echo "請編輯 .env 文件並設置 API Key"
    exit 1
fi

# 執行程式
if [ -z "$1" ]; then
    echo "使用方法：./run.sh <圖片路徑>"
    echo ""
    echo "範例:"
    echo "  ./run.sh test_food.jpg"
    echo "  ./run.sh test_beef_broccoli.jpg"
    exit 1
fi

# 選擇版本
if [ "$1" = "--only" ]; then
    shift
    echo "🚀 使用 MiniMax-01 ONLY 版本..."
    python3 nutritionist_openrouter_only.py "$@"
else
    echo "🚀 使用 OpenRouter + Aliyun 雙模型版本..."
    python3 nutritionist_openrouter.py "$@"
fi
