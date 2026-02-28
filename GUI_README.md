# 🎨 Kanban Board GUI 使用指南

## 🚀 快速啟動

### 方法 1：直接打開 HTML 文件

最簡單的方法 - 直接在瀏覽器打開：

```bash
# macOS
open kanban-gui.html

# Linux
xdg-open kanban-gui.html

# Windows
start kanban-gui.html
```

或者在瀏覽器地址欄輸入：
```
file:///你的路徑/kanban-gui.html
```

---

### 方法 2：使用本地服務器（推薦）

```bash
# 1. 啟動 Web 服務器
python3 -m http.server 8080

# 2. 在瀏覽器訪問
http://localhost:8080/kanban-gui.html
```

---

### 方法 3：完整設置（含後端處理）

```bash
# 終端 1：啟動後端處理器
python3 kanban-backend.py

# 終端 2：啟動 Web 服務器
python3 -m http.server 8080

# 瀏覽器訪問
http://localhost:8080/kanban-gui.html
```

---

## 📋 GUI 功能

### ✅ 已實現

1. **查看 Board** - 實時顯示所有項目
2. **添加項目** - 點擊「添加新項目」按鈕
3. **移動項目** - 使用按鈕改變項目狀態
4. **完成項目** - 一鍵標記為完成
5. **優先級顯示** - 不同顏色標示優先級
6. **統計數據** - 頂部顯示各狀態項目數量
7. **自動刷新** - 每 30 秒自動更新

### 🎨 界面預覽

```
┌─────────────────────────────────────────────────────────────┐
│                    📊 Kanban Board                          │
│              OpenClaw 項目管理系統                          │
└─────────────────────────────────────────────────────────────┘

[➕ 添加新項目]  [🔄 刷新]

┌─────────┬─────────┬─────────┬─────────┬─────────┐
│  Backlog│  To Do  │In Progress│ Blocked │  Done   │
│    0    │    0    │     0    │    0    │    1    │
├─────────┼─────────┼─────────┼─────────┼─────────┤
│         │         │         │         │✅阿里雲 │
│         │         │         │         │  設置   │
│         │         │         │         │         │
└─────────┴─────────┴─────────┴─────────┴─────────┘
```

---

## 💡 使用技巧

### 添加項目

1. 點擊「➕ 添加新項目」
2. 填寫：
   - 標題（必填）
   - 描述（可選）
   - 優先級（低/中/高/緊急）
   - 初始狀態
3. 點擊「添加」

### 移動項目

每個項目卡片上有操作按鈕：
- **▶️ 開始** - 移到「進行中」
- **✅ 完成** - 移到「已完成」
- **⏪ 暫緩** - 移回「Backlog」

### 查看統計

頂部統計卡片顯示：
- 各狀態的項目數量
- 總項目數

---

## 🔄 數據同步

### 僅查看模式（無需後端）

- ✅ 可以查看 board
- ✅ 點擊按鈕會創建命令文件
- ❌ 不會自動更新（需手動刷新）

### 完整模式（需要後端）

```bash
# 啟動後端處理器
python3 kanban-backend.py
```

- ✅ 實時查看
- ✅ 自動處理命令
- ✅ 自動更新 board

---

## 📁 文件說明

| 文件 | 說明 |
|------|------|
| `kanban-gui.html` | GUI 界面（主要文件） |
| `kanban-board.json` | Board 數據 |
| `kanban-backend.py` | 後端處理器 |
| `kanban-command.json` | 命令隊列（臨時文件） |

---

## 🛠️ 故障排除

### 問題：頁面顯示空白

**解決：**
1. 檢查 `kanban-board.json` 是否存在
2. 查看瀏覽器控制台錯誤（F12）
3. 確保文件在同一目錄

### 問題：添加項目無效

**解決：**
1. 確保後端處理器正在運行
2. 檢查 `kanban-command.json` 是否被處理
3. 刷新頁面查看更新

### 問題：無法訪問 localhost:8080

**解決：**
1. 確認服務器已啟動：`python3 -m http.server 8080`
2. 檢查端口是否被佔用
3. 嘗試其他端口：`python3 -m http.server 3000`

---

## 🎯 快速命令

```bash
# 查看當前項目
python3 kanban_manager.py show

# 添加項目（命令行）
python3 kanban_manager.py add "新項目" "描述" high

# 完成項目
python3 kanban_manager.py complete proj-001

# 啟動 GUI
python3 -m http.server 8080
# 訪問：http://localhost:8080/kanban-gui.html
```

---

## 📞 需要幫助？

1. 查看 `KANBAN_README.md` - 詳細使用指南
2. 運行 `python3 kanban_manager.py help` - 命令行幫助
3. 隨時問我！

---

**享受你的 Kanban Board！** 🎉
