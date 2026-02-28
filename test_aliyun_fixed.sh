#!/bin/bash

echo "🔧 阿里雲 API 測試 (更新後)"
echo "============================================================"

# 獲取 API 密鑰
API_KEY="${ALIYUN_API_KEY}"
if [ -z "$API_KEY" ]; then
    echo "❌ 未找到 ALIYUN_API_KEY 環境變量"
    exit 1
fi

echo "🔑 API 密鑰：${API_KEY:0:10}...${API_KEY: -4}"
echo "🌐 API 地址：https://dashscope.aliyuncs.com/compatible-mode/v1"
echo "📦 測試模型：qwen-plus"

# 測試 API 連接
echo ""
echo "📡 測試 API 連接..."
curl -s -X POST "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen-plus",
    "messages": [
      {"role": "system", "content": "你是一個有用的助手。"},
      {"role": "user", "content": "你好！請簡單回應以確認 API 連接正常。"}
    ],
    "max_tokens": 50
  }' \
  -w "\n📊 HTTP 狀態碼：%{http_code}\n" \
  --max-time 30

echo ""
echo "============================================================"
