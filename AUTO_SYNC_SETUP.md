# 🔄 Auto-Sync Git Commits to Kanban

**Fully automated workflow: Commit code → Kanban updates itself!**

---

## 🎯 What This Does

```
You code → Git commit → Auto-update Kanban → Push
                                    ↓
                    (No manual work needed!)
```

---

## 📋 How It Works

### **1. Commit Message Format**

Include task ID in your commit message:

```bash
git commit -m "feat: Add calendar sync [proj-035]"
git commit -m "fix: Bug fix in auth [proj-001]"
git commit -m "docs: Update README [proj-002]"
```

**Format:** `[proj-XXX]` where XXX is your task ID

---

### **2. Auto-Sync Script**

After each commit, the script:

1. ✅ Reads latest commit (hash, message, date)
2. ✅ Extracts task ID from commit message
3. ✅ Updates `kanban-board.json`:
   - Adds commit to task's `commits` array
   - Updates task status (todo → in_progress)
   - Adds note with commit link
4. ✅ Auto-commits kanban update
5. ✅ Pushes to GitHub

---

### **3. Result in Kanban**

**Before:**
```json
{
  "id": "proj-035",
  "title": "Google Calendar 集成",
  "status": "todo",
  "notes": []
}
```

**After commit `feat: Add calendar sync [proj-035]`:**
```json
{
  "id": "proj-035",
  "title": "Google Calendar 集成",
  "status": "in_progress",
  "commits": [
    {
      "hash": "5ee15f5",
      "message": "feat: Add calendar sync",
      "url": "https://github.com/raycoderhk/2048-game/commit/5ee15f5",
      "date": "2026-03-07"
    }
  ],
  "notes": [
    "🔗 Commit: [5ee15f5](https://github.com/raycoderhk/2048-game/commit/5ee15f5) - feat: Add calendar sync..."
  ]
}
```

---

## 🛠️ Setup (One-Time)

### **Step 1: Install Git Hook**

```bash
# Navigate to workspace
cd /home/node/.openclaw/workspace

# Copy post-commit hook
cp scripts/auto-sync-commits.sh .git/hooks/post-commit

# Make executable
chmod +x .git/hooks/post-commit
```

---

### **Step 2: Test the Hook**

```bash
# Make a test commit
git add some-file.txt
git commit -m "test: Test auto-sync [proj-035]"

# Check if kanban-board.json was updated
git status

# You should see:
# modified: kanban-zeabur/kanban-board.json
```

---

### **Step 3: Configure Repo URL**

Edit `scripts/auto-sync-commits.sh`:

```bash
# Line 18: Update your repo URL
GIT_REPO_URL="https://github.com/raycoderhk/2048-game"
```

---

## 📖 Usage Examples

### **Example 1: Start Working on Task**

```bash
# Work on feature
# ... code ...

# Commit with task ID
git commit -m "feat: Add calendar API integration [proj-035]"

# ✅ Auto-sync runs!
# - Kanban task status: todo → in_progress
# - Commit link added
# - Pushed to GitHub
```

---

### **Example 2: Multiple Commits on Same Task**

```bash
# First commit
git commit -m "feat: Add calendar sync [proj-035]"
# ✅ Commit 1 added to kanban

# Second commit
git commit -m "feat: Add event creation [proj-035]"
# ✅ Commit 2 added to kanban

# Third commit
git commit -m "fix: Fix timezone bug [proj-035]"
# ✅ Commit 3 added to kanban
```

**Result:** Task has 3 commits linked!

---

### **Example 3: Complete Task**

```bash
# Final commit
git commit -m "feat: Complete calendar integration [proj-035]"

# Manually update status to done (or add automation)
# I can help with this via Discord/Telegram command
```

---

## 🔧 Advanced Configuration

### **Skip Auto-Sync for Certain Commits**

Add `[skip-sync]` to commit message:

```bash
git commit -m "chore: Update config [skip-sync]"
# ❌ Auto-sync will skip this commit
```

---

### **Custom Kanban File Location**

Edit `scripts/auto-sync-commits.sh`:

```bash
# Line 16: Update path
KANBAN_FILE="/your/path/kanban-board.json"
```

---

### **Disable Auto-Push**

If you want to review before pushing:

```bash
# Comment out line 167-170 in auto-sync-commits.sh
# git push origin main 2>&1 | head -5
```

---

## 📊 Kanban Schema Updates

### **New `commits` Field**

```json
{
  "commits": [
    {
      "hash": "5ee15f5",
      "message": "feat: Add feature",
      "url": "https://github.com/user/repo/commit/5ee15f5",
      "date": "2026-03-07",
      "added_at": "2026-03-07T08:30:00Z"
    }
  ]
}
```

---

### **Status Auto-Update**

| Commit Action | Status Change |
|---------------|---------------|
| First commit on task | `todo` → `in_progress` |
| Commit with "fix" | `blocked` → `in_progress` |
| Commit with "complete" or "done" | `in_progress` → `done` |

---

## 🎨 Frontend Display

Add this to your Kanban UI to show commits:

```html
<div class="task-commits" ng-if="task.commits && task.commits.length">
  <h4>🔗 Commits</h4>
  <ul>
    <li ng-repeat="commit in task.commits">
      <a href="{{commit.url}}" target="_blank">
        {{commit.hash}} - {{commit.message}}
      </a>
      <span class="commit-date">{{commit.date}}</span>
    </li>
  </ul>
</div>
```

---

## 🐛 Troubleshooting

### **Problem: Hook doesn't run**

```bash
# Check if hook is executable
ls -la .git/hooks/post-commit

# Should show: -rwxr-xr-x
# If not: chmod +x .git/hooks/post-commit
```

---

### **Problem: Task ID not found**

**Solution:** Use correct format in commit message:

```bash
# ❌ Wrong
git commit -m "feat: Add feature proj-035"

# ✅ Correct
git commit -m "feat: Add feature [proj-035]"
```

---

### **Problem: Kanban file not updated**

```bash
# Check script permissions
ls -la scripts/auto-sync-commits.sh

# Should be: -rwxr-xr-x
# If not: chmod +x scripts/auto-sync-commits.sh
```

---

### **Problem: Git push fails**

```bash
# Check git remote
git remote -v

# Should show your GitHub repo
# If not: git remote add origin https://github.com/user/repo
```

---

## 📝 Commit Message Best Practices

### **Good Examples:**

```bash
feat: Add user authentication [proj-001]
fix: Resolve login bug [proj-001]
docs: Update API docs [proj-002]
test: Add unit tests [proj-003]
refactor: Improve code structure [proj-004]
chore: Update dependencies [skip-sync]
```

### **Bad Examples:**

```bash
# ❌ No task ID
git commit -m "Add feature"

# ❌ Wrong format
git commit -m "Add feature proj-001"

# ❌ Task ID not in brackets
git commit -m "Add feature (proj-001)"
```

---

## 🎯 Workflow Summary

```
┌─────────────────────────────────────────────────────────┐
│                  Complete Workflow                      │
└─────────────────────────────────────────────────────────┘

1. 💻 Code your feature
   │
2. 📝 Commit with task ID
   git commit -m "feat: Feature [proj-XXX]"
   │
3. 🤖 Post-commit hook AUTO-RUNS
   │
4. 📊 Kanban updated automatically
   - Status: todo → in_progress
   - Commit link added
   - Notes updated
   │
5. ✅ Auto-commit + auto-push
   │
6. 🎉 Done! Kanban always in sync
```

---

## 🚀 Next Steps

1. ✅ **Script created:** `scripts/auto-sync-commits.sh`
2. ⏳ **Install hook:** Copy to `.git/hooks/post-commit`
3. ⏳ **Test:** Make a test commit
4. ⏳ **Verify:** Check kanban-board.json updated

---

## ❓ Need Help?

**Common issues:**
- Hook not running → Check permissions
- Task ID not found → Use `[proj-XXX]` format
- Kanban not updating → Check file path

**Ask me (Jarvis) for help!** I can:
- Debug the script
- Manually sync if needed
- Update kanban directly

---

**Ready to automate!** 🤖✨
