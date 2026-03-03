# 🚀 營養師 App - Zeabur 部署指南

## 📋 概述

**版本：** 2.0 - OpenRouter Vision  
**模型：** MiniMax-01 (OpenRouter)  
**特點：** 食物識別 + 營養分析 單一 API 搞掂

---

## 🎯 部署步驟

### 1️⃣ 準備 GitHub Repo

代碼已 Push 到：
- **Branch:** `openrouter-vision`
- **URL:** https://github.com/raycoderhk/kanban-board/tree/openrouter-vision/nutritionist-app

---

### 2️⃣ Zeabur 部署

#### 方法 A: 直接部署

1. **前往 Zeabur:** https://zeabur.com
2. **登入** (GitHub 帳號)
3. **新建項目** → "Deploy from GitHub"
4. **選擇 Repo:** `kanban-board`
5. **選擇 Branch:** `openrouter-vision`
6. **設置 Root Directory:** `nutritionist-app`

#### 方法 B: 一鍵部署

點擊以下按鈕直接部署：

[![Deploy to Zeabur](https://zeabur.com/button.svg)](https://zeabur.com)

---

### 3️⃣ 設置環境變數

**喺 Zeabur Dashboard:**

1. 進入項目 → **Settings** → **Environment Variables**
2. 添加以下變數：

| Variable | Value | 說明 |
|----------|-------|------|
| `OPENROUTER_API_KEY` | `sk-or-v1-...` | OpenRouter API Key |
| `PORT` | `8080` | 服務端口 (Zeabur 自動設置) |

**獲取 OpenRouter API Key:**
- 前往：https://openrouter.ai/keys
- 登入 → Create Key → 複製

---

### 4️⃣ 重新部署

1. 進入項目 → **Deployments**
2. 點擊 **Redeploy**
3. 等待 2-3 分鐘

---

### 5️⃣ 測試

**訪問你的應用：**
```
https://nutritionist-app-xxxx.zeabur.app
```

**健康檢查：**
```
https://nutritionist-app-xxxx.zeabur.app/health
```

**預期結果：**
```json
{
  "status": "ok",
  "openrouter_configured": true,
  "model": "minimax/minimax-01",
  "version": "2.0 - OpenRouter Vision"
}
```

---

## 🧪 本地測試

### 安裝依賴

```bash
cd nutritionist-app

# 安裝 Flask
pip3 install flask gunicorn
```

### 設置環境變數

```bash
# 方法 1: 使用 .env 文件 (自動載入)
cat > .env << EOF
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
EOF

# 方法 2: 直接 export
export OPENROUTER_API_KEY='sk-or-v1-...'
```

### 啟動服務

```bash
# 開發模式
python3 server.py

# 生產模式 (gunicorn)
gunicorn -w 4 -b 0.0.0.0:8080 server:app
```

### 測試 API

```bash
# 健康檢查
curl http://localhost:8080/health

# 測試分析 (需要圖片)
curl -X POST http://localhost:8080/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"image": "data:image/jpeg;base64,..."}'
```

---

## 📊 成本估算

| 服務 | 計劃 | 成本 | 額度 |
|------|------|------|------|
| **OpenRouter** | MiniMax-01 | 免費 | 測試額度 |
| **Zeabur** | Hobby | $0 | 500 小時/月 |

**總成本：** $0/月 (免費額度內)

---

## 🐛 故障排除

### 問題 1: 401 Unauthorized

```json
{"error": "OPENROUTER_API_KEY 未設置"}
```

**解決：**
- 檢查 Zeabur 環境變數是否正確
- 確認 API Key 無多餘空格
- 重新部署

### 問題 2: 402 Payment Required

```json
{"error": "This request requires more credits"}
```

**解決：**
- OpenRouter 免費額度用盡
- 前往 https://openrouter.ai/settings/credits 充值
- 或減少 `max_tokens` 用量

### 問題 3: JSON 解析失敗

**解決：**
- 模型可能返回非 JSON 格式
- 檢查 prompt 是否清晰要求 JSON
- 重試一次

### 問題 4: 超時 (Timeout)

**解決：**
- 圖片太大 (建議 < 5MB)
- 壓縮圖片後再上傳
- 增加 timeout 設置

---

## 📁 文件結構

```
nutritionist-app/
├── index.html                  # Web UI (前端)
├── server.py                   # Flask Server (後端)
├── requirements.txt            # Python 依賴
├── .env                        # 環境變數 (本地用)
├── .env.example                # 環境變數範例
├── nutritionist_openrouter_only.py  # CLI 版本
├── test_openrouter.py          # 測試腳本
└── DEPLOYMENT.md               # 部署指南 (本文件)
```

---

## 🔗 相關連結

- **OpenRouter:** https://openrouter.ai/
- **MiniMax 文檔:** https://platform.minimaxi.com/
- **Zeabur 文檔:** https://zeabur.com/docs/
- **GitHub Repo:** https://github.com/raycoderhk/kanban-board

---

## ✅ 檢查清單

部署前確認：

- [ ] OpenRouter 帳號已註冊
- [ ] API Key 已獲取
- [ ] Zeabur 帳號已登入
- [ ] GitHub Repo 已 Push
- [ ] 環境變數已設置
- [ ] 本地測試成功
- [ ] 健康檢查通過

---

## 🎉 完成！

部署成功後，你就可以：

1. **上傳食物圖片** 📸
2. **AI 自動識別** 🤖
3. **獲取營養分析** 📊
4. **查看健康建議** 💡

**享受健康飲食！** 🥗

---

**版本：** 2.0 - OpenRouter Vision  
**更新日期：** 2026-03-03  
**作者：** Jarvis + Raymond
