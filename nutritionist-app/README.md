# 🥗 營養師 App

使用 AI 識別食物圖片並提供營養分析建議。

---

## 🚀 功能特點

- 📸 **食物圖片識別** - 使用 OpenRouter MiniMax-01 (Vision)
- 📊 **營養成分分析** - 卡路里、蛋白質、碳水化合物、脂肪、纖維
- 💡 **健康建議** - 專業營養師建議
- 📝 **報告生成** - Markdown 格式報告
- 🔄 **雙模型協作** - MiniMax-01 識別 + Qwen3.5-Plus 分析

---

## 🛠️ 技術堆棧

| 組件 | 技術 | 平台 |
|------|------|------|
| **圖片識別** | MiniMax-01 (Vision) | OpenRouter |
| **營養分析** | Qwen3.5-Plus | Aliyun Coding Plan |
| **備用方案** | Qwen-VL / SigLIP | Aliyun / HF |

**架構優勢：**
- ✅ MiniMax-01 免費額度 - 適合測試
- ✅ Qwen3.5-Plus 中文優化 - 營養分析準確
- ✅ 雙模型協作 - 發揮各自優勢

---

## 💻 使用方法

### 快速開始 (OpenRouter 版)

```bash
cd /home/node/.openclaw/workspace/nutritionist-app

# 設置環境變量
export OPENROUTER_API_KEY="sk-or-..."
export ALIYUN_API_KEY="sk-..."

# 分析食物圖片
python3 nutritionist_openrouter.py food.jpg
```

### 傳統方法 (Hugging Face 版)

```bash
export HF_API_KEY="your-hf-token"
export ALIYUN_API_KEY="your-aliyun-key"

python3 nutritionist_app.py food.jpg
```

### Qwen-VL 單一 API 版

```bash
export ALIYUN_API_KEY="your-aliyun-key"

python3 nutritionist_qwen_vl.py food.jpg
```

---

## 🔧 配置

### 環境變量 (OpenRouter 版)

```bash
# OpenRouter API Key (MiniMax-01 for Vision)
export OPENROUTER_API_KEY="sk-or-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Aliyun API Key (Qwen3.5-Plus for Nutrition)
export ALIYUN_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

### 環境變量 (Hugging Face 版)

```bash
# Hugging Face Token
export HF_API_KEY="your-hf-token-here"

# Aliyun API Key
export ALIYUN_API_KEY="your-aliyun-key-here"
```

---

## 📁 文件結構

```
nutritionist-app/
├── nutritionist_openrouter.py  # 【推薦】OpenRouter + Aliyun 雙模型
├── nutritionist_qwen_vl.py     # Aliyun Qwen-VL 單一 API
├── nutritionist_app.py         # Hugging Face + Aliyun (傳統版)
├── index.html                  # Web 界面
├── server.py                   # Web Server
├── README.md                   # 使用說明
├── OPENROUTER_SETUP.md         # OpenRouter 設定指南
├── DEPLOYMENT.md               # 部署指南
└── .env.example                # 環境變量範例
```

---

## 🚀 部署

### Zeabur 部署

1. Push 代碼到 GitHub
2. Zeabur 連接 Repo
3. 設定環境變數：
   - `OPENROUTER_API_KEY`
   - `ALIYUN_API_KEY`
4. 自動部署

詳見 [DEPLOYMENT.md](DEPLOYMENT.md)

### OpenRouter 設定

詳見 [OPENROUTER_SETUP.md](OPENROUTER_SETUP.md)

---

## 📊 成本估算

| 服務 | 計劃 | 成本 | 額度 |
|------|------|------|------|
| **OpenRouter** | MiniMax-01 | 免費 | 測試額度 |
| **Aliyun** | Coding Plan | CNY 7.9/月 | 1M tokens |

**總成本：** CNY 7.9/月 (約 HKD 9/月)

---

## 🧪 測試

```bash
# 測試 OpenRouter Vision
python3 nutritionist_openrouter.py test_food.jpg

# 測試 Qwen-VL
python3 nutritionist_qwen_vl.py test_food.jpg

# 測試 Hugging Face
python3 nutritionist_app.py test_food.jpg
```

---

## 🐛 故障排除

### OpenRouter 401 錯誤
- 檢查 API Key 是否正確
- 確認無多餘空格

### JSON 解析失敗
- 模型可能返回非 JSON 格式
- 檢查 prompt 是否清晰

### Token 不足
- 檢查 Aliyun Coding Plan 訂閱
- 查看用量：https://dashscope.console.aliyun.com/usage

---

## 📚 參考連結

- **OpenRouter 設定：** [OPENROUTER_SETUP.md](OPENROUTER_SETUP.md)
- **部署指南：** [DEPLOYMENT.md](DEPLOYMENT.md)
- **OpenRouter:** https://openrouter.ai/
- **Aliyun 百煉:** https://dashscope.console.aliyun.com/

---

**🌸 祝您健康！**
