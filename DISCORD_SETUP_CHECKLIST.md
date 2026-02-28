# ✅ Discord Setup Checklist

*Quick reference for setting up Discord multi-channel support*

---

## 📋 Step-by-Step Checklist

### Phase 1: Discord Bot Setup (5-7 min)

- [ ] **Create Discord Application**
  - [ ] Go to https://discord.com/developers/applications
  - [ ] Click "New Application"
  - [ ] Name: `OpenClaw-Bot`
  - [ ] Click "Create"

- [ ] **Get Bot Credentials**
  - [ ] Go to "Bot" tab
  - [ ] Click "Reset Token" / "View Token"
  - [ ] **COPY TOKEN** (save for later!)
  - [ ] Go to "General Information"
  - [ ] **COPY Application ID**

- [ ] **Enable Intents**
  - [ ] MESSAGE CONTENT INTENT ✅
  - [ ] SERVER MEMBERS INTENT ✅
  - [ ] PRESENCE INTENT ✅

- [ ] **Invite Bot to Server**
  - [ ] Generate invite URL:
    ```
    https://discord.com/api/oauth2/authorize?client_id=YOUR_APP_ID&permissions=8&scope=bot
    ```
  - [ ] Open URL in browser
  - [ ] Select server
  - [ ] Authorize bot

---

### Phase 2: Discord Channel Setup (3-5 min)

- [ ] **Enable Developer Mode**
  - [ ] Discord Settings → Advanced → Developer Mode ✅

- [ ] **Create Channels**
  - [ ] `#💬-general-chat` (日常對話)
  - [ ] `#💻-coding-projects` (編碼任務)
  - [ ] `#🔍-research-reports` (研究報告)
  - [ ] `#📅-schedule-reminders` (日程提醒)
  - [ ] `#📊-kanban-updates` (Kanban 更新)
  - [ ] `#🤖-subagent-logs` (Sub-agent 日誌)
  - [ ] `#⚙️-system-status` (系統狀態)
  - [ ] `#📢-announcements` (重要通知)

- [ ] **Copy Channel IDs**
  - [ ] General Chat ID: `___________________`
  - [ ] Coding Projects ID: `___________________`
  - [ ] Research Reports ID: `___________________`
  - [ ] Schedule Reminders ID: `___________________`
  - [ ] Kanban Updates ID: `___________________`
  - [ ] Sub-agent Logs ID: `___________________`
  - [ ] System Status ID: `___________________`
  - [ ] Announcements ID: `___________________`

---

### Phase 3: OpenClaw Configuration (5-10 min)

- [ ] **Backup Current Config**
  ```bash
  cp /home/node/.openclaw/openclaw.json /home/node/.openclaw/openclaw.json.backup
  ```

- [ ] **Update openclaw.json**
  - [ ] Open `openclaw-discord-template.json`
  - [ ] Replace `YOUR_DISCORD_BOT_TOKEN_HERE` with actual token
  - [ ] Replace all `YOUR_*_CHANNEL_ID` with actual channel IDs
  - [ ] Save file
  - [ ] Copy to OpenClaw directory:
    ```bash
    cp openclaw-discord-template.json /home/node/.openclaw/openclaw.json
    ```

- [ ] **Verify Configuration**
  ```bash
  # Check JSON is valid
  cat /home/node/.openclaw/openclaw.json | python3 -m json.tool > /dev/null && echo "✅ Valid JSON" || echo "❌ Invalid JSON"
  ```

---

### Phase 4: Restart & Test (5 min)

- [ ] **Restart Gateway**
  ```bash
  openclaw gateway restart
  ```

- [ ] **Wait for Startup**
  ```bash
  sleep 15
  ```

- [ ] **Check Status**
  ```bash
  openclaw status
  ```

- [ ] **Verify Discord Connection**
  ```bash
  openclaw channels status --probe
  ```

- [ ] **Test in Discord**
  - [ ] Go to `#💬-general-chat`
  - [ ] Type: `@jarvis Hello!`
  - [ ] Should respond! ✅
  
  - [ ] Go to `#💻-coding-projects`
  - [ ] Type: `@coding Write hello world in Python`
  - [ ] Coding Agent should respond! ✅
  
  - [ ] Go to `#🔍-research-reports`
  - [ ] Type: `@research Search for AI trends`
  - [ ] Research Agent should respond! ✅
  
  - [ ] Go to `#📅-schedule-reminders`
  - [ ] Type: `@admin What's my schedule?`
  - [ ] Admin Agent should respond! ✅

---

### Phase 5: Troubleshooting (if needed)

- [ ] **Bot Not Responding?**
  ```bash
  # Check logs
  openclaw logs --tail 50
  
  # Look for errors
  openclaw logs --tail 50 | grep -i error
  openclaw logs --tail 50 | grep -i discord
  ```

- [ ] **Check Bot Permissions**
  - [ ] Bot has "Read Messages" permission
  - [ ] Bot has "Send Messages" permission
  - [ ] Bot has "Read Message History" permission

- [ ] **Verify Channel IDs**
  - [ ] All channel IDs are correct
  - [ ] No extra spaces or quotes
  - [ ] IDs are strings (in quotes)

---

## 🎯 Quick Reference

### Required Values

| Value | Where to Get | Example |
|-------|-------------|---------|
| **Bot Token** | Discord Developer Portal → Bot → Token | `MTIzNDU2...` |
| **Application ID** | Discord Developer Portal → General Information | `123456789...` |
| **Channel IDs** | Right-click channel → Copy ID | `987654321...` |

### File Locations

| File | Path |
|------|------|
| Main Config | `/home/node/.openclaw/openclaw.json` |
| Template | `/home/node/.openclaw/workspace/openclaw-discord-template.json` |
| Setup Guide | `/home/node/.openclaw/workspace/DISCORD_SETUP_GUIDE.md` |
| Checklist | `/home/node/.openclaw/workspace/DISCORD_SETUP_CHECKLIST.md` |

### Commands

```bash
# Restart gateway
openclaw gateway restart

# Check status
openclaw status

# View logs
openclaw logs --tail 50
openclaw logs --follow

# Check channels
openclaw channels status --probe
```

---

## 📊 Expected Timeline

| Phase | Time | Total |
|-------|------|-------|
| Phase 1: Bot Setup | 5-7 min | 7 min |
| Phase 2: Channel Setup | 3-5 min | 12 min |
| Phase 3: Configuration | 5-10 min | 22 min |
| Phase 4: Test | 5 min | 27 min |
| **Total** | **~30 min** | **~30 min** |

---

## ✅ Success Indicators

You're done when:

- ✅ Bot is online in Discord server
- ✅ Bot responds to `@jarvis` in general-chat
- ✅ Coding tasks route to Coding Agent
- ✅ Research tasks route to Research Agent
- ✅ Schedule questions route to Admin Agent
- ✅ No errors in logs
- ✅ `openclaw status` shows Discord connected

---

## 🆘 Need Help?

If stuck:

1. Check logs: `openclaw logs --tail 50`
2. Verify config: `cat /home/node/.openclaw/openclaw.json`
3. Test connection: `openclaw channels status --probe`
4. Ask Jarvis! Type in Discord: `@jarvis Help me troubleshoot Discord setup`

---

**Good luck! 🎮**
