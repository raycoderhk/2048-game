# 📅 Google Calendar Service Account Setup

**Zero Windows Setup Required!** 🎉

This guide uses **Google Service Account** for server-to-server authentication - no browser OAuth flow needed.

---

## 🎯 Overview

```
┌─────────────────────────────────────────────────────────┐
│              Service Account Flow                       │
│                                                         │
│  1. Create Service Account (Google Cloud Console)       │
│  2. Download JSON Key                                   │
│  3. Share Your Calendar with Service Account            │
│  4. Copy JSON to VPS                                    │
│  5. Configure gog                                       │
│  6. Done! ✅                                            │
└─────────────────────────────────────────────────────────┘
```

**Time:** 15-20 minutes  
**Windows Required:** ❌ No!  
**VPS Only:** ✅ Yes!

---

## 📋 Prerequisites

- [ ] Google Cloud account (free tier works)
- [ ] SSH access to Zeabur VPS
- [ ] Your personal Google Calendar (raycoderhk@gmail.com)

---

## 🔧 Step-by-Step Setup

### **Step 1: Create Google Cloud Project** (5 min)

1. Go to https://console.cloud.google.com/

2. Click **"Create Project"** (or select existing project)

3. Project details:
   - **Name:** `OpenClaw Assistant`
   - **Organization:** (leave default)
   - Click **"Create"**

4. Wait for project creation (30 seconds)

---

### **Step 2: Enable Google Calendar API** (2 min)

1. In Google Cloud Console, go to:
   **APIs & Services** → **Library**

2. Search for: `Google Calendar API`

3. Click on it → **"Enable"**

4. Wait for activation (10 seconds)

✅ **Done!** Calendar API is enabled.

---

### **Step 3: Create Service Account** (5 min)

1. Go to: **APIs & Services** → **Credentials**

2. Click **"+ CREATE CREDENTIALS"** → **"Service account"**

3. Service account details:
   - **Name:** `openclaw-calendar-bot`
   - **ID:** (auto-generated, e.g., `openclaw-calendar-bot@project-id.iam.gserviceaccount.com`)
   - **Description:** `Automated calendar access for OpenClaw`
   - Click **"Create and continue"**

4. **Grant this service account access to project:**
   - **Role:** Select `Calendar API` → `Calendar API Service Agent`
   - Click **"Continue"**

5. **Grant users access to this service account:**
   - Skip this step (click **"Done"**)

✅ **Service account created!**

---

### **Step 4: Generate JSON Key** (3 min)

1. Still in **Credentials** page, find your service account:
   - `openclaw-calendar-bot@your-project-id.iam.gserviceaccount.com`

2. Click on the **email address** (or 3-dot menu → **"Manage keys"**)

3. Go to **"Keys"** tab

4. Click **"+ ADD KEY"** → **"Create new key"**

5. Key type: **JSON** (selected by default)

6. Click **"Create"**

7. **JSON file downloads automatically!**
   - Filename: `openclaw-calendar-bot-xxxxx.json`
   - **⚠️ IMPORTANT:** This file contains private credentials!
   - **🔒 Store securely - treat like a password**

✅ **JSON key downloaded!**

---

### **Step 5: Share Your Calendar** (3 min)

**This step is CRITICAL!** The service account needs permission to access YOUR calendar.

1. Go to https://calendar.google.com/

2. Click **⚙️ Settings** (top right)

3. Left sidebar: **"Settings for my calendars"** → Click your calendar (e.g., `raycoderhk@gmail.com`)

4. Scroll to: **"Share with specific people"**

5. Click **"+ Add people"**

6. Add service account email:
   - **Email:** `openclaw-calendar-bot@your-project-id.iam.gserviceaccount.com`
   - **Permissions:** Select **"Make changes to events"** (or "See all event details")
   - Click **"Send"** (or "OK")

✅ **Calendar shared!**

---

### **Step 6: Copy JSON Key to VPS** (2 min)

**From your Windows PC:**

**Option A: Using VS Code / Cursor** (Easiest)
1. Open the downloaded JSON file in VS Code/Cursor
2. Copy entire content (Ctrl+A, Ctrl+C)
3. SSH to VPS: `ssh root@your-zeabur-vps`
4. Create file: `nano ~/service-account.json`
5. Paste content (Ctrl+Shift+V or right-click)
6. Save: Ctrl+O, Enter, Exit: Ctrl+X
7. Set permissions: `chmod 600 ~/service-account.json`

**Option B: Using PowerShell SCP** (If you have SSH client)
```powershell
scp C:\Users\Raymond\Downloads\openclaw-calendar-bot-xxxxx.json root@your-zeabur-vps:~/service-account.json
```

**On VPS (verify):**
```bash
# Check file exists
ls -la ~/service-account.json

# Should show: -rw------- (600 permissions)
```

✅ **JSON key on VPS!**

---

### **Step 7: Install gog on VPS** (3 min)

**SSH to VPS:**
```bash
ssh root@your-zeabur-vps
```

**Install gog CLI:**
```bash
# Download latest release
wget https://github.com/gogcli/gog/releases/latest/download/gog-linux-amd64 -O /usr/local/bin/gog

# Make executable
chmod +x /usr/local/bin/gog

# Verify installation
gog --version
```

✅ **gog installed!**

---

### **Step 8: Configure gog for Service Account** (2 min)

**On VPS:**
```bash
# Create config directory
mkdir -p ~/.gog

# Set environment variable for service account
export GOOGLE_APPLICATION_CREDENTIALS=~/service-account.json

# Add to .bashrc for persistence
echo 'export GOOGLE_APPLICATION_CREDENTIALS=~/service-account.json' >> ~/.bashrc
echo 'export GOG_ACCOUNT=raycoderhk@gmail.com' >> ~/.bashrc

# Apply changes
source ~/.bashrc

# Verify
echo $GOOGLE_APPLICATION_CREDENTIALS
echo $GOG_ACCOUNT
```

✅ **Environment configured!**

---

### **Step 9: Test Calendar Access** (2 min)

**On VPS:**
```bash
# List calendars (should show your calendar)
gog calendar list

# View upcoming events (next 7 days)
gog calendar events primary \
  --from 2026-03-07T00:00:00+08:00 \
  --to 2026-03-14T23:59:59+08:00
```

**Expected output:**
```
📅 Your Calendar Events:
- 2026-03-08 08:15: 學校旅行 (科大及西貢鹽田梓)
- 2026-03-10 19:00: 匹克球 (Tsuen Wan Pickledise)
...
```

✅ **Calendar access working!**

---

## 🎉 Setup Complete!

---

## 🔧 Troubleshooting

### **Problem: `gog: command not found`**

**Solution:**
```bash
# Check if gog is in PATH
which gog

# If not found, use full path or add to PATH
export PATH=$PATH:/usr/local/bin
```

---

### **Problem: `Error: credentials not found`**

**Solution:**
```bash
# Verify environment variable
echo $GOOGLE_APPLICATION_CREDENTIALS

# Should show: /root/service-account.json

# If empty, re-run:
export GOOGLE_APPLICATION_CREDENTIALS=~/service-account.json
```

---

### **Problem: `Error: calendar not found` or empty results**

**Solution:**
1. Verify calendar is shared with service account (Step 5)
2. Wait 5-10 minutes for permission propagation
3. Try again

---

### **Problem: `Permission denied`**

**Solution:**
```bash
# Check file permissions
ls -la ~/service-account.json

# Should be: -rw------- (600)
# If not, fix:
chmod 600 ~/service-account.json
```

---

## 📊 Next Steps (After Setup)

Once gog works on VPS, I can:

1. **✅ Integrate with OpenClaw Heartbeat**
   - Auto-check calendar every 30 minutes
   - Send reminders for upcoming events

2. **✅ Auto-create events from emails**
   - Detect event invitations
   - Add to calendar automatically

3. **✅ Kanban sync**
   - Events → Kanban tasks
   - Tasks → Calendar events

4. **✅ Voice/chat commands**
   - "What's on my calendar today?"
   - "Add dentist appointment next Tuesday at 3pm"

---

## 🔒 Security Notes

| Best Practice | Why |
|---------------|-----|
| **Keep JSON key private** | Anyone with this file can access your calendar |
| **Set 600 permissions** | Only root can read the file |
| **Don't commit to Git** | Add to `.gitignore` |
| **Rotate keys periodically** | Revoke old keys, create new ones |

---

## 📞 Need Help?

If you get stuck at any step:

1. **Copy the exact error message**
2. **Tell me which step you're on**
3. **I'll help troubleshoot!**

---

## ✅ Checklist

Before moving to integration:

- [ ] Google Cloud Project created
- [ ] Calendar API enabled
- [ ] Service Account created
- [ ] JSON key downloaded
- [ ] Calendar shared with service account
- [ ] JSON key copied to VPS
- [ ] gog installed on VPS
- [ ] Environment variables set
- [ ] `gog calendar list` works
- [ ] `gog calendar events` works

**Once all checked → Ready for OpenClaw integration!** 🚀

---

**Good luck! Let me know when you complete the setup!** 😊
