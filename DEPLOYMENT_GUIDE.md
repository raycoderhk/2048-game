# 🚀 一鍵部署指南 - Gameworld + Kanban

## ✅ 自動化部署已配置！

GitHub Actions 會自動部署到 Zeabur，當你 push 代碼到 `main` branch。

---

## 📋 步驟 1: 配置 Zeabur Secrets (一次性設置)

### 1.1 獲取 Zeabur API Key

1. 登入 https://zeabur.com
2. 去 Settings → API Keys
3. 創建新 API Key
4. Copy 條 key

---

### 1.2 添加到 GitHub Secrets

1. 去 https://github.com/raycoderhk/2048-game/settings/secrets/actions
2. 添加以下 secrets：

```
ZEABUR_API_KEY = [你嘅 Zeabur API Key]
ZEABUR_GAMEWORLD_PROJECT_ID = [Gameworld Project ID]
ZEABUR_GAMEWORLD_SERVICE_ID = [Gameworld Service ID]
ZEABUR_KANBAN_PROJECT_ID = [Kanban Project ID]
ZEABUR_KANBAN_SERVICE_ID = [Kanban Service ID]
```

**點樣攞 Project/Service ID？**

- 去 Zeabur Dashboard
- 選擇項目
- URL 會顯示：`https://zeabur.com/dashboard/project/[PROJECT_ID]/service/[SERVICE_ID]`

---

## 📋 步驟 2: Zeabur 手動部署 (Alternative)

如果唔想用 GitHub Actions，可以手動部署：

### Gameworld 部署

```bash
# 1. 去 Zeabur Dashboard
# 2. 創建新服務
# 3. 選擇 GitHub repo: raycoderhk/2048-game
# 4. Root Directory: games/2048-game
# 5. Domain: gameworld.zeabur.app
# 6. Deploy!
```

**環境變量：** 無需

---

### Kanban 部署

```bash
# 1. 去 Zeabur Dashboard
# 2. 創建新服務
# 3. 選擇 GitHub repo: raycoderhk/kanban-board
# 4. Root Directory: kanban-zeabur
# 5. Domain: kanban.zeabur.app
# 6. Build Command: npm install
# 7. Start Command: node server.js
# 8. Deploy!
```

**環境變量：**
```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_CALLBACK_URL=/auth/google/callback
SESSION_SECRET=super-secret-random-string
NODE_ENV=production
```

---

## 📋 步驟 3: 配置 Google OAuth

### 3.1 Google Cloud Console

1. 去 https://console.cloud.google.com/
2. 選擇/創建項目
3. 啟用 Google+ API
4. APIs & Services → Credentials
5. Create Credentials → OAuth client ID
6. Application type: Web application

### 3.2 Authorized redirect URIs

```
https://kanban.zeabur.app/auth/google/callback
http://localhost:8080/auth/google/callback
```

### 3.3 記錄 Credentials

```
Client ID: xxxxx.apps.googleusercontent.com
Client Secret: GOCSPX-xxxxx
```

### 3.4 添加到 Zeabur

去 Zeabur Dashboard → Variables:

```bash
GOOGLE_CLIENT_ID=[Client ID]
GOOGLE_CLIENT_SECRET=[Client Secret]
```

---

## 📋 步驟 4: 測試部署

### Gameworld 測試

1. 去 https://gameworld.zeabur.app
2. 檢查所有遊戲卡片顯示
3. 點擊每個遊戲確保正常
4. 檢查 Kanban 卡片連結

**Expected Result:**
- ✅ 首頁正常加載
- ✅ 6 款遊戲顯示
- ✅ Kanban 卡片存在
- ✅ Mobile Responsive 正常

---

### Kanban 測試

1. 去 https://kanban.zeabur.app
2. 檢查 Login Screen 顯示
3. 點擊 "Sign in with Google"
4. 完成 OAuth 流程
5. 檢查 Kanban Board 顯示
6. 檢查「返回遊戲世界」連結

**Expected Result:**
- ✅ Login Screen 顯示
- ✅ Google Login 正常
- ✅ Board 正常加載
- ✅ Cross-link 正常

---

## 🔄 自動部署流程

```
Push to main branch
        ↓
GitHub Actions triggered
        ↓
Build & Deploy to Zeabur
        ↓
Zeabur auto-restarts service
        ↓
Deployment complete!
```

**部署時間：** 約 2-5 分鐘

---

## 📊 部署狀態監控

### GitHub Actions

- 去 https://github.com/raycoderhk/2048-game/actions
- 查看最新 deployment
- 綠色 ✓ = 成功
- 紅色 ✗ = 失敗

### Zeabur

- 去 Zeabur Dashboard
- 查看服務狀態
- 查看 Deployment History
- 查看 Logs

---

## 🐛 故障排除

### 問題 1: GitHub Actions 失敗

**錯誤：** `Error: Unauthorized`

**解決：**
```
1. 檢查 ZEABUR_API_KEY 是否正確
2. 確保 API Key 有足夠權限
3. 重新生成 API Key
```

---

### 問題 2: Zeabur 部署失敗

**錯誤：** `Build failed`

**解決：**
```
1. 檢查 package.json 是否正確
2. 查看 Zeabur build logs
3. 確保 node_modules 已排除
```

---

### 問題 3: OAuth 重定向失敗

**錯誤：** `redirect_uri_mismatch`

**解決：**
```
1. 檢查 Google Cloud Console 的 Authorized redirect URIs
2. 確保包含 https://kanban.zeabur.app/auth/google/callback
3. 檢查 GOOGLE_CALLBACK_URL 環境變量
```

---

### 問題 4: Supabase 連接失敗

**錯誤：** `Failed to load projects`

**解決：**
```
1. 檢查 SUPABASE_URL 格式
2. 確保 SUPABASE_ANON_KEY 正確
3. 檢查 Supabase 表是否已創建
4. 查看 Zeabur logs
```

---

## 📝 部署清單

### Gameworld

- [ ] GitHub repo 已 push
- [ ] Zeabur 服務已創建
- [ ] Domain 已配置 (`gameworld.zeabur.app`)
- [ ] GitHub Actions secrets 已設置
- [ ] 測試所有遊戲正常
- [ ] 測試 Kanban 連結正常

### Kanban

- [ ] GitHub repo 已 push
- [ ] Zeabur 服務已創建
- [ ] Domain 已配置 (`kanban.zeabur.app`)
- [ ] GitHub Actions secrets 已設置
- [ ] Supabase 環境變量已設置
- [ ] Google OAuth 已配置
- [ ] 測試 Login 正常
- [ ] 測試 Board 正常
- [ ] 測試 Gameworld 連結正常

---

## 🎯 快速部署命令

### 手動部署 (如果 Actions 失敗)

```bash
# 1. 確保代碼已 push
cd /home/node/.openclaw/workspace
git push origin main

# 2. 去 Zeabur Dashboard
# 3. 選擇服務
# 4. 撳 "Redeploy"
```

---

## 📊 最終檢查

### 公開訪問

| 應用 | URL | 狀態 |
|------|-----|------|
| **Gameworld** | https://gameworld.zeabur.app | ⏳ Pending |
| **Kanban** | https://kanban.zeabur.app | ⏳ Pending |

### Cross-Links

| 連結 | 來源 → 目標 | 狀態 |
|------|-----------|------|
| **Kanban Card** | Gameworld → Kanban | ✅ Configured |
| **Back Link** | Kanban → Gameworld | ✅ Configured |

---

## 🎉 完成！

部署成功後：

1. **Share Gameworld:** https://gameworld.zeabur.app
2. **Share Kanban:** https://kanban.zeabur.app (需要 Google Login)
3. **測試 Cross-Links:** 確保互相跳轉正常

---

**需要幫助？** 參考 `GAMEWORLD_KANBAN_ARCHITECTURE.md`

**最後更新：** 2026-02-28  
**Version:** 1.0
