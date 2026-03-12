# 📚 Book Tracker

A beautiful, persistent book tracking system with dated notes and cover images.

## Features

✨ **What's Included:**

- 📖 **Book Collection Management** - Track books you're reading, want to read, or completed
- 📝 **Dated Notes** - Add timestamped notes that persist across sessions
- 🖼️ **Cover Images** - Visual recognition with book cover photos
- ⭐ **Rating System** - Rate books 1-5 stars
- 🏷️ **Topic Tags** - Organize by topics and categories
- 📊 **Statistics Dashboard** - See your reading progress at a glance
- 🔍 **Filtering** - Filter by reading status (All, Reading, Want to Read, Completed)

## Files

```
book-tracker/
├── index.html          # Main web interface
├── books.json          # Book data with notes (persistent)
└── README.md           # This file
```

## How to Use

### 1. Open the Book Tracker

**Option A: Local File**
```bash
# Open in browser
open /home/node/.openclaw/workspace/book-tracker/index.html
# Or on Windows: start /home/node/.openclaw/workspace/book-tracker/index.html
```

**Option B: GitHub Pages** (after pushing)
```
https://raycoderhk.github.io/openclaw-knowledge/book-tracker/
```

### 2. Add Notes to Books

1. Click **"View Details"** on any book
2. Type your note in the input field
3. Press **Enter** or click **"Add Note"**
4. Notes are automatically dated and saved!

### 3. Update Reading Status

1. Open book details
2. Change status dropdown (Want to Read → Reading → Completed)
3. Status updates automatically save

### 4. Rate Books

Click the stars (1-5) to rate a book after you finish it.

## Data Persistence

**Where are notes saved?**

- Notes are saved in `books.json` in the same folder
- Each note includes:
  - `date`: When the note was added (YYYY-MM-DD)
  - `content`: Your note text
  - `timestamp`: Full ISO timestamp

**Example note:**
```json
{
  "date": "2026-03-10",
  "content": "Key insight: 黑洞不是終點，而是我們與星空之間的開端",
  "timestamp": "2026-03-10T10:30:00Z"
}
```

## Integration with Kanban Board

Books are also tracked in your main Kanban board:
- **Column:** 📚 Books
- **Location:** `/workspace/kanban-board-clean/kanban-board.json`
- **Projects:** book-001 through book-005

## Current Collection (5 Books)

| # | Title | Author | Status |
|---|-------|--------|--------|
| 1️⃣ | The Economist (Mar 7-13, 2026) | Editorial Team | 📖 Reading |
| 2️⃣ | 宇宙的邊界到底在哪裡？ | Unknown | 📋 Want to Read |
| 3️⃣ | AI 时代，说故事 | Karen Eber | 📋 Want to Read |
| 4️⃣ | 藝術有什麼 | 伍常 | 📋 Want to Read |
| 5️⃣ | 天地與音樂的多重變奏 | 柯英嘉 | 📋 Want to Read |

## Future Enhancements

- [ ] Auto-sync with Goodreads API
- [ ] Export notes to Markdown
- [ ] Reading statistics (books/year, pages read)
- [ ] Book recommendations based on topics
- [ ] Share reading progress to Discord

## Tips

💡 **Pro Tips:**

1. **Quick Note:** Click "Quick Note" on any book card for fast note entry
2. **Filter by Status:** Use filter buttons to see only books you're currently reading
3. **Add Purchase Links:** Include links to buy books for easy reference
4. **Cover Images:** Images are stored in `/home/node/.openclaw/media/inbound/`

---

**Created:** March 10, 2026  
**Version:** 1.0  
**Author:** Jarvis (OpenClaw AI Assistant)
