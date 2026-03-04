# 🔧 OpenClaw 實戰手冊 - Troubleshooting 指南

**版本：** 1.0  
**日期：** 2026-03-04  
**OpenClaw 版本：** 2026.2.19

---

## 🚨 常見問題快速修復

### Gateway 無法啟動

**症狀：**
```bash
$ openclaw gateway status
gateway connect failed: Error: pairing required
```

**解決方案：**

```bash
# 方法 1: 重啟 Gateway
openclaw gateway restart

# 方法 2: 修復配置
openclaw doctor --repair

# 方法 3: 手動啟動
openclaw gateway --port 18789
```

---

### Discord Bot 無回應

**症狀：**
- Bot 已邀請到服務器
- 但係無回應任何消息

**解決方案：**

```bash
# 1. 檢查 Bot Token
openclaw config get channels.discord

# 2. 確認 Bot 權限
# Discord Developer Portal → Bot → Permissions
# 確保有：Send Messages, Read Message History

# 3. 重啟 Gateway
openclaw gateway restart

# 4. 測試連接
openclaw channels list
```

**檢查清單：**
- [ ] Bot Token 正確
- [ ] Bot 已邀請到服務器
- [ ] Bot 有足夠權限
- [ ] Gateway 運行中
- [ ] 頻道 ID 正確

---

### Skills 無法安裝

**症狀：**
```bash
$ npx clawhub install github
✖ Rate limit exceeded
```

**解決方案：**

```bash
# 方法 1: 等待 15-30 分鐘
# ClawHub API 有 rate limit

# 方法 2: 手動下載
cd /app/skills
git clone https://github.com/openclaw/openclaw.git
# 複製所需 skills 到 ~/.openclaw/skills/

# 方法 3: 使用 --force
npx clawhub install github --force
```

---

### API Key 無效

**症狀：**
```bash
Error: Invalid API key
```

**解決方案：**

```bash
# 1. 檢查 API Key 是否正確
openclaw config get models

# 2. 確認 API Key 已啟用
# 前往：https://bailian.console.aliyun.com/

# 3. 檢查配額
# 免費額度：100 萬 tokens/月

# 4. 重新配置
openclaw config set models.aliyun/qwen3.5-plus.apiKey "sk-xxx"
```

---

### Command Not Found

**症狀：**
```bash
bash: openclaw: command not found
```

**解決方案：**

```bash
# 方法 1: 重新安裝
npm install -g openclaw@latest

# 方法 2: 檢查 PATH
echo $PATH

# 方法 3: 使用完整路徑
~/.nvm/versions/node/v22.0.0/bin/openclaw

# 方法 4: 重新安裝 Node.js
# https://nodejs.org/
```

---

## 📖 章节特定問題

### Chapter 1: 快速啟動

#### 問題：npm install 失敗

```bash
# 清除 npm 緩存
npm cache clean --force

# 重試安裝
npm install -g openclaw@latest

# 如果仲失敗，檢查 Node.js 版本
node --version  # 需要 v20+
```

#### 問題：Discord Bot 邀請失敗

```
1. 確認你有管理員權限
2. 檢查服務器是否達到 Bot 上限
3. 重新生成 OAuth2 URL
4. 確保 Bot 未禁用
```

---

### Chapter 2: 安全架構

#### 問題：healthcheck skill 無法運行

```bash
# 檢查 skill 是否已安裝
openclaw skills list | grep healthcheck

# 如果顯示 "missing"
npx clawhub install healthcheck

# 如果仲失敗，手動配置
cd /app/skills/healthcheck
npm install
```

#### 問題：SSH 連接失敗

```bash
# 檢查 SSH 配置
sudo nano /etc/ssh/sshd_config

# 確認以下設置：
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes

# 重啟 SSH
sudo systemctl restart sshd
```

---

### Chapter 3: Multi-agent

#### 問題：Agent 無回應

```bash
# 1. 檢查 Gateway 狀態
openclaw gateway status

# 2. 檢查 Agents 配置
openclaw config get agents

# 3. 測試簡單命令
openclaw agent --profile main "你好"

# 4. 查看日誌
openclaw gateway logs
```

#### 問題：Token 使用量過高

```bash
# 1. 檢查用量
openclaw config get models

# 2. 優化策略：
# - 使用 Turbo 模型處理簡單任務
# - 設置 max_tokens 限制
# - 使用緩存減少重複請求

# 3. 設置限額
openclaw config set models.limits.perDay 500000
```

---

### Chapter 4: Dashboard

#### 問題：Kanban Board 無法訪問

```bash
# 1. 檢查 Zeabur 部署
# 前往：https://zeabur.com/

# 2. 檢查環境變數
# PORT=3000
# NODE_ENV=production

# 3. 查看日誌
# Zeabur Dashboard → Logs

# 4. 重新部署
# Zeabur Dashboard → Redeploy
```

#### 問題：數據無法保存

```bash
# 1. 檢查文件權限
ls -la kanban-board.json

# 2. 修復權限
chmod 644 kanban-board.json

# 3. 檢查磁碟空間
df -h

# 4. 檢查文件鎖
lsof kanban-board.json
```

---

### Chapter 5: CLI 工具

#### 問題：Python CLI 無法運行

```bash
# 1. 檢查 Python 版本
python3 --version  # 需要 3.8+

# 2. 安裝依賴
pip3 install requests

# 3. 添加執行權限
chmod +x cli-starter.py

# 4. 運行
python3 cli-starter.py top
```

#### 問題：Node.js CLI 無法運行

```bash
# 1. 檢查 Node.js 版本
node --version  # 需要 18+

# 2. 安裝依賴
npm install axios

# 3. 添加執行權限
chmod +x cli-starter.js

# 4. 運行
node cli-starter.js top
```

---

### Chapter 6: 渠道整合

#### 問題：Telegram Bot 無法連接

```bash
# 1. 檢查 Bot Token
# Telegram: @BotFather → /mybots

# 2. 配置 Webhook
openclaw channels login telegram

# 3. 測試
# 發送消息給 Bot
# 查看日誌：openclaw gateway logs
```

#### 問題：WhatsApp 無法連接

```bash
# 方法 1: 官方 API
# 需要商業驗證

# 方法 2: WhatsApp Web
npm install -g whatsapp-web.js

# 方法 3: OpenClaw 內置
openclaw channels login whatsapp
```

---

### Chapter 7: 雲端部署

#### 問題：Zeabur 部署失敗

```bash
# 1. 檢查 Build Log
# Zeabur Dashboard → Deployments → View Logs

# 2. 常見錯誤：
# - PORT not set → 添加環境變數
# - Build failed → 檢查 package.json
# - Node version → 設置 Node.js 版本

# 3. 重新部署
# Zeabur Dashboard → Redeploy
```

#### 問題：Vercel 部署失敗

```bash
# 1. 檢查 Build Log
vercel logs

# 2. 常見錯誤：
# - Environment variables not set
# - Build command failed
# - Node version mismatch

# 3. 重新部署
vercel --prod
```

---

### Chapter 8: 自動化

#### 問題：Cron 任務無執行

```bash
# 1. 檢查 Cron 狀態
crontab -l

# 2. 檢查日誌
grep CRON /var/log/syslog

# 3. 重啟 Cron 服務
sudo systemctl restart cron

# 4. 測試命令
# 手動運行命令確認無錯誤
```

#### 問題：HEARTBEAT 無觸發

```bash
# 1. 檢查 HEARTBEAT.md 是否存在
ls -la HEARTBEAT.md

# 2. 檢查配置
openclaw config get heartbeat

# 3. 重啟 Gateway
openclaw gateway restart

# 4. 查看日誌
openclaw gateway logs | grep heartbeat
```

---

## 🆘 需要更多幫助？

### 自助資源

1. **文檔：** https://docs.openclaw.ai
2. **GitHub Issues:** https://github.com/openclaw/openclaw/issues
3. **Discord:** https://discord.com/invite/clawd
4. **FAQ:** handbook/FAQ.md

### 聯絡作者

- **Discord:** @raycoderhk
- **Email:** raycoderhk@gmail.com
- **GitHub:** https://github.com/raycoderhk/openclaw-knowledge

### 提供錯誤報告

請包括以下資料：
```
1. OpenClaw 版本：openclaw --version
2. 操作系統：uname -a
3. 錯誤訊息：完整錯誤輸出
4. 重現步驟：點樣導致錯誤
5. 期望結果：應該發生咩
```

---

## 📝 錯誤日誌模板

```markdown
### 錯誤報告

**日期：** 2026-03-04
**OpenClaw 版本：** 2026.2.19
**操作系統：** Ubuntu 22.04

**錯誤訊息：**
```
[粘贴完整錯誤輸出]
```

**重現步驟：**
1. 第一步
2. 第二步
3. 錯誤發生

**期望結果：**
應該發生咩

**已嘗試解決方案：**
- [ ] 重啟 Gateway
- [ ] 檢查配置
- [ ] 查看日誌
```

---

**Last updated:** 2026-03-04  
**Status:** ✅ Ready
