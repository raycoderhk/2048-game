# 🔑 How to Get Google OAuth Credentials

**Time needed:** 5-10 minutes  
**Cost:** FREE

---

## 📋 Step-by-Step Guide

### Step 1: Go to Google Cloud Console
Visit: https://console.cloud.google.com/

Sign in with your Google account (`raycoderhk@gmail.com`)

---

### Step 2: Create New Project (or Select Existing)

1. Click the **project dropdown** at the top of the page
2. Click **"NEW PROJECT"** or **"CREATE PROJECT"**
3. Enter project name: `OpenClaw Dashboard` (or any name you like)
4. Click **"CREATE"**
5. Wait a few seconds, then select the newly created project

---

### Step 3: Enable Google+ API

1. In the left sidebar, go to **APIs & Services** → **Library**
2. Search for **"Google+ API"** or **"Google People API"**
3. Click on it
4. Click **"ENABLE"**

*(Note: Google+ API is needed for profile information)*

---

### Step 4: Configure OAuth Consent Screen

1. Go to **APIs & Services** → **OAuth consent screen**
2. Select **"External"** (unless you have Google Workspace)
3. Click **"CREATE"**

**Fill in the form:**
- **App name:** `OpenClaw Dashboard`
- **User support email:** `raycoderhk@gmail.com`
- **App logo:** (optional)
- **App domain:** Leave blank for now
- **Developer contact:** `raycoderhk@gmail.com`

4. Click **"SAVE AND CONTINUE"**

**Scopes page:**
- Click **"ADD OR REMOVE SCOPES"**
- Select:
  - `.../auth/userinfo.email` - View your email address
  - `.../auth/userinfo.profile` - View your basic profile info
  - `.../auth/openid` - Associate with your info on Google
- Click **"UPDATE"**
- Click **"SAVE AND CONTINUE"**

**Test users page:**
- Click **"ADD USERS"**
- Add: `raycoderhk@gmail.com`
- Click **"SAVE AND CONTINUE"**

5. Click **"BACK TO DASHBOARD"**

---

### Step 5: Create OAuth 2.0 Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **"+ CREATE CREDENTIALS"** at the top
3. Select **"OAuth client ID"**

**If prompted to configure consent screen again:**
- Click **"CONFIGURE CONSENT SCREEN"** and complete Step 4 first

**Create OAuth Client ID:**
- **Application type:** `Web application`
- **Name:** `OpenClaw Dashboard`

**Authorized JavaScript origins:**
Click **"+ ADD URI"** and add:
```
http://localhost:3000
https://kanban-board.zeabur.app
https://pixel-office.zeabur.app
```

**Authorized redirect URIs:**
Click **"+ ADD URI"** and add:
```
http://localhost:3000/auth/google/callback
http://localhost:3000/api/auth/callback/google
https://kanban-board.zeabur.app/auth/google/callback
https://pixel-office.zeabur.app/api/auth/callback/google
```

4. Click **"CREATE"**

---

### Step 6: Copy Your Credentials

A popup will appear with:
```
Your Client ID
xxx.apps.googleusercontent.com

Your Client Secret
xxx-xxxxxxxxxxxxxxx
```

**IMPORTANT:** Copy both values immediately!

- **Client ID:** Looks like `123456789-abc123def456.apps.googleusercontent.com`
- **Client Secret:** Looks like `GOCSPX-abc123def456`

Click **"OK"**

---

### Step 7: Add to Zeabur

#### For Kanban Board:
1. Go to https://zeabur.com/dashboard
2. Select `kanban-board` project
3. Go to **Variables** tab
4. Add these variables:

```
GOOGLE_CLIENT_ID=paste-your-client-id-here.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=paste-your-client-secret-here
GOOGLE_CALLBACK_URL=https://kanban-board.zeabur.app/auth/google/callback
ALLOWED_EMAILS=raycoderhk@gmail.com
SESSION_SECRET=kanban-secret-key-change-this
```

5. Click **"Redeploy"**

#### For Pixel Office:
1. Go to https://zeabur.com/dashboard
2. Select `pixel-office` project
3. Go to **Variables** tab
4. Add these variables:

```
GOOGLE_CLIENT_ID=paste-your-client-id-here.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=paste-your-client-secret-here
NEXTAUTH_SECRET=generate-random-secret-see-below
NEXTAUTH_URL=https://pixel-office.zeabur.app
ALLOWED_EMAILS=raycoderhk@gmail.com
```

5. Click **"Redeploy"**

---

## 🔐 Generate NEXTAUTH_SECRET

For Pixel Office, you need a random secret. Generate it with:

### Option 1: Online Generator
Visit: https://generate-secret.vercel.app/32

Copy the generated value.

### Option 2: Command Line (Mac/Linux)
```bash
openssl rand -base64 32
```

### Option 3: Node.js
```bash
node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"
```

---

## ✅ Verify Setup

### Test Kanban Board:
1. Visit https://kanban-board.zeabur.app
2. Click **"Login with Google"**
3. Select your account (`raycoderhk@gmail.com`)
4. Should redirect back to dashboard ✅

### Test Pixel Office:
1. Visit https://pixel-office.zeabur.app/pixel-office
2. Should redirect to sign-in page
3. Click **"Sign in with Google"**
4. Select your account
5. Should access dashboard ✅

---

## 🚨 Troubleshooting

### Error: "redirect_uri_mismatch"
**Problem:** Redirect URI doesn't match exactly  
**Solution:** Check Zeabur URL matches what you added in Google Console

### Error: "Access blocked: This app's request is invalid"
**Problem:** OAuth consent screen not configured  
**Solution:** Complete Step 4 (OAuth consent screen)

### Error: "Invalid client"
**Problem:** Wrong Client ID or Secret  
**Solution:** Double-check you copied correctly (no extra spaces)

### Can't find Google+ API
**Solution:** Search for "Google People API" instead - same thing

---

## 📸 Visual Guide

**Google Cloud Console Home:**
```
console.cloud.google.com
↓
Select project (top dropdown)
↓
APIs & Services → Library
↓
Enable "Google+ API" or "Google People API"
```

**Create Credentials:**
```
APIs & Services → Credentials
↓
+ CREATE CREDENTIALS
↓
OAuth client ID
↓
Application type: Web application
↓
Add authorized origins and redirect URIs
↓
CREATE
↓
Copy Client ID and Client Secret
```

---

## 🔒 Security Notes

1. **Never share your Client Secret** - It's like a password
2. **Keep allowed emails updated** - Only trusted emails
3. **Use HTTPS in production** - Zeabur provides this automatically
4. **Rotate secrets periodically** - Generate new ones every few months

---

## 📞 Need Help?

**Google Cloud Console:** https://console.cloud.google.com/  
**NextAuth.js Docs:** https://next-auth.js.org/configuration/providers/google  
**Zeabur Support:** https://zeabur.com/docs

---

*Last updated: March 13, 2026*
