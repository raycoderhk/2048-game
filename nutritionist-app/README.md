# 🥗 營養師 App

使用 AI 識別食物圖片並提供營養分析建議。

---

## 🚀 功能特點

- 📸 **食物圖片識別** - 使用 Hugging Face AI 模型
- 📊 **營養成分分析** - 卡路里、蛋白質、碳水化合物、脂肪、纖維
- 💡 **健康建議** - 專業營養師建議
- 📝 **報告生成** - Markdown 格式報告

---

## 🛠️ 技術堆棧

| 組件 | 技術 |
|------|------|
| **圖片識別** | Hugging Face Inference API |
| **模型** | google/siglip-so400m-patch14-384 |
| **營養分析** | Aliyun Qwen3.5-plus |
| **HF Token** | 從環境變量讀取 |

---

## 💻 使用方法

```bash
cd /home/node/.openclaw/workspace/nutritionist-app

# 設置環境變量
export HF_API_KEY="your-hf-token"
export ALIYUN_API_KEY="your-aliyun-key"

# 分析食物圖片
python3 nutritionist_app.py food.jpg
```

---

## 🔧 配置

### 環境變量

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
├── nutritionist_app.py      # 主程式
├── index.html               # Web 界面
├── README.md                # 使用說明
└── server.py                # Web Server
```

---

## 🚀 部署

詳見 [DEPLOYMENT.md](DEPLOYMENT.md)

---

**🌸 祝您健康！**
