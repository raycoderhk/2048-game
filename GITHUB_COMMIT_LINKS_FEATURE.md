# 🔗 GitHub Commit Links for Kanban Tasks

**Feature:** Add clickable GitHub commit links to Kanban tasks

---

## ✅ Yes, This Works!

GitHub commit URLs follow a standard format:

```
https://github.com/{username}/{repo}/commit/{commit-hash}
```

**Example:**
```
https://github.com/raycoderhk/2048-game/commit/5ee15f5
```

---

## 🎯 Implementation Options

### **Option 1: Add to Task Notes** (Simplest)

Add commit links directly in task notes:

```json
{
  "id": "proj-XXX",
  "title": "Phase 1 | NEW-01: 實時進度追蹤",
  "status": "done",
  "notes": [
    "✅ Done",
    "🔗 Commit: https://github.com/raycoderhk/2048-game/commit/5ee15f5"
  ]
}
```

**Pros:**
- ✅ No schema changes needed
- ✅ Works immediately
- ✅ Multiple commits per task supported

**Cons:**
- ⚠️ Manual entry (not auto-detected)

---

### **Option 2: Add `commits` Field to Schema** (Structured)

Add a dedicated `commits` array to each task:

```json
{
  "id": "proj-XXX",
  "title": "Phase 1 | NEW-01: 實時進度追蹤",
  "status": "done",
  "commits": [
    {
      "hash": "5ee15f5",
      "message": "Add real-time progress tracking",
      "url": "https://github.com/raycoderhk/2048-game/commit/5ee15f5",
      "date": "2026-03-07T10:00:00Z"
    }
  ]
}
```

**Pros:**
- ✅ Structured data
- ✅ Can store multiple commits
- ✅ Can auto-generate URLs

**Cons:**
- ⚠️ Requires schema update
- ⚠️ Need to update frontend to display

---

### **Option 3: Auto-Sync from Git** (Advanced)

Create a script that:
1. Reads recent git commits
2. Matches commit messages to task IDs
3. Auto-updates Kanban JSON

**Example commit message format:**
```
feat: Add real-time progress tracking [proj-XXX]
```

**Pros:**
- ✅ Fully automated
- ✅ No manual entry

**Cons:**
- ⚠️ Complex setup
- ⚠️ Requires commit message convention

---

## 🛠️ Recommended: Option 1 + Option 2 Hybrid

**Start with Option 1** (add to notes) for immediate use.

**Later upgrade to Option 2** (structured field) when you want automation.

---

## 📝 Example: Updated Task Format

### Current Format:
```json
{
  "id": "proj-XXX",
  "title": "Phase 1 | NEW-01: 實時進度追蹤",
  "description": "...",
  "status": "done",
  "priority": "high",
  "notes": [
    "✅ Done"
  ]
}
```

### Updated Format (with commits):
```json
{
  "id": "proj-XXX",
  "title": "Phase 1 | NEW-01: 實時進度追蹤",
  "description": "...",
  "status": "done",
  "priority": "high",
  "commits": [
    {
      "hash": "5ee15f5",
      "url": "https://github.com/raycoderhk/2048-game/commit/5ee15f5",
      "message": "Add real-time progress tracking",
      "date": "2026-03-07"
    }
  ],
  "notes": [
    "✅ Done",
    "🔗 [View Commit](https://github.com/raycoderhk/2048-game/commit/5ee15f5)"
  ]
}
```

---

## 🎨 Frontend Display (Kanban UI)

Add a "Commits" section to task cards:

```html
<div class="task-commits">
  <strong>🔗 Commits:</strong>
  <ul>
    <li>
      <a href="https://github.com/raycoderhk/2048-game/commit/5ee15f5" target="_blank">
        5ee15f5 - Add real-time progress tracking
      </a>
    </li>
  </ul>
</div>
```

---

## 🚀 Quick Start: Manual Method (Now)

For your example task:

**1. Edit `kanban-board.json`:**
```json
{
  "id": "proj-XXX",
  "title": "Phase 1 | NEW-01: 實時進度追蹤",
  "notes": [
    "✅ Done",
    "🔗 Commit: https://github.com/raycoderhk/2048-game/commit/5ee15f5"
  ]
}
```

**2. Frontend will render as clickable link** (if using markdown rendering)

---

## 🤖 Automation: Git Hook Script (Future)

Create `.git/hooks/post-commit`:

```bash
#!/bin/bash
# Auto-add commit to Kanban task

COMMIT_HASH=$(git rev-parse --short HEAD)
COMMIT_MSG=$(git log -1 --pretty=%B)
REPO_URL="https://github.com/raycoderhk/2048-game"

# Extract task ID from commit message (e.g., [proj-XXX])
TASK_ID=$(echo "$COMMIT_MSG" | grep -oP '\[proj-\w+\]' | tr -d '[]')

if [ -n "$TASK_ID" ]; then
    echo "Adding commit $COMMIT_HASH to $TASK_ID"
    # Update kanban-board.json with commit info
fi
```

---

## 📋 My Recommendation

**For now (Quick Win):**

1. ✅ Add commit links to task **notes** (manual)
2. ✅ Works immediately with current Kanban UI
3. ✅ No code changes needed

**Later (When you want automation):**

1. 🔄 Add `commits` array to schema
2. 🔄 Update frontend to display commits
3. 🔄 Create auto-sync script

---

## ❓ Want Me to:

**A)** Add commit link to your example task now (manual)?  
**B)** Create structured schema with `commits` field?  
**C)** Build auto-sync script for future?

**Let me know!** 🚀
