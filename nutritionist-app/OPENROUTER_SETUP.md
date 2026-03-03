# 🔑 OpenRouter + Aliyun 設定指南

## 📋 概述

營養師 App 使用**雙模型協作**架構：

| 任務 | 模型 | 平台 | 成本 |
|------|------|------|------|
| **食物識別** | MiniMax-01 | OpenRouter | 免費額度 |
| **營養分析** | Qwen3.5-Plus | Aliyun | Coding Plan 內 |

---

## 🚀 步驟 1: 獲取 OpenRouter API Key

### 1.1 註冊 OpenRouter

1. 前往 https://openrouter.ai/
2. 點擊 "Sign In" (可用 Google/GitHub 登入)
3. 完成註冊

### 1.2 創建 API Key

1. 登入後前往 https://openrouter.ai/keys
2. 點擊 "Create Key"
3. 輸入名稱 (例如：`Nutritionist App`)
4. 複製 API Key (格式：`sk-or-...`)

### 1.3 免費額度

**MiniMax-01** 在 OpenRouter 提供：
- ✅ **免費額度** - 適合測試和個人使用
- ✅ **Vision 支援** - 圖像識別能力強
- ✅ **中文優化** - 對中文食物識別準確

**查看用量：** https://openrouter.ai/activity

---

## 🚀 步驟 2: 獲取 Aliyun API Key

### 2.1 登入阿里雲百煉

1. 前往 https://dashscope.console.aliyun.com/
2. 使用阿里雲帳號登入

### 2.2 創建 API Key

1. 前往 https://dashscope.console.aliyun.com/apiKey
2. 點擊 "創建新的 API-KEY"
3. 複製 API Key (格式：`sk-...`)

### 2.3 Coding Plan 訂閱

**確認你有 Coding Plan：**
- 價格：CNY 7.9/月
- 額度：1M tokens
- 支援模型：Qwen3.5-Plus, GLM-5, MiniMax M2.5, Kimi K2.5

**查看用量：** https://dashscope.console.aliyun.com/usage

---

## 🚀 步驟 3: 設定環境變數

### 3.1 本地測試

```bash
cd /home/node/.openclaw/workspace/nutritionist-app

# 設定環境變數
export OPENROUTER_API_KEY='sk-or-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
export ALIYUN_API_KEY='sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

# 測試
python3 nutritionist_openrouter.py test_food.jpg
```

### 3.2 Zeabur 部署

1. 前往 https://zeabur.com
2. 選擇你的 Nutritionist App 項目
3. 進入 **Settings → Environment Variables**
4. 添加以下變數：

| Variable | Value |
|----------|-------|
| `OPENROUTER_API_KEY` | `sk-or-...` |
| `ALIYUN_API_KEY` | `sk-...` |

5. 點擊 **Redeploy** 重新部署

---

## 🧪 測試流程

### 測試 1: OpenRouter Vision

```bash
# 測試圖片識別
python3 -c "
import urllib.request
import json
import base64

API_KEY = 'sk-or-...'
IMAGE_PATH = 'test_food.jpg'

with open(IMAGE_PATH, 'rb') as f:
    image_data = base64.b64encode(f.read()).decode('utf-8')

payload = {
    'model': 'minimax/minimax-01',
    'messages': [{
        'role': 'user',
        'content': [
            {'type': 'image_url', 'image_url': {'url': f'data:image/jpeg;base64,{image_data}'}},
            {'type': 'text', 'text': '這是什麼食物？'}
        ]
    }]
}

req = urllib.request.Request(
    'https://openrouter.ai/api/v1/chat/completions',
    data=json.dumps(payload).encode('utf-8'),
    headers={'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'},
    method='POST'
)

with urllib.request.urlopen(req) as response:
    result = json.loads(response.read().decode('utf-8'))
    print(result['choices'][0]['message']['content'])
"
```

### 測試 2: Aliyun Nutrition

```bash
# 測試營養分析
python3 -c "
import urllib.request
import json

API_KEY = 'sk-...'

payload = {
    'model': 'qwen3.5-plus',
    'messages': [
        {'role': 'system', 'content': '你是一位專業營養師。'},
        {'role': 'user', 'content': '分析白飯的營養成分'}
    ]
}

req = urllib.request.Request(
    'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions',
    data=json.dumps(payload).encode('utf-8'),
    headers={'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'},
    method='POST'
)

with urllib.request.urlopen(req) as response:
    result = json.loads(response.read().decode('utf-8'))
    print(result['choices'][0]['message']['content'])
"
```

### 測試 3: 完整流程

```bash
# 用真實食物圖片測試
python3 nutritionist_openrouter.py龙虾.jpg
```

---

## 📊 成本估算

### OpenRouter (MiniMax-01)

| 用量 | 成本 |
|------|------|
| 測試階段 | 免費 |
| 每日 10 次 | 免費額度內 |
| 每日 100+ 次 | 約 $0.01-0.05/次 |

### Aliyun (Qwen3.5-Plus)

| 用量 | 成本 |
|------|------|
| Coding Plan | CNY 7.9/月 |
| 額度 | 1M tokens |
| 每次分析 | ~500-1000 tokens |
| 可用次數 | ~1000-2000 次/月 |

**總成本：** CNY 7.9/月 (主要係 Aliyun 固定費用)

---

## 🐛 故障排除

### 問題 1: OpenRouter 401 錯誤

```
HTTP 401: Unauthorized
```

**解決：**
- 檢查 API Key 是否正確
- 確認無多餘空格
- 重新創建 API Key

### 問題 2: MiniMax-01 無回應

```
Timeout error
```

**解決：**
- 增加 timeout (預設 60 秒)
- 檢查圖片大小 (建議 < 5MB)
- 壓縮圖片後再上傳

### 問題 3: JSON 解析失敗

```
JSON 解析失敗
```

**解決：**
- 模型可能返回非 JSON 格式
- 檢查 prompt 是否清晰要求 JSON
- 手動提取 JSON 部分

### 問題 4: Aliyun Token 不足

```
Insufficient balance
```

**解決：**
- 檢查 Coding Plan 訂閱狀態
- 續訂或升級計劃
- 查看用量：https://dashscope.console.aliyun.com/usage

---

## 🔄 備用方案

如果 OpenRouter 唔 Work，可以轉用：

### 備用 1: Aliyun Qwen-VL

```python
# 使用 nutritionist_qwen_vl.py
# 單一 Aliyun API 搞掂識別 + 分析
python3 nutritionist_qwen_vl.py test_food.jpg
```

### 備用 2: Hugging Face SigLIP

```python
# 使用 nutritionist_app.py
# 免費但識別能力較弱
python3 nutritionist_app.py test_food.jpg
```

---

## 📚 參考連結

- **OpenRouter:** https://openrouter.ai/
- **MiniMax 文檔:** https://platform.minimaxi.com/
- **Aliyun 百煉:** https://help.aliyun.com/zh/dashscope/
- **Qwen3.5-Plus:** https://help.aliyun.com/zh/dashscope/model-square/

---

## ✅ 檢查清單

- [ ] OpenRouter 帳號註冊完成
- [ ] OpenRouter API Key 獲取
- [ ] Aliyun API Key 獲取
- [ ] 環境變數設定完成
- [ ] 本地測試成功
- [ ] Zeabur 環境變數設定
- [ ] Zeabur 重新部署
- [ ] 真實圖片測試成功

---

**設定完成後，你就可以用 MiniMax-01 識別龍蝦等複雜食物圖片！** 🦞
