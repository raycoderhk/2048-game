# 🍎 Qwen-VL API 測試指南

## 📋 步驟

### 1️⃣ 準備測試圖片

搵一張食物相，例如：
- 你頭先 post 嗰兩張相
- 或者任何一餐飯嘅相

**將圖片放到：** `/home/node/.openclaw/workspace/nutritionist-app/`

**命名為：** `test_food.jpg` （或者 `.png`）

---

### 2️⃣ 運行測試腳本

```bash
cd /home/node/.openclaw/workspace/nutritionist-app
python3 test_qwen_vl.py
```

**或者指定圖片路徑：**
```bash
python3 test_qwen_vl.py /path/to/your/food.jpg
```

---

### 3️⃣ 測試內容

腳本會自動運行 **3 個測試**：

#### ✅ 測試 1: 純文本 API
- 驗證你而家嘅 API Key 係咪 work
- 用 `qwen-plus` 模型（包喺 ¥40/月 內）
- **預期結果：** 通過 ✅

#### ✅ 測試 2: 基本圖片識別
- 用 `qwen-vl-plus` 模型
- 問：「這張圖片中有什麼食物？」
- **預期結果：** 
  - 通過 ✅ = 支援圖片上傳！
  - 失敗 ❌ = 需要額外開通或升級

#### ✅ 測試 3: 營養成份分析
- 用 `qwen-vl-plus` 模型
- 問：「請提供營養成份（卡路里、蛋白質、脂肪等）」
- **預期結果：** 睇吓 AI 識唔識分析營養

---

### 4️⃣ 睇測試結果

**如果全部通過：**
```
🎉 恭喜！阿里雲 Qwen-VL API 完全支援圖片上傳！
   你可以開始開發營養師 App 了！🚀
```

**如果圖片測試失敗：**
```
⚠️  純文本 OK，但 Qwen-VL 失敗。
   可能原因:
   1. Qwen-VL 模型需要額外開通
   2. API Key 權限不足
   3. 需要聯絡阿里雲客服
```

---

## 💰 費用提示

**Qwen-VL 按 Token 計費（唔包喺 ¥40/月 內）：**

| 測試 | 估計成本 |
|------|---------|
| 每次圖片分析 | ~¥0.05 |
| 3 次測試總計 | ~¥0.15 |

**好便宜！放心試！** 😄

---

## 🔧 如果失敗點算？

### 情況 1: API Key 錯誤
```
❌ 狀態碼：401
錯誤訊息：Invalid API Key
```
**解決方法：** 
- 去阿里雲控制台重新生成 API Key
- 網址：https://bailian.console.aliyun.com/

---

### 情況 2: Qwen-VL 未開通
```
❌ 狀態碼：403
錯誤訊息：Model not accessible
```
**解決方法：**
1. 登入阿里雲百煉控制台
2. 去「模型管理」
3. 開通 `qwen-vl-plus` 模型
4. 或者聯絡客服：https://workorder.console.aliyun.com/

---

### 情況 3: 圖片格式錯誤
```
❌ 發生錯誤：Invalid image format
```
**解決方法：**
- 用 JPG 或 PNG 格式
- 圖片大小 < 10MB
- 解析度建議：800x600 到 2048x2048

---

## 📞 阿里雲客服聯絡

如果搞唔掂，可以聯絡阿里雲：

**在線客服：**
- 網址：https://workorder.console.aliyun.com/
- 工作時間：9:00-21:00（北京時間）

**電話：**
- 香港：+852 3018 5680
- 內地：95187

**英文/廣東話都得！**

---

## 🎯 下一步

**測試通過後：**

1. ✅ 確認 Qwen-VL 可用
2. 📝 記錄實際 Token 使用量
3. 💰 計算每月預算
4. 🚀 開始開發 MVP！

**測試失敗後：**

1. ❓ 聯絡阿里雲確認
2. 🔄 考慮其他 API（Google Vision, Azure）
3. 📊 更新 Kanban 任務狀態

---

**準備好未？運行個測試啦！** 🏃‍♂️

```bash
cd /home/node/.openclaw/workspace/nutritionist-app
python3 test_qwen_vl.py
```
