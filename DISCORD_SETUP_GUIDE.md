# 🎮 Discord Setup Guide for OpenClaw

*Complete setup for multi-channel agent organization*
*Created: 2026-02-26*

---

## 📋 Channel Organization Plan

### Recommended Discord Server Structure

```
🏠 OpenClaw HQ (Server)
│
├── #💬-general-chat          → 日常對話 (Jarvis main)
├── #💻-coding-projects       → 編碼任務 (Coding Agent)
├── #🔍-research-reports      → 研究報告 (Research Agent)
├── #📅-schedule-reminders    → 日程提醒 (Admin Agent)
├── #📊-kanban-board          → Kanban 更新
├── #🤖-subagent-logs         → Sub-agent 日誌
├── #⚙️-system-status         → 系統狀態
└── #📢-announcements         → 重要通知
```

---

## 🚀 Setup Steps

### Step 1: Create Discord Bot (5 min)

1. **Go to Discord Developer Portal:**
   - https://discord.com/developers/applications

2. **Create New Application:**
   - Click "New Application"
   - Name: `OpenClaw-Bot`
   - Click "Create"

3. **Get Bot Token:**
   - Go to "Bot" tab
   - Click "Reset Token" (or "View Token")
   - **Copy the token** (save it securely!)

4. **Enable Privileged Gateway Intents:**
   - Scroll down to "Privileged Gateway Intents"
   - Enable:
     - ✅ MESSAGE CONTENT INTENT
     - ✅ SERVER MEMBERS INTENT
     - ✅ PRESENCE INTENT

5. **Copy Bot ID:**
   - Go to "General Information"
   - Copy "APPLICATION ID"

---

### Step 2: Invite Bot to Your Server (2 min)

1. **Generate Invite URL:**
   ```
   https://discord.com/api/oauth2/authorize?client_id=YOUR_APP_ID&permissions=8&scope=bot
   ```
   - Replace `YOUR_APP_ID` with your Application ID

2. **Open URL in Browser:**
   - Select your server
   - Click "Authorize"

3. **Bot is now in your server!**

---

### Step 3: Create Discord Channels (3 min)

**In your Discord server:**

1. **Create Categories:**
   - Right-click server → "Create Category"
   - Name: `OpenClaw Agents`

2. **Create Text Channels:**
   - `💬-general-chat`
   - `💻-coding-projects`
   - `🔍-research-reports`
   - `📅-schedule-reminders`
   - `📊-kanban-updates`
   - `🤖-subagent-logs`
   - `⚙️-system-status`
   - `📢-announcements`

3. **Copy Channel IDs:**
   - Enable Developer Mode: User Settings → Advanced → Developer Mode
   - Right-click channel → "Copy ID"
   - Save all channel IDs

---

### Step 4: Update OpenClaw Configuration (10 min)

**Update `openclaw.json`:**

```json5
{
  "channels": {
    "discord": {
      "accounts": {
        "default": {
          "token": "YOUR_BOT_TOKEN_HERE",
          "dmPolicy": "pairing",
          "groupPolicy": "allowlist",
          "streamMode": "partial"
        }
      }
    },
    "telegram": {
      "dmPolicy": "pairing",
      "botToken": "8232446525:AAFL780qsojMhAmetS7gS6OeOFoOMzo3MRo",
      "groupPolicy": "allowlist",
      "streamMode": "partial"
    }
  },
  
  "bindings": [
    {
      "agentId": "main",
      "match": {
        "channel": "discord",
        "accountId": "default",
        "peer": {
          "kind": "channel",
          "id": "GENERAL_CHANNEL_ID"
        }
      }
    },
    {
      "agentId": "coding",
      "match": {
        "channel": "discord",
        "accountId": "default",
        "peer": {
          "kind": "channel",
          "id": "CODING_CHANNEL_ID"
        }
      }
    },
    {
      "agentId": "research",
      "match": {
        "channel": "discord",
        "accountId": "default",
        "peer": {
          "kind": "channel",
          "id": "RESEARCH_CHANNEL_ID"
        }
      }
    },
    {
      "agentId": "admin",
      "match": {
        "channel": "discord",
        "accountId": "default",
        "peer": {
          "kind": "channel",
          "id": "ADMIN_CHANNEL_ID"
        }
      }
    },
    {
      "agentId": "main",
      "match": {
        "channel": "telegram",
        "accountId": "default"
      }
    }
  ],
  
  "agents": {
    "list": [
      {
        "id": "main",
        "name": "Jarvis",
        "default": true,
        "workspace": "~/.openclaw/workspace",
        "model": "aliyun/qwen3.5-plus",
        "groupChat": {
          "mentionPatterns": ["@jarvis", "@Jarvis"]
        }
      },
      {
        "id": "coding",
        "name": "Coding Agent",
        "workspace": "~/.openclaw/agents/coding/workspace",
        "agentDir": "~/.openclaw/agents/coding/agent",
        "model": "aliyun/qwen3-coder-plus",
        "groupChat": {
          "mentionPatterns": ["@coding", "@coder", "@dev"]
        }
      },
      {
        "id": "research",
        "name": "Research Agent",
        "workspace": "~/.openclaw/agents/research/workspace",
        "agentDir": "~/.openclaw/agents/research/agent",
        "model": "aliyun/qwen3.5-plus",
        "groupChat": {
          "mentionPatterns": ["@research", "@search", "@study"]
        }
      },
      {
        "id": "admin",
        "name": "Admin Agent",
        "workspace": "~/.openclaw/agents/admin/workspace",
        "agentDir": "~/.openclaw/agents/admin/agent",
        "model": "aliyun/qwen-turbo",
        "groupChat": {
          "mentionPatterns": ["@admin", "@schedule", "@reminder"]
        }
      }
    ],
    "defaults": {
      "model": {
        "primary": "aliyun/qwen3.5-plus"
      },
      "models": {
        "deepseek/deepseek-chat": {},
        "deepseek/deepseek-reasoner": {},
        "aliyun/qwen3.5-plus": {},
        "aliyun/qwen3-coder-plus": {},
        "aliyun/qwen3-max-2026-01-23": {},
        "aliyun/qwen-turbo": {}
      },
      "heartbeat": {
        "target": "discord"
      },
      "maxConcurrent": 4,
      "subagents": {
        "maxSpawnDepth": 2,
        "maxChildrenPerAgent": 5,
        "maxConcurrent": 8,
        "model": "aliyun/qwen-turbo",
        "archiveAfterMinutes": 60
      }
    }
  }
}
```

---

### Step 5: Restart OpenClaw (2 min)

```bash
# Restart gateway
openclaw gateway restart

# Wait for startup
sleep 15

# Check status
openclaw status

# Verify Discord connection
openclaw channels status --probe
```

---

### Step 6: Test Integration (3 min)

**Test in Discord:**

1. **Test Main Agent:**
   - Go to `#💬-general-chat`
   - Type: `@jarvis Hello!`
   - Should respond!

2. **Test Coding Agent:**
   - Go to `#💻-coding-projects`
   - Type: `@coding Write a hello world in Python`
   - Coding Agent should respond!

3. **Test Research Agent:**
   - Go to `#🔍-research-reports`
   - Type: `@research Search for AI trends`
   - Research Agent should respond!

4. **Test Admin Agent:**
   - Go to `#📅-schedule-reminders`
   - Type: `@admin What's my schedule tomorrow?`
   - Admin Agent should respond!

---

## 📊 Channel Routing Logic

### Automatic Routing by Channel

| Discord Channel | Agent | Use Case |
|----------------|-------|----------|
| `#💬-general-chat` | Jarvis (main) | 日常對話、一般問題 |
| `#💻-coding-projects` | Coding Agent | 編碼、技術任務 |
| `#🔍-research-reports` | Research Agent | 研究、搜尋、分析 |
| `#📅-schedule-reminders` | Admin Agent | 日程、提醒、行政 |
| `#📊-kanban-updates` | Jarvis | Kanban 更新通知 |
| `#🤖-subagent-logs` | System | Sub-agent 日誌 |
| `⚙️-system-status` | System | 系統狀態更新 |
| `#📢-announcements` | Jarvis | 重要通知 |

---

### Routing by Mention (in Group Channels)

If you want to use **one general channel** but still route to different agents:

```json5
{
  "bindings": [
    {
      "agentId": "main",
      "match": {
        "channel": "discord",
        "accountId": "default"
      }
    }
  ],
  "agents": {
    "list": [
      {
        "id": "main",
        "groupChat": {
          "mentionPatterns": ["@jarvis", "@Jarvis", "@主 agent"]
        }
      },
      {
        "id": "coding",
        "groupChat": {
          "mentionPatterns": ["@coding", "@coder", "@開發"]
        }
      },
      {
        "id": "research",
        "groupChat": {
          "mentionPatterns": ["@research", "@研究", "@search"]
        }
      },
      {
        "id": "admin",
        "groupChat": {
          "mentionPatterns": ["@admin", "@日程", "@reminder"]
        }
      }
    ]
  }
}
```

**Usage:**
- `@jarvis 幫我寫個郵件` → Jarvis 回覆
- `@coding 幫我寫個 Python 腳本` → Coding Agent 回覆
- `@research 幫我搜尋資料` → Research Agent 回覆
- `@admin 提醒我明天的會議` → Admin Agent 回覆

---

## 🔧 Advanced Configuration

### Sub-agent Output Routing

**Send sub-agent completions to specific channel:**

```json5
{
  "agents": {
    "defaults": {
      "subagents": {
        "announceChannel": "SUBAGENT_LOGS_CHANNEL_ID"
      }
    }
  }
}
```

### Heartbeat Routing

**Send heartbeats to specific channel:**

```json5
{
  "agents": {
    "defaults": {
      "heartbeat": {
        "target": "discord",
        "channel": "SCHEDULE_REMINDERS_CHANNEL_ID"
      }
    }
  }
}
```

### Cron Job Output

**Send cron job results to specific channel:**

```json5
{
  "agents": {
    "list": [
      {
        "id": "admin",
        "cron": {
          "defaultChannel": "SCHEDULE_REMINDERS_CHANNEL_ID"
        }
      }
    ]
  }
}
```

---

## 🎯 Quick Reference

### Required Information

Before starting, prepare:

- [ ] Discord Bot Token
- [ ] Discord Application ID
- [ ] Server ID
- [ ] Channel IDs:
  - [ ] General Chat
  - [ ] Coding Projects
  - [ ] Research Reports
  - [ ] Schedule Reminders
  - [ ] Kanban Updates
  - [ ] Sub-agent Logs

### Commands Checklist

```bash
# 1. Update config
# Edit openclaw.json with Discord settings

# 2. Restart gateway
openclaw gateway restart

# 3. Check status
openclaw status

# 4. Verify Discord
openclaw channels status --probe

# 5. Test in Discord
# Type @jarvis in general-chat channel
```

---

## 🐛 Troubleshooting

### Problem 1: Bot Doesn't Respond

**Check:**
1. Bot is in the server
2. Bot has permissions to read/send messages
3. MESSAGE CONTENT INTENT is enabled
4. Channel ID is correct in config

**Fix:**
```bash
# Check logs
openclaw logs --tail 50

# Look for Discord errors
openclaw logs --tail 50 | grep -i discord
```

---

### Problem 2: Wrong Agent Responds

**Check:**
1. Binding configuration
2. Channel IDs match
3. Mention patterns are correct

**Fix:**
- Review `bindings` in `openclaw.json`
- Ensure channel IDs are correct
- Restart gateway after changes

---

### Problem 3: Bot Can't Read Messages

**Check:**
1. Server permissions
2. Channel permissions
3. Role assignments

**Fix:**
- Right-click bot → Roles
- Ensure bot has "Read Messages" permission
- Ensure bot has "Send Messages" permission

---

## 📈 Next Steps

After basic setup:

1. **Set up automated reports:**
   - Daily summary to `#📢-announcements`
   - Sub-agent logs to `#🤖-subagent-logs`
   - System status to `#⚙️-system-status`

2. **Configure notifications:**
   - Kanban updates → `#📊-kanban-updates`
   - Schedule reminders → `#📅-schedule-reminders`
   - Critical alerts → `#📢-announcements`

3. **Set up webhooks:**
   - GitHub notifications
   - CI/CD updates
   - External service alerts

---

## 🎉 Success Criteria

You'll know it's working when:

- ✅ Bot responds to `@jarvis` in general-chat
- ✅ Coding tasks in coding channel get Coding Agent
- ✅ Research requests get Research Agent
- ✅ Schedule questions get Admin Agent
- ✅ Sub-agent completions post to logs channel
- ✅ Heartbeat messages post to schedule channel

---

**Ready to set up? Let me know if you need help with any step!** 🚀
