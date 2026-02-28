# 🚀 Kanban Board Supabase Setup Guide

## Step 1: Create Supabase Project (5 minutes)

1. Go to [supabase.com](https://supabase.com)
2. Click "New Project"
3. Fill in:
   - **Name:** `kanban-board`
   - **Database Password:** (save this!)
   - **Region:** Choose closest to you (e.g., Asia East)
4. Wait 2-3 minutes for setup

## Step 2: Run Database Schema (2 minutes)

1. In your Supabase dashboard, go to **SQL Editor** (left sidebar)
2. Click "New Query"
3. Copy & paste contents from: `kanban-zeabur/supabase-schema.sql`
4. Click "Run" or press `Ctrl+Enter`
5. ✅ You should see "Success. No rows returned"

**Verify tables created:**
- Go to **Table Editor** (left sidebar)
- You should see: `boards`, `columns`, `projects`

## Step 3: Get API Credentials (1 minute)

1. Go to **Settings** (gear icon) → **API**
2. Copy these two values:
   - **Project URL:** `https://xxxxx.supabase.co`
   - **anon/public key:** `eyJhbG...` (long string)

## Step 4: Update Zeabur Deployment (3 minutes)

1. Go to [zeabur.com](https://zeabur.com)
2. Find your `kanban-board` service
3. Go to **Variables** tab
4. Add these environment variables:
   ```
   SUPABASE_URL=https://your-project-id.supabase.co
   SUPABASE_ANON_KEY=your-anon-key-here
   PORT=8080
   ```
5. Zeabur will auto-redeploy (wait 1-2 minutes)

## Step 5: Test Realtime Updates (2 minutes)

1. Open your Zeabur URL in **two browser tabs**
2. In Tab 1: Add a new project
3. Watch Tab 2: It should appear **instantly**! 🎉
4. Try moving projects between columns
5. Both tabs stay in sync automatically

## 🎯 What Changed

### Before (Static)
```
Git Push → Zeabur Build (1-2 min) → UI Updates
```

### After (Realtime)
```
API Call → Supabase → All connected clients update instantly! ⚡
```

## 📊 Database Structure

```
boards (1)
  └── columns (5)
        ├── 📋 Backlog
        ├── 📝 To Do
        ├── 🔄 In Progress
        ├── 🚧 Blocked
        └── ✅ Done
  └── projects (N)
        ├── Title
        ├── Description
        ├── Status
        ├── Priority
        ├── Tags[]
        └── Notes[]
```

## 🔧 Troubleshooting

### "Missing SUPABASE_URL"
- Check Zeabur environment variables
- Make sure no typos in variable names
- Redeploy after adding variables

### "Permission denied"
- Run the SQL schema again
- Check RLS policies are enabled (they're set to allow all by default)

### "Not updating in realtime"
- Open browser console (F12)
- Look for "✅ Supabase connected" message
- Check for any error messages
- Verify SUPABASE_URL is correct

## 🎨 Future Enhancements

- [ ] Add user authentication (Supabase Auth)
- [ ] Drag-and-drop between columns
- [ ] Edit projects inline
- [ ] Search and filter
- [ ] Activity history
- [ ] Export to CSV/JSON

## 📞 Need Help?

- Supabase Docs: https://supabase.com/docs
- Zeabur Docs: https://zeabur.com/docs
- GitHub Repo: https://github.com/raycoderhk/kanban-board

---

**Total Setup Time:** ~10-15 minutes  
**Result:** Realtime collaborative Kanban board! 🚀
