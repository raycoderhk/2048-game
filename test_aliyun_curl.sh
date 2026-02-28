#!/bin/bash

echo "🔧 阿里雲Coding Plan API測試"
echo "============================================================"

# 獲取API密鑰
API_KEY="${ALIYUN_API_KEY}"
if [ -z "$API_KEY" ]; then
    echo "❌ 未找到ALIYUN_API_KEY環境變量"
    exit 1
fi

echo "🔑 API密鑰: ${API_KEY:0:10}...${API_KEY: -4}"
echo "🌐 API地址: https://coding.dashscope.aliyuncs.com/v1"

# 測試API連接
echo ""
echo "📡 測試API連接..."
curl -s -X POST "https://coding.dashscope.aliyuncs.com/v1/chat/completions" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen-turbo-latest",
    "messages": [
      {"role": "system", "content": "你是一個有用的助手。"},
      {"role": "user", "content": "你好！請簡單回應以確認API連接正常。"}
    ],
    "max_tokens": 50
  }' \
  -w "\n📊 HTTP狀態碼: %{http_code}\n" \
  --max-time 30

echo ""
echo "============================================================"
echo "💡 如果看到HTTP狀態碼200和AI回應，表示API連接成功！"
echo "💡 如果看到錯誤，請檢查："
echo "   1. API密鑰是否正確"
echo "   2. 是否已訂閱Coding Plan服務"
echo "   3. 網絡連接是否正常"