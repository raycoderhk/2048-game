# OpenClaw Devbox Deployment Guide

## Quick Start (5 minutes)

### Step 1: Find Devbox Template

**URL:** https://zeabur.com/templates

**Search:** `OpenClaw devbox` or `ZBVZNH`

**If found:** Click "Deploy" → Go to Step 2

**If NOT found:** Use Option B below (Custom Docker)

---

### Step 2: Configure Devbox

**Service Settings:**
```
Name: openclaw-devbox
Region: Tokyo or Jakarta (match your main OpenClaw)
Cluster: Flex Shared (free tier)
```

**Environment Variables:**
```bash
OPENCLAW_GATEWAY_HOST=openclaw.zeabur.internal
EXEC_SECURITY=full
ALIYUN_API_KEY=sk-sp-8eec812bc72d47c3866d388cef6372f8
```

**Deploy!** (Wait 1-2 minutes)

---

### Step 3: Connect to Main OpenClaw

**In your Main OpenClaw chat (Discord/Telegram):**

1. **List nodes:**
   ```
   openclaw nodes list
   ```

2. **You should see devbox:**
   ```
   Node ID: devbox-xxx
   Status: pending
   ```

3. **Approve it:**
   ```
   openclaw devices approve devbox-xxx
   ```

4. **Verify connection:**
   ```
   openclaw nodes list
   ```
   Status should be: `connected` ✅

---

### Step 4: Install Pillow

**In OpenClaw chat:**
```
openclaw nodes run --node devbox pip install Pillow --user
```

**Expected output:**
```
Successfully installed Pillow-xx.x.x
```

---

### Step 5: Test Image Processing

**Send an image and ask:**
```
What's in this image?
```

**Or:**
```
Extract text from this screenshot
```

**Should work!** ✅

---

## Option B: Custom Docker (If Devbox Template Unavailable)

### Step 1: Build Custom Image

**In GitHub repo:**
1. Add the `Dockerfile` (provided)
2. Push to GitHub
3. Zeabur will auto-build

### Step 2: Deploy to Zeabur

1. Go to Zeabur Dashboard
2. New Service → Docker
3. Image: `your-username/openclaw-custom:latest`
4. Deploy!

### Step 3: Configure

Same environment variables as main OpenClaw.

---

## Option C: Use Cloud Vision API

If local processing is too complex, use cloud APIs:

### Google Vision API Skill

**Setup:**
1. Get Google Cloud API key
2. Create vision-api skill
3. Send images to Google for analysis

**Pros:** No local dependencies
**Cons:** API costs, privacy concerns

---

## Troubleshooting

### Devbox not connecting:
- Check `OPENCLAW_GATEWAY_HOST` is correct
- Verify both services in same Zeabur project
- Check firewall/network settings

### Pillow install fails:
- Try: `pip install Pillow --user`
- Or: `python3 -m pip install Pillow`

### Image processing still fails:
- Check skill is routing to devbox
- Verify Pillow is installed: `pip list | grep Pillow`

---

## Next Steps After Success

1. ✅ Test image processing
2. ✅ Update Kanban (proj-009 → Done!)
3. ✅ Create more skills that need pip packages
4. ✅ Deploy Jarvis + sub-agents on devbox

---

**Questions? Share what you see in Zeabur!**
