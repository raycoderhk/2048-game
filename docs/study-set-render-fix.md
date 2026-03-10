# 🔧 Render Keep-Alive Workflow - Fix Guide

**Issue:** Multiple GitHub Actions failures detected (4 failures today)  
**Repository:** `raycoderhk/study-set`  
**Workflow:** Render Keep-Alive  
**Status:** ❌ Failing repeatedly

---

## 📊 Failure Pattern

| Time | Commit | Status |
|------|--------|--------|
| 13:30 HKT | fcd834a | ❌ Failed |
| 13:30 HKT | 5d5282f | ❌ Failed |
| 13:30 HKT | f4f8618 | ❌ Failed |
| 14:30 HKT | c404327 | ❌ Failed |

**Pattern:** Workflow failing every run, likely a configuration issue.

---

## 🔍 Common Causes

### 1. Missing GitHub Secret: `RENDER_APP_URL` ❌

**Most likely cause!** The workflow needs this secret to ping your Render app.

**Fix:**
1. Go to: https://github.com/raycoderhk/study-set/settings/secrets/actions
2. Click **"New repository secret"**
3. Add:
   - **Name:** `RENDER_APP_URL`
   - **Value:** Your Render app URL (e.g., `https://your-app.onrender.com`)
4. Click **"Add secret"**

---

### 2. Workflow File Missing or Incorrect

**Check if workflow file exists:**
- Path: `.github/workflows/keep-alive.yml`
- If missing, create it (see template below)

**Workflow Template:**
```yaml
name: Render Keep-Alive

on:
  schedule:
    - cron: '*/10 * * * *'  # Every 10 minutes
  workflow_dispatch:  # Allow manual trigger

jobs:
  ping-render:
    runs-on: ubuntu-latest
    steps:
      - name: Ping Render App
        run: |
          RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "${{ secrets.RENDER_APP_URL }}")
          echo "Response code: $RESPONSE"
          if [ "$RESPONSE" -ge 200 ] && [ "$RESPONSE" -lt 400 ]; then
            echo "✅ App is alive!"
            exit 0
          else
            echo "❌ App ping failed with status: $RESPONSE"
            exit 1
          fi
```

---

### 3. Render App URL Invalid or Expired

**Check:**
1. Go to: https://dashboard.render.com/
2. Find your app
3. Copy the correct URL (should be `https://xxx.onrender.com`)
4. Update the `RENDER_APP_URL` secret

---

### 4. Render App Deleted or Suspended

**Check:**
1. Log in to Render dashboard
2. Verify app status is "Running"
3. If suspended, redeploy or upgrade

---

## 🛠️ Step-by-Step Fix

### Step 1: Add GitHub Secret

```
1. https://github.com/raycoderhk/study-set/settings/secrets/actions
2. Click "New repository secret"
3. Name: RENDER_APP_URL
4. Value: https://your-app.onrender.com
5. Click "Add secret"
```

### Step 2: Verify Workflow File

```
1. https://github.com/raycoderhk/study-set/tree/main/.github/workflows
2. Check if keep-alive.yml exists
3. If not, create it with template above
```

### Step 3: Test Manually

```
1. https://github.com/raycoderhk/study-set/actions
2. Click "Render Keep-Alive" workflow
3. Click "Run workflow" (manual trigger)
4. Check if it passes ✅
```

### Step 4: Check Render App

```
1. https://dashboard.render.com/
2. Verify app is running
3. Check app logs for errors
```

---

## 📋 Quick Checklist

- [ ] GitHub secret `RENDER_APP_URL` added
- [ ] Workflow file `.github/workflows/keep-alive.yml` exists
- [ ] Render app URL is valid and accessible
- [ ] Render app is running (not suspended)
- [ ] Manual workflow trigger passes

---

## 🎯 Alternative: Disable Keep-Alive

If you don't need 24/7 uptime:

**Option 1: Disable Workflow**
```
1. https://github.com/raycoderhk/study-set/actions
2. Click "Render Keep-Alive"
3. Click "⋮" (three dots)
4. Select "Disable workflow"
```

**Option 2: Delete Workflow**
```
1. Go to repo root
2. Delete `.github/workflows/keep-alive.yml`
3. Commit changes
```

**Note:** Render free tier apps sleep after 15 mins inactivity. First request after sleep takes ~30 seconds (cold start).

---

## 📧 Contact Info

If you need help:
- Render Support: https://render.com/support
- GitHub Actions Docs: https://docs.github.com/en/actions

---

**Created by:** OpenClaw Assistant  
**Date:** 2026-03-10  
**Priority:** HIGH (4 failures detected)
