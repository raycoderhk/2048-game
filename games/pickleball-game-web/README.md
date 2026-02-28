# 🏓 Pickleball Master - Web 版部署指南

## 🌐 在線玩

**Zeabur 部署後：** https://pickleball-game.zeabur.app

---

## 🚀 部署到 Zeabur

### 方法 1：GitHub 部署 (推薦)

#### 1. 上傳到 GitHub

```bash
# 進入遊戲目錄
cd /home/node/.openclaw/workspace/games/pickleball-game-web

# 初始化 Git
git init

# 添加所有文件
git add .

# Commit
git commit -m "Initial commit: Pickleball Master Web Game"

# 添加 remote (替換成你的 GitHub username)
git remote add origin https://github.com/raycoderhk/pickleball-game-web.git

# Push
git push -u origin main
```

#### 2. Zeabur 部署

1. **登入 Zeabur:** https://zeabur.com
2. **New Project** → 選擇你個 GitHub repo
3. **選擇 `pickleball-game-web`**
4. **Deploy!**

#### 3. 配置

- **Port:** 8080 (自動檢測)
- **Node Version:** 18.x
- **Build Command:** (留空)
- **Start Command:** `npm start`

---

### 方法 2：本地測試

```bash
# 進入目錄
cd /home/node/.openclaw/workspace/games/pickleball-game-web

# 安裝依賴
npm install

# 運行
npm start

# 打開 browser
# http://localhost:8080
```

---

## 📁 文件結構

```
pickleball-game-web/
├── index.html      # 遊戲主文件 (HTML/CSS/JS)
├── server.js       # Express 服務器
├── package.json    # Node.js 配置
└── README.md       # 呢個文件
```

---

## 🎮 遊戲特色

### 3 種挑戰模式：

| 模式 | 說明 | 最高分 |
|------|------|--------|
| 📝 知識挑戰 | 回答匹克球問題 | 45 分 |
| ⚡ 反應挑戰 | 測試反應速度 | 30 分 |
| 🎯 發球挑戰 | 發球準確度 | 50 分 |

### 等級系統：

| 等級 | 稱號 | 所需積分 |
|------|------|----------|
| Lv.1 | 🌱 新手 | 0-19 |
| Lv.2 | 🎾 初學者 | 20-39 |
| Lv.3 | 🎯 中級玩家 | 40-69 |
| Lv.4 | ⭐ 高級玩家 | 70-99 |
| Lv.5 | 🏆 匹克球大師 | 100+ |

---

## 📱 分享俾朋友

**URL:** https://pickleball-game.zeabur.app

**QR Code:** (可以用 Zeabur 生成)

---

## 💡 未來改進

- [ ] 記錄最高分 (LocalStorage / Database)
- [ ] 成就系統
- [ ] 多玩家模式 (Online Leaderboard)
- [ ] 更多問題
- [ ] 音效/音樂
- [ ] Mobile 優化

---

## 🎨 技術棧

- **Frontend:** HTML5 + CSS3 + Vanilla JavaScript
- **Backend:** Node.js + Express (靜態文件服務)
- **Deploy:** Zeabur (Free Tier)

---

## 📞 聯絡

**Developer:** Raymond  
**GitHub:** raycoderhk

---

**玩得開心！🏓**
