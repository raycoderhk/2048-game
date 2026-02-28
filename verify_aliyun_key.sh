#!/bin/bash

echo "🔍 阿里雲 API 密鑰驗證工具"
echo "============================================================"
echo ""

API_KEY="${ALIYUN_API_KEY}"

if [ -z "$API_KEY" ]; then
    echo "❌ 錯誤：未找到 ALIYUN_API_KEY 環境變量"
    exit 1
fi

echo "📋 API 密鑰信息:"
echo "   格式：${API_KEY:0:15}...${API_KEY: -4}"
echo "   長度：${#API_KEY} 字符"
echo ""

# 測試不同的 API 端點
echo "🔧 測試不同 API 端點..."
echo ""

# 端點 1: DashScope 兼容模式
echo "1️⃣  DashScope 兼容模式:"
echo "   URL: https://dashscope.aliyuncs.com/compatible-mode/v1"
RESPONSE1=$(curl -s -X POST "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen-plus","messages":[{"role":"user","content":"hi"}],"max_tokens":10}' \
  -w "\nHTTP_CODE:%{http_code}" \
  --max-time 15)

HTTP_CODE1=$(echo "$RESPONSE1" | grep -o "HTTP_CODE:[0-9]*" | cut -d: -f2)
BODY1=$(echo "$RESPONSE1" | sed 's/HTTP_CODE:[0-9]*//')

echo "   狀態碼：$HTTP_CODE1"
if [ "$HTTP_CODE1" = "200" ]; then
    echo "   ✅ 成功！"
    echo "   響應：$(echo "$BODY1" | head -c 200)"
else
    echo "   ❌ 失敗"
    echo "   錯誤：$(echo "$BODY1" | grep -o '"message":"[^"]*"' | head -1)"
fi
echo ""

# 端點 2: DashScope 原生 API
echo "2️⃣  DashScope 原生 API:"
echo "   URL: https://dashscope.aliyuncs.com/api/v1"
RESPONSE2=$(curl -s -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen-plus","input":{"messages":[{"role":"user","content":"hi"}]}}' \
  -w "\nHTTP_CODE:%{http_code}" \
  --max-time 15)

HTTP_CODE2=$(echo "$RESPONSE2" | grep -o "HTTP_CODE:[0-9]*" | cut -d: -f2)
BODY2=$(echo "$RESPONSE2" | sed 's/HTTP_CODE:[0-9]*//')

echo "   狀態碼：$HTTP_CODE2"
if [ "$HTTP_CODE2" = "200" ]; then
    echo "   ✅ 成功！"
else
    echo "   ❌ 失敗"
    echo "   錯誤：$(echo "$BODY2" | grep -o '"message":"[^"]*"' | head -1)"
fi
echo ""

# 端點 3: Coding Plan 專用
echo "3️⃣  Coding Plan 專用端點:"
echo "   URL: https://coding.dashscope.aliyuncs.com/v1"
RESPONSE3=$(curl -s -X POST "https://coding.dashscope.aliyuncs.com/v1/chat/completions" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen-plus","messages":[{"role":"user","content":"hi"}],"max_tokens":10}' \
  -w "\nHTTP_CODE:%{http_code}" \
  --max-time 15)

HTTP_CODE3=$(echo "$RESPONSE3" | grep -o "HTTP_CODE:[0-9]*" | cut -d: -f2)
BODY3=$(echo "$RESPONSE3" | sed 's/HTTP_CODE:[0-9]*//')

echo "   狀態碼：$HTTP_CODE3"
if [ "$HTTP_CODE3" = "200" ]; then
    echo "   ✅ 成功！"
    echo "   響應：$(echo "$BODY3" | head -c 200)"
else
    echo "   ❌ 失敗"
    echo "   錯誤：$(echo "$BODY3" | grep -o '"message":"[^"]*"' | head -1)"
fi
echo ""

# 端點 4: 檢查模型列表
echo "4️⃣  檢查可用模型列表:"
RESPONSE4=$(curl -s -X GET "https://dashscope.aliyuncs.com/compatible-mode/v1/models" \
  -H "Authorization: Bearer $API_KEY" \
  -w "\nHTTP_CODE:%{http_code}" \
  --max-time 15)

HTTP_CODE4=$(echo "$RESPONSE4" | grep -o "HTTP_CODE:[0-9]*" | cut -d: -f2)
BODY4=$(echo "$RESPONSE4" | sed 's/HTTP_CODE:[0-9]*//')

echo "   狀態碼：$HTTP_CODE4"
if [ "$HTTP_CODE4" = "200" ]; then
    echo "   ✅ 成功獲取模型列表"
    echo "   可用模型:"
    echo "$BODY4" | grep -o '"id":"[^"]*"' | head -10 | sed 's/"id":"/     - /g' | sed 's/"//g'
else
    echo "   ❌ 失敗"
    echo "   錯誤：$(echo "$BODY4" | grep -o '"message":"[^"]*"' | head -1)"
fi
echo ""

echo "============================================================"
echo "📊 驗證總結:"
echo ""

# 判斷結果
SUCCESS_COUNT=0
[ "$HTTP_CODE1" = "200" ] && ((SUCCESS_COUNT++))
[ "$HTTP_CODE2" = "200" ] && ((SUCCESS_COUNT++))
[ "$HTTP_CODE3" = "200" ] && ((SUCCESS_COUNT++))
[ "$HTTP_CODE4" = "200" ] && ((SUCCESS_COUNT++))

if [ $SUCCESS_COUNT -gt 0 ]; then
    echo "✅ API 密鑰有效！$SUCCESS_COUNT/4 端點測試成功"
    echo ""
    echo "💡 建議配置:"
    if [ "$HTTP_CODE1" = "200" ]; then
        echo "   推薦使用：DashScope 兼容模式"
        echo "   Base URL: https://dashscope.aliyuncs.com/compatible-mode/v1"
    elif [ "$HTTP_CODE3" = "200" ]; then
        echo "   推薦使用：Coding Plan 專用端點"
        echo "   Base URL: https://coding.dashscope.aliyuncs.com/v1"
    fi
else
    echo "❌ API 密鑰可能無效或未激活"
    echo ""
    echo "🔧 解決步驟:"
    echo "   1. 登錄阿里雲百煉控制台：https://bailian.console.aliyun.com/"
    echo "   2. 確認 API 密鑰是否正確"
    echo "   3. 檢查是否已開通 DashScope/Model Studio 服務"
    echo "   4. 確認 Coding Plan 訂閱狀態"
    echo "   5. 如需新密鑰，在控制台重新生成"
fi

echo ""
echo "============================================================"
