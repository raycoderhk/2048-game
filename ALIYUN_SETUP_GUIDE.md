# 阿里雲 API 密鑰設置指南

## ⚠️ 重要提醒 - 必讀！

**🚨 獲取 API Key 的正確位置：**

| 獲取位置 | 是否正確 | 收費方式 |
|---------|---------|---------|
| Coding Plan 訂閱專屬頁面 | ✅ 正確 | 包月制（已付費） |
| 普通 API-KEY 管理頁面 | ❌ 錯誤 | 按流量額外收費 |
| DashScope 通用控制台 | ❌ 錯誤 | 按流量額外收費 |

**使用錯誤位置的 API Key = 白付錢！**

即使你訂閱了 Coding Plan，如果用普通 API Key，系統會**額外按 token 計費**！

**正確做法：**
1. 訂閱 Coding Plan 套餐
2. 在**訂閱詳情頁**獲取專屬 API Key
3. 將專屬 Key 設置到環境變量

---

## 🔍 問題診斷

當前 API 密鑰格式：`sk-sp-8eec812bc72d47c3866d388cef6372f8`
- ✅ 格式正確（sk-sp-開頭）
- ❌ 但所有端點都返回 401 錯誤

## 📋 解決步驟

### 步驟 1：登錄阿里雲百煉控制台

訪問：https://bailian.console.aliyun.com/

### 步驟 2：確認服務開通

1. 在控制台首頁，確認已開通 **Model Studio (百煉)** 服務
2. 檢查是否已訂閱 **Coding Plan** 套餐（Lite ¥7.9 或 Pro ¥39.9）

### 步驟 3：獲取 Coding Plan 專屬 API 密鑰 ⚠️ 重要！

**🚨 必須在訂閱套餐頁面獲取專屬 API Key！**

**重要提醒：**
- ❌ **不要**在普通 API-KEY 管理頁面獲取
- ❌ **不要**使用 DashScope 通用 API Key
- ✅ **必須**在 Coding Plan 訂閱頁面獲取專屬 Key
- ⚠️ 使用普通 API Key 會**按流量額外收費**，失去包月優惠！

**正確獲取步驟：**

1. 進入 Coding Plan 訂閱頁面
   - 百煉控制台 → Coding Plan → 我的訂閱

2. 在訂閱詳情頁面找到「API 密鑰」或「專屬 Key」

3. 點擊「生成專屬 API Key」或「查看密鑰」

4. 複製專屬密鑰（格式：`sk-coding-xxxxxxxx` 或類似）

5. **立即保存** - 密鑰通常只显示一次！

### 步驟 4：更新環境變量

獲取新密鑰後，更新環境變量：

```bash
# 替換 YOUR_NEW_API_KEY 為實際密鑰
export ALIYUN_API_KEY="sk-yournewapikey123456789"
```

### 步驟 5：驗證新密鑰

運行驗證腳本：
```bash
./verify_aliyun_key.sh
```

## 🎯 Coding Plan 套餐選擇

### Lite 基礎版（¥7.9 首月）
- 1.8 萬次請求/月
- 適合：新手、轻度用戶、個人學習

### Pro 高級版（¥39.9 首月）
- 9 萬次請求/月
- 適合：全職開發者、重度用戶、複雜 Agent 任務

## 📝 可用模型

訂閱 Coding Plan 後可使用的模型：

**Qwen 系列:**
- `qwen-plus` - 平衡性能和速度（推薦）
- `qwen-turbo` - 快速響應
- `qwen-max` - 最強推理能力
- `qwen-coder-plus` - 編碼專用
- `qwen2.5-coder-32b-instruct` - 開源編碼模型

**其他模型:**
- `glm-4` - 智譜 GLM
- `kimi-k2` - Moonshot Kimi
- `minimax-m2` - MiniMax

## 🔗 有用鏈接

- 百煉控制台：https://bailian.console.aliyun.com/
- DashScope 控制台：https://dashscope.console.aliyun.com/
- API 文檔：https://help.aliyun.com/zh/model-studio/
- 錯誤碼說明：https://help.aliyun.com/zh/model-studio/error-code
- Coding Plan 詳情：https://help.aliyun.com/zh/model-studio/coding-plan

## ⚠️ 常見問題

**Q: 為什麼顯示 "Incorrect API key provided"?**
A: 可能原因：
1. API 密鑰複製錯誤（多空格或少字符）
2. 密鑰已過期或被撤銷
3. 密鑰屬於其他阿里雲服務（非 Model Studio）

**Q: 為什麼顯示 "model not supported"?**
A: 可能原因：
1. 該模型需要額外訂閱
2. 模型名稱不正確
3. 所在區域不支持該模型

**Q: Coding Plan 和普通按量計費有什麼區別？**
A: Coding Plan 是包月制，在額度內不限請求次數；按量計費是按 token 收費，用多少付多少。

## 📞 需要幫助？

如果以上步驟無法解決問題：
1. 檢查阿里雲賬戶是否已完成實名認證
2. 確認賬戶餘額是否充足
3. 聯繫阿里雲客服：https://workorder.console.aliyun.com/

---

## ✅ 快速檢查清單

設置前請確認：

- [ ] 已訂閱 Coding Plan 套餐（Lite 或 Pro）
- [ ] 從**訂閱專屬頁面**獲取 API Key（不是普通 API Key）
- [ ] API Key 格式正確（通常以 `sk-` 開頭）
- [ ] 已將 Key 設置到環境變量 `ALIYUN_API_KEY`
- [ ] 已重啟 OpenClaw Gateway 使配置生效
- [ ] 已運行驗證腳本確認連接成功

**完成所有步驟後，你就可以享受包月無限使用，不用擔心 token 費用！** 🎉
