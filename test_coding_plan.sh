#!/bin/bash

echo "🔍 測試 Coding Plan API"
echo "============================================================"

API_KEY="sk-sp-8eec812bc72d47c3866d388cef6372f8"

echo "🔑 API Key: ${API_KEY:0:15}...${API_KEY: -4}"
echo ""

# 測試 Coding Plan 專用端點
echo "📡 測試端點：https://coding.dashscope.aliyuncs.com/v1"
echo ""

# 嘗試不同的模型名稱
MODELS=("qwen-plus" "qwen3.5-plus" "qwen-coder-plus" "qwen-max")

for MODEL in "${MODELS[@]}"; do
    echo "🧪 測試模型：$MODEL"
    RESPONSE=$(curl -s -X POST "https://coding.dashscope.aliyuncs.com/v1/chat/completions" \
      -H "Authorization: Bearer $API_KEY" \
      -H "Content-Type: application/json" \
      -d "{\"model\":\"$MODEL\",\"messages\":[{\"role\":\"user\",\"content\":\"hi\"}],\"max_tokens\":10}" \
      -w "\nHTTP:%{http_code}" \
      --max-time 20)
    
    HTTP_CODE=$(echo "$RESPONSE" | grep -o "HTTP:[0-9]*" | cut -d: -f2)
    BODY=$(echo "$RESPONSE" | sed 's/HTTP:[0-9]*//')
    
    echo "   狀態碼：$HTTP_CODE"
    if [ "$HTTP_CODE" = "200" ]; then
        echo "   ✅ 成功！"
        echo "   響應：$(echo "$BODY" | head -c 150)"
        echo ""
        echo "🎉 找到正確的模型：$MODEL"
        echo ""
        break
    else
        ERROR=$(echo "$BODY" | grep -o '"message":"[^"]*"' | head -1)
        echo "   ❌ 失敗：$ERROR"
    fi
    echo ""
done

echo "============================================================"
echo ""
echo "💡 如果所有模型都失敗，可能原因："
echo "   1. API Key 需要時間生效（等待 5-10 分鐘）"
echo "   2. 需要在 Zeabur 重啟服務"
echo "   3. 訂閱還未激活"
