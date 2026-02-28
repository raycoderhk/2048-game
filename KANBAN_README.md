# 📋 Kanban Board 使用指南

## 🎯 快速開始

### 1️⃣ 添加新項目

```bash
# 基本用法
python3 kanban_manager.py add "項目標題"

# 添加描述
python3 kanban_manager.py add "創建網站" "設計並開發新網站"

# 指定優先級 (low/medium/high/urgent)
python3 kanban_manager.py add "緊急修復" "修復生產環境 bug" urgent
```

### 2️⃣ 查看 Board

```bash
# 顯示完整 board
python3 kanban_manager.py show

# 只看特定狀態
python3 kanban_manager.py list todo
python3 kanban_manager.py list in_progress
python3 kanban_manager.py list done
```

### 3️⃣ 移動項目

```bash
# 開始進行
python3 kanban_manager.py move proj-001 in_progress

# 完成項目
python3 kanban_manager.py complete proj-001

# 移回待辦
python3 kanban_manager.py move proj-001 todo

# 標記為阻擋
python3 kanban_manager.py move proj-001 blocked
```

### 4️⃣ 添加備註

```bash
python3 kanban_manager.py note proj-001 "已完成初稿，等待審核"
```

### 5️⃣ 搜索項目

```bash
python3 kanban_manager.py search 網站
python3 kanban_manager.py search API
```

### 6️⃣ 更新項目

```bash
python3 kanban_manager.py update proj-001 priority=high
python3 kanban_manager.py update proj-001 title="新標題"
```

### 7️⃣ 刪除項目

```bash
python3 kanban_manager.py delete proj-001
```

---

## 📊 狀態說明

| 狀態 | 說明 | 使用時機 |
|------|------|----------|
| 📋 **backlog** | 未來可能做的項目 | 想法、建議、暫時不做 |
| 📝 **todo** | 計劃要做的項目 | 已確認要做，但未開始 |
| 🔄 **in_progress** | 進行中的項目 | 正在處理中 |
| 🚧 **blocked** | 被阻擋的項目 | 需要等待外部因素 |
| ✅ **done** | 已完成的項目 | 已完成並驗收 |

---

## 🎯 優先級說明

| 優先級 | 表情 | 說明 |
|--------|------|------|
| **low** | 🟢 | 低優先級，有空再做 |
| **medium** | 🟡 | 中優先級，默認級別 |
| **high** | 🟠 | 高優先級，盡快處理 |
| **urgent** | 🔴 | 緊急，立即處理 |

---

## 💡 實用技巧

### 告訴 OpenClaw 添加項目

你可以直接告訴我：

> "記住這個任務：創建一個新網站，高優先級"

我會自動添加到 Kanban Board！

### 批量操作

```bash
# 完成多個項目
python3 kanban_manager.py complete proj-001
python3 kanban_manager.py complete proj-002
python3 kanban_manager.py complete proj-003
```

### 查看統計

```bash
# 查看 board 時會自動顯示統計
python3 kanban_manager.py show
```

---

## 📁 文件說明

| 文件 | 說明 |
|------|------|
| `kanban-board.json` | 主數據文件 (JSON 格式) |
| `kanban_manager.py` | 管理腳本 |
| `KANBAN_BOARD.md` | 可讀的 Markdown 視圖 |
| `KANBAN_README.md` | 本使用指南 |

---

## 🔄 自動更新

Markdown 視圖 (`KANBAN_BOARD.md`) 會在每次修改 board 後自動更新。

---

## 📞 需要幫助？

```bash
python3 kanban_manager.py help
```

或者隨時問我！
