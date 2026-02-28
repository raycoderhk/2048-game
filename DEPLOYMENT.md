# 🚀 2048 Game - Zeabur Deployment Guide

## 部署步驟

### 方法 1: Zeabur (推薦)

1. **登入 Zeabur**
   - https://zeabur.com

2. **創建新項目**
   - 撳 "Deploy" 按鈕
   - 選擇 "GitHub"
   - 揀 `raycoderhk/2048-game`

3. **配置**
   - Service Name: `2048-game`
   - Build Command: (留空 - 靜態網站)
   - Output Directory: (留空)
   - Port: `8080` (Zeabur 會自動分配)

4. **部署**
   - 撳 "Deploy"
   - 等 1-2 分鐘

5. **完成！**
   - Zeabur 會俾條 URL 你
   - 例如：`https://2048-game.zeabur.app`

---

### 方法 2: GitHub Pages

1. **啟用 GitHub Pages**
   - 去 repo: https://github.com/raycoderhk/2048-game
   - Settings → Pages
   - Source: Deploy from branch
   - Branch: main → root
   - 撳 Save

2. **等部署**
   - 約 1-2 分鐘

3. **完成！**
   - URL: `https://raycoderhk.github.io/2048-game/`

---

### 方法 3: Vercel

1. **登入 Vercel**
   - https://vercel.com

2. **Import Project**
   - 揀 GitHub repo: `2048-game`
   - 撳 Import

3. **Deploy**
   - 撳 Deploy
   - 等 1-2 分鐘

4. **完成！**
   - URL: `https://2048-game.vercel.app`

---

## 測試

部署完成後，開條 URL 試玩下！

**控制：**
- Desktop: 方向鍵 ↑↓←→
- Mobile: 滑動

**目標：** 合併到 2048！

---

## 預期 URL

| 平台 | URL 格式 |
|------|----------|
| **Zeabur** | `https://2048-game.zeabur.app` |
| **GitHub Pages** | `https://raycoderhk.github.io/2048-game/` |
| **Vercel** | `https://2048-game.vercel.app` |

---

## 故障排除

### 問題：Zeabur 部署失敗

**解決：**
- 檢查 GitHub repo 係 public
- 確認 `index.html` 喺 root 目錄
- 睇 Zeabur deployment logs

### 問題：GitHub Pages 404

**解決：**
- 等 2-3 分鐘 (需要時間 build)
- 檢查 Settings → Pages 配置
- 確認 `index.html` 喺 main branch

---

**玩得開心！** 🎮
