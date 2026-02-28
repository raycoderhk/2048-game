# 🏗️ Gameworld + Kanban Board - 架構部署指南

## 📊 架構概覽

```
┌─────────────────────────────────────────────────────────┐
│                   Zeabur Deployment                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────────────┐    ┌──────────────────────┐  │
│  │   Gameworld (Public) │    │  Kanban (Protected)  │  │
│  │   gameworld.zeabur.app│    │ kanban.zeabur.app    │  │
│  │                      │    │                      │  │
│  │  - 6 款小遊戲         │    │  - Google OAuth      │  │
│  │  - 無需認證          │    │  - 項目管理          │  │
│  │  - 靜態 HTML          │    │  - Supabase 後端     │  │
│  │                      │    │                      │  │
│  │  / (首頁)            │    │  / (需要登入)        │  │
│  │  /2048/              │    │  /api/*              │  │
│  │  /snake/             │    │  /auth/google        │  │
│  │  /tictactoe/         │    │                      │  │
│  │  /breakout/          │    │                      │  │
│  │  /memory/            │    │                      │  │
│  └──────────────────────┘    └──────────────────────┘  │
│            │                            │               │
│            └──────────┬─────────────────┘               │
│                       │                                  │
│              互相連結 (Cross-Links)                      │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 推薦方案：兩個獨立部署

### 方案 A: 獨立部署 (推薦) ⭐

**優點：**
- ✅ 清晰分離 (遊戲 vs 工具)
- ✅ 各自獨立擴展
- ✅ 唔同嘅安全要求
- ✅ 更容易維護
- ✅ OAuth 不會影響遊戲

**部署：**

| 應用 | Domain | 認證 | 技術棧 |
|------|--------|------|--------|
| **Gameworld** | `gameworld.zeabur.app` | 無需 | 靜態 HTML |
| **Kanban** | `kanban.zeabur.app` | Google OAuth | Express + Supabase |

**互相連結：**

**Gameworld → Kanban:**
```html
<a href="https://kanban.zeabur.app" class="game-card">
    <div class="game-icon">📊</div>
    <h2 class="game-name">Kanban 看板</h2>
</a>
```

**Kanban → Gameworld:**
```html
<a href="https://gameworld.zeabur.app" class="back-link">
    🏠 返回遊戲世界
</a>
```

---

### 方案 B: 單一部署 (Subdirectory)

**優點：**
- ✅ 單一 Domain
- ✅ 統一管理

**缺點：**
- ❌ 複雜嘅路由配置
- ❌ OAuth 可能影響遊戲
- ❌ 靜態 + 動態混合

**部署：**

```
gameworld.zeabur.app/
├── /                     # 遊戲首頁 (公開)
├── /2048/                # 2048 遊戲 (公開)
├── /snake/               # 貪食蛇 (公開)
├── /tictactoe/           # 井字過三關 (公開)
├── /breakout/            # 打磚塊 (公開)
├── /memory/              # 記憶配對 (公開)
└── /kanban/              # Kanban (需要 OAuth)
    ├── /                 # Kanban 首頁 ( protected)
    ├── /api/*            # API routes
    └── /auth/google      # OAuth routes
```

---

## 🚀 部署步驟 (方案 A - 推薦)

### 步驟 1: Gameworld 部署

**GitHub Repo:** `raycoderhk/2048-game`

**Zeabur 配置：**
```
Service Name: gameworld
Domain: gameworld.zeabur.app
Build Command: (留空)
Output Directory: games/2048-game
Port: 8080
```

**環境變量：** 無需

---

### 步驟 2: Kanban 部署

**GitHub Repo:** `raycoderhk/kanban-board` (需要創建/更新)

**Zeabur 配置：**
```
Service Name: kanban-board
Domain: kanban.zeabur.app
Build Command: npm install
Output Directory: (留空)
Port: 8080
```

**環境變量：**
```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_CALLBACK_URL=https://kanban.zeabur.app/auth/google/callback
SESSION_SECRET=your-random-secret-key
```

---

## 🔗 互相連結配置

### Gameworld 添加 Kanban 連結

**文件：** `games/2048-game/index.html`

```html
<!-- 在 games-grid 中添加 -->
<a href="https://kanban.zeabur.app" class="game-card">
    <div class="game-icon">📊</div>
    <h2 class="game-name">Kanban 看板</h2>
    <p class="game-desc">項目管理看板！追蹤你嘅所有項目進度，需要 Google 登入。</p>
    <div class="game-tags">
        <span class="tag hot">💼 工具</span>
        <span class="tag">生產力</span>
        <span class="tag">需要登入</span>
    </div>
</a>
```

---

### Kanban 添加 Gameworld 連結

**文件：** `kanban-zeabur/public/index.html`

```html
<!-- 在 header 添加 -->
<div class="header">
    <div>
        <h1>📊 Kanban Board</h1>
        <p>Track your projects with OpenClaw</p>
    </div>
    <a href="https://gameworld.zeabur.app" class="back-link" style="
        color: white;
        text-decoration: none;
        padding: 10px 20px;
        background: rgba(255,255,255,0.2);
        border-radius: 8px;
        transition: all 0.3s;
    " onmouseover="this.style.background='rgba(255,255,255,0.3)'" 
       onmouseout="this.style.background='rgba(255,255,255,0.2)'">
        🏠 返回遊戲世界
    </a>
</div>
```

---

## 🔐 Kanban OAuth 配置

### Google Cloud Console 設置

1. **去** https://console.cloud.google.com/

2. **創建/選擇項目**

3. **啟用 Google+ API**

4. **創建 OAuth 憑證：**
   - 去：APIs & Services → Credentials
   - 撳：Create Credentials → OAuth client ID
   - Application type: Web application
   - Name: Kanban Board

5. **配置 Authorized redirect URIs：**
   ```
   https://kanban.zeabur.app/auth/google/callback
   http://localhost:8080/auth/google/callback (for testing)
   ```

6. **記錄 Credentials：**
   - Client ID: `xxxxx.apps.googleusercontent.com`
   - Client Secret: `xxxxx`

---

### Zeabur 環境變量

去 Zeabur Dashboard → Variables:

```bash
# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Google OAuth
GOOGLE_CLIENT_ID=123456789-xxxxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-xxxxx
GOOGLE_CALLBACK_URL=/auth/google/callback

# Session
SESSION_SECRET=super-secret-random-string-change-this
```

---

## ✅ 測試清單

### Gameworld 測試

- [ ] 首頁正常加載
- [ ] 所有遊戲卡片顯示
- [ ] 點擊遊戲正常跳轉
- [ ] Kanban 卡片顯示並連結正確
- [ ] Mobile Responsive 正常

### Kanban 測試

- [ ] 未登入時顯示 Login Screen
- [ ] Google Login 按鈕正常
- [ ] OAuth 流程正常完成
- [ ] 登入後顯示 Kanban Board
- [ ] API 正常調用
- [ ] Logout 正常
- [ ] 返回遊戲世界連結正常

---

## 🐛 故障排除

### 問題 1: OAuth 重定向失敗

**錯誤：** `redirect_uri_mismatch`

**解決：**
```
1. 檢查 Google Cloud Console 的 Authorized redirect URIs
2. 確保同 GOOGLE_CALLBACK_URL 環境變量一致
3. 包括 http://localhost:8080 (for testing)
4. 包括 https://kanban.zeabur.app (for production)
```

---

### 問題 2: Supabase 連接失敗

**錯誤：** `Failed to load projects`

**解決：**
```
1. 檢查 SUPABASE_URL 格式 (必須以 https:// 開頭)
2. 檢查 SUPABASE_ANON_KEY 是否正確
3. 確保 Supabase 表已創建 (boards, columns, projects)
4. 檢查 Zeabur 環境變量是否正確設置
```

---

### 問題 3: Cross-Domain 問題

**錯誤：** CORS errors

**解決：**
```javascript
// server.js 確保有 CORS 配置
app.use(cors({
  origin: ['https://gameworld.zeabur.app', 'https://kanban.zeabur.app'],
  credentials: true
}));
```

---

## 📊 最終架構

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│  User → https://gameworld.zeabur.app                │
│              │                                       │
│              ├── / (Games Homepage)                 │
│              ├── /2048/                             │
│              ├── /snake/                            │
│              ├── /tictactoe/                        │
│              ├── /breakout/                         │
│              ├── /memory/                           │
│              └── [Kanban Card]                      │
│                          │                           │
│                          ▼                           │
│              https://kanban.zeabur.app              │
│                          │                           │
│                          ├── / (Login Required)     │
│                          ├── /api/projects          │
│                          ├── /auth/google           │
│                          └── [Back to Games]        │
│                                                      │
└──────────────────────────────────────────────────────┘
```

---

## 🎯 下一步

1. **更新 Gameworld index.html** - 添加 Kanban 卡片 ✅
2. **更新 Kanban index.html** - 添加返回連結
3. **部署 Gameworld** - `games/2048-game` 到 Zeabur
4. **部署 Kanban** - `kanban-zeabur` 到 Zeabur (新 domain)
5. **配置 OAuth** - Google Cloud Console + Zeabur Variables
6. **測試** - 確保兩個應用互相連結正常

---

**最後更新：** 2026-02-28  
**Version:** 1.0
