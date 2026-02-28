#!/bin/bash

echo "✅ 最終測試 - 阿里雲 Coding Plan API"
echo "============================================================"

API_KEY="sk-sp-8eec812bc72d47c3866d388cef6372f8"

echo "🔑 API Key: ${API_KEY:0:15}...${API_KEY: -4}"
echo "🌐 端點：https://coding.dashscope.aliyuncs.com/v1"
echo "📦 模型：qwen3.5-plus"
echo ""

RESPONSE=$(curl -s -X POST "https://coding.dashscope.aliyuncs.com/v1/chat/completions" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3.5-plus",
    "messages": [
      {"role": "system", "content": "你是一個有用的助手。"},
      {"role": "user", "content": "你好！請用一句話確認 API 連接正常。"}
    ],
    "max_tokens": 50
  }' \
  -w "\n\nHTTP_CODE:%{http_code}" \
  --max-time 30)

HTTP_CODE=$(echo "$RESPONSE" | grep -o "HTTP_CODE:[0-9]*" | cut -d: -f2)
BODY=$(echo "$RESPONSE" | sed 's/HTTP_CODE:[0-9]*//')

echo "📊 響應狀態碼：$HTTP_CODE"
echo ""

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ API 連接成功！"
    echo ""
    echo "🤖 AI 回應:"
    echo "$BODY" | grep -o '"content":"[^"]*"' | head -1 | sed 's/"content":"//g' | sed 's/"//g' | sed 's/\\n/\n/g'
    echo ""
    echo ""
    echo "🎉 配置完成！OpenClaw 現在可以使用阿里雲 Coding Plan！"
    echo ""
    echo "📋 可用模型:"
    echo "   • aliyun/qwen3.5-plus (主要推薦)"
    echo "   • aliyun/qwen3-coder-plus (編碼專用)"
    echo "   • aliyun/qwen3-max-2026-01-23 (最強推理)"
    echo ""
    echo "💰 收費：包月制（已訂閱 Coding Plan）"
    echo "🎯 在額度內無限使用，不用擔心 token 費用！"
else
    echo "❌ API 連接失敗"
    echo ""
    echo "錯誤信息:"
    echo "$BODY" | grep -o '"message":"[^"]*"' | head -1
fi

echo ""
echo "============================================================"
