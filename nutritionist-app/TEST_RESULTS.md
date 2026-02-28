# 🧪 Qwen-VL API 測試結果

**測試日期：** 2026-03-01  
**測試圖片：** `/home/node/.openclaw/media/inbound/a034886a-6552-48ea-9574-57ebfb48a46d.jpg`

---

## ❌ 測試結果：失敗

**錯誤代碼：** HTTP 401 - Invalid API Key

**錯誤訊息：**
```json
{
  "error": {
    "message": "Incorrect API key provided. For details, see: https://help.aliyun.com/zh/model-studio/error-code#apikey-error",
    "type": "invalid_request_error",
    "code": "invalid_api_key"
  },
  "request_id": "8d97a503-e040-9b33-bcb1-1bfaf353ae9d"
}
```

---

## 🔍 問題分析

### 我哋用緊嘅 API Key
```
sk-sp-8eec812bc72d47c3866d388cef6372f8
```
- **來源：** 環境變數 `ALIYUN_API_KEY`
- **用途：** 阿里雲 Coding Plan（¥39.9/月）
- **Base URL:** `https://coding.dashscope.aliyuncs.com/v1`
- **工作正常：** ✅ 文本模型（Qwen-Plus, Qwen-Coder）

### Qwen-VL 需要嘅 API Key
- **平台：** 阿里雲百煉（Model Studio）
- **Base URL:** `https://dashscope.aliyuncs.com/compatible-mode/v1`
- **計費：** 按 Token 計費（唔包喺 Coding Plan 內）

---

## ⚠️ 關鍵發現

**阿里雲有兩個唔同嘅平台：**

| 平台 | Coding Plan | 百煉 (Model Studio) |
|------|-------------|---------------------|
| **用途** | 文本生成/代碼 | 多模態（圖片、音頻等） |
| **計費** | ¥39.9/月 包月 | 按 Token 計費 |
| **API Key** | `sk-sp-xxx` | `sk-xxx` (可能唔同) |
| **Base URL** | `coding.dashscope.aliyuncs.com` | `dashscope.aliyuncs.com` |
| **我哋現狀** | ✅ 用緊 | ❌ 未開通 |

---

## 🎯 解決方案

### 方案 A：開通百煉服務（推薦）

**步驟：**

1. **登入阿里雲百煉控制台**
   - 網址：https://bailian.console.aliyun.com/

2. **開通 Qwen-VL 模型**
   - 去「模型管理」
   - 找到 `qwen-vl-plus`
   - 點擊「開通」

3. **獲取新 API Key**
   - 去「API Key 管理」
   - 創建一個新 Key（或者用現有）
   - 複製 Key

4. **測試新 Key**
   - 用新 Key 運行測試腳本
   - Base URL 用：`https://dashscope.aliyuncs.com/compatible-mode/v1`

**優點：**
- ✅ 正式支援 Qwen-VL
- ✅ 按量付費，成本低
- ✅ 同 Coding Plan 分開計費，清晰

**缺點：**
- ⚠️ 需要額外註冊/開通

---

### 方案 B：聯絡阿里雲客服

**聯絡方法：**

1. **在線工單：**
   - 網址：https://workorder.console.aliyun.com/
   - 分類：產品咨詢 > 百煉 > 模型使用

2. **電話：**
   - 香港：+852 3018 5680
   - 內地：95187

3. **在線客服：**
   - 阿里雲官網右下角「在線客服」

**詢問內容：**
```
我而家用緊 Coding Plan (¥39.9/月)，想問：
1. 可唔可以用同一個 API Key 調用 Qwen-VL 模型？
2. 如果唔得，點樣開通百煉服務？
3. 開通後計費係點？
```

---

### 方案 C：用替代 API

如果阿里雲搞唔掂，可以考慮：

| API | 供應商 | 價格 | 備註 |
|-----|-------|------|------|
| **Google Vision** | Google | $1.5/1000 次 | 需翻牆 |
| **Azure Computer Vision** | Microsoft | $1/1000 次 | 需信用卡 |
| **Claude 3** | Anthropic | $3/1M tokens | 支援圖片 |
| **GPT-4V** | OpenAI | $10/1M tokens | 最貴但最強 |

---

## 📝 下一步行動

### 即時行動（今日）

1. **登入阿里雲百煉控制台**
   - https://bailian.console.aliyun.com/
   - 用同一個阿里雲賬戶

2. **檢查是否已開通 Qwen-VL**
   - 去「模型管理」
   - 睇吓有無 `qwen-vl-plus` 或 `qwen-vl-max`

3. **如果未開通：**
   - 點擊「開通」
   - 同意服務條款
   - 綁定支付方式（按量付費）

4. **獲取 API Key**
   - 去「API Key 管理」
   - 創建或複製現有 Key

5. **重新測試**
   - 更新測試腳本中的 API Key
   - 運行：`python3 test_with_env.py <圖片>`

### 如果搞唔掂

- 📞 聯絡阿里雲客服
- 📧 發送郵件到：bailian-support@list.alibaba-inc.com
- 💬 喺 Discord 度話我知，我幫你跟進

---

## 💰 預算估算

**假設開通成功：**

| 項目 | 成本 |
|------|------|
| Coding Plan (文本) | ¥39.9/月 |
| Qwen-VL (圖片分析) | ¥0.05/張 |
| 每日 3 餐 × 30 日 | ¥4.5/月 |
| **總計** | **約 ¥45/月** (約 $50 HKD) |

**好便宜！值得開發！** 💪

---

## 🚀 結論

**現狀：**
- ❌ Coding Plan API Key 唔支援 Qwen-VL
- ✅ 阿里雲百煉有 Qwen-VL，但要額外開通

**下一步：**
1. 開通百煉服務
2. 獲取新 API Key
3. 重新測試
4. 開始開發 MVP

**需要幫忙？** 隨時喺 Discord 度搵我！🤖

---

*Last updated: 2026-03-01 10:00 UTC*
