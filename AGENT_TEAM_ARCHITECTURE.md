# 🤖 OpenClaw Agent Team 架構

*最後更新：2026-02-26*

---

## 📋 設計理念

基於你的使用場景，我設計了一個 **主從式 agent 團隊**：

```
┌─────────────────────────────────────────────────────┐
│              🧠 Jarvis (主 orchestrator)            │
│         模型：aliyun/qwen3.5-plus (包月)            │
│         職責：任務分發、最終決策、用戶溝通          │
└─────────────────────────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          │               │               │
          ▼               ▼               ▼
    ┌──────────┐   ┌──────────┐   ┌──────────┐
    │  Coding  │   │ Research │   │  Admin   │
    │  Agent   │   │  Agent   │   │  Agent   │
    └──────────┘   └──────────┘   └──────────┘
```

---

## 🎯 Agent 角色設計

### 1️⃣ **Jarvis (主 Agent)** - `main`
**職責：**
- ✅ 接收用戶請求
- ✅ 任務分析和分發
- ✅ 最終決策和回覆
- ✅ 管理 sub-agents

**模型：** `aliyun/qwen3.5-plus` (包月， unlimited)

**特點：**
- 溫暖、幽默、有個性
- 了解你的個人情況（家庭、日程、偏好）
- 主動提醒重要事項

---

### 2️⃣ **Coding Agent** - `coding`
**職責：**
- 💻 編寫和調試代碼
- 🔧 配置 OpenClaw 和技能
- 🧪 測試和驗證
- 📝 技術文檔

**模型：** `aliyun/qwen3-coder-plus` (編碼專用)

**觸發場景：**
- "幫我寫一個..."
- "修復這個 bug"
- "配置..."
- "創建腳本..."

---

### 3️⃣ **Research Agent** - `research`
**職責：**
- 🔍 網絡搜索和研究
- 📰 新聞和資訊整理
- 📊 數據分析
- 📚 資料收集和總結

**模型：** `aliyun/qwen3.5-plus` (平衡性能和成本)

**觸發場景：**
- "搜尋..."
- "幫我研究..."
- "整理關於..."
- "分析..."

---

### 4️⃣ **Admin Agent** - `admin`
**職責：**
- 📅 日程管理和提醒
- 📋 Kanban Board 維護
- 📊 系統監控
- 🔄 例行任務（晨報、心跳等）

**模型：** `aliyun/qwen-turbo` (快速、便宜)

**觸發場景：**
- 日程查詢
- 添加待辦事項
- 系統狀態檢查
- 定時任務

---

## 📁 工作區結構

```
~/.openclaw/
├── workspace/                    # 主工作區 (Jarvis)
│   ├── SOUL.md
│   ├── AGENTS.md
│   ├── USER.md
│   ├── HEARTBEAT.md
│   ├── MEMORY.md
│   ├── kanban-board.json
│   └── ...
│
├── agents/
│   ├── main/                     # Jarvis (主 agent)
│   │   ├── agent/
│   │   │   ├── models.json
│   │   │   └── auth-profiles.json
│   │   └── sessions/
│   │
│   ├── coding/                   # Coding Agent
│   │   ├── agent/
│   │   │   ├── models.json
│   │   │   └── auth-profiles.json
│   │   ├── workspace/
│   │   │   ├── SOUL.md          # 技術專家性格
│   │   │   ├── AGENTS.md        # 編碼規範
│   │   │   └── TOOLS.md         # 開發工具配置
│   │   └── sessions/
│   │
│   ├── research/                 # Research Agent
│   │   ├── agent/
│   │   │   ├── models.json
│   │   │   └── auth-profiles.json
│   │   ├── workspace/
│   │   │   ├── SOUL.md          # 研究員性格
│   │   │   ├── AGENTS.md        # 研究規範
│   │   │   └── TOOLS.md         # 搜索工具配置
│   │   └── sessions/
│   │
│   └── admin/                    # Admin Agent
│       ├── agent/
│       │   ├── models.json
│       │   └── auth-profiles.json
│       ├── workspace/
│       │   ├── SOUL.md          # 管家性格
│       │   ├── AGENTS.md        # 行政規範
│       │   └── TOOLS.md         # 日程工具配置
│       └── sessions/
│
└── openclaw.json                 # 主配置文件
```

---

## ⚙️ 配置示例

### openclaw.json (多 agent 配置)

```json5
{
  "agents": {
    "list": [
      {
        "id": "main",
        "name": "Jarvis",
        "default": true,
        "workspace": "~/.openclaw/workspace",
        "model": "aliyun/qwen3.5-plus"
      },
      {
        "id": "coding",
        "name": "Coding Agent",
        "workspace": "~/.openclaw/agents/coding/workspace",
        "model": "aliyun/qwen3-coder-plus"
      },
      {
        "id": "research",
        "name": "Research Agent",
        "workspace": "~/.openclaw/agents/research/workspace",
        "model": "aliyun/qwen3.5-plus"
      },
      {
        "id": "admin",
        "name": "Admin Agent",
        "workspace": "~/.openclaw/agents/admin/workspace",
        "model": "aliyun/qwen-turbo"
      }
    ],
    "defaults": {
      "subagents": {
        "maxSpawnDepth": 2,      // 允許 sub-agent 再 spawn worker
        "maxChildrenPerAgent": 5,
        "maxConcurrent": 8,
        "model": "aliyun/qwen-turbo",  // sub-agents 用便宜模型
        "archiveAfterMinutes": 60
      }
    }
  },

  "bindings": [
    // Telegram 主聊天 → Jarvis
    {
      "agentId": "main",
      "match": { "channel": "telegram", "accountId": "default" }
    }
  ],

  "tools": {
    "subagents": {
      "tools": {
        "deny": ["cron"]  // sub-agents 不能創建 cron
      }
    }
  }
}
```

---

## 🚀 使用場景

### 場景 1：編碼任務

**用戶：** "幫我創建一個 Python 腳本來爬取天氣數據"

**Jarvis (主 agent)：**
1. 分析任務 → 需要編碼
2. Spawn `coding` sub-agent
3. 等待結果
4. 整合回覆給用戶

```
用戶 → Jarvis → [spawn coding agent] → 執行 → 結果 → Jarvis → 用戶
```

---

### 場景 2：研究任務

**用戶：** "幫我研究阿里雲 Coding Plan 和 DeepSeek API 的性價比"

**Jarvis (主 agent)：**
1. 分析任務 → 需要研究
2. Spawn `research` sub-agent
3. Research agent 進行 web_search
4. 整理報告 → Jarvis → 用戶

```
用戶 → Jarvis → [spawn research agent] → web_search → 報告 → Jarvis → 用戶
```

---

### 場景 3：複雜任務（多 sub-agents）

**用戶：** "幫我創建一個完整的股票分析系統，包括數據爬取、分析、和可視化"

**Jarvis (主 agent)：**
1. 分析任務 → 複雜、多步驟
2. Spawn `coding` agent 作為 orchestrator (depth 1)
3. Coding agent spawn 多個 worker sub-agents (depth 2)：
   - Worker 1: 數據爬取模塊
   - Worker 2: 分析模塊
   - Worker 3: 可視化模塊
4. 整合所有結果 → Jarvis → 用戶

```
用戶 → Jarvis → [spawn coding orchestrator]
                      ├─→ [spawn worker 1: 爬取]
                      ├─→ [spawn worker 2: 分析]
                      └─→ [spawn worker 3: 可視化]
                   ← 整合結果 ← Jarvis → 用戶
```

---

### 場景 4：日程管理

**用戶：** "提醒我明天的匹克球活動"

**Jarvis (主 agent)：**
1. 分析任務 → 日程管理
2. 調用 `admin` agent 或直接處理
3. 檢查 HEARTBEAT.md
4. 設置提醒

---

## 💡 Sub-agent 使用模式

### 模式 1：簡單任務（直接 spawn）

```python
# Jarvis 直接 spawn sub-agent
sessions_spawn(
    agentId="coding",
    task="創建一個 Python 腳本來爬取天氣數據",
    model="aliyun/qwen3-coder-plus"
)
```

### 模式 2：複雜任務（orchestrator 模式）

```python
# Jarvis spawn orchestrator
sessions_spawn(
    agentId="coding",
    task="創建股票分析系統",
    # coding agent 會再 spawn 多個 worker
)
```

### 模式 3：並行任務

```python
# 同時 spawn 多個 sub-agents
sessions_spawn(agentId="research", task="研究竞品 A")
sessions_spawn(agentId="research", task="研究竞品 B")
sessions_spawn(agentId="research", task="研究竞品 C")
# 等待所有完成後整合
```

---

## 📊 成本優化

| Agent | 模型 | 用途 | 成本 |
|-------|------|------|------|
| **Jarvis (main)** | qwen3.5-plus | 主對話、決策 | 包月 |
| **Coding** | qwen3-coder-plus | 編碼任務 | 包月 |
| **Research** | qwen3.5-plus | 研究分析 | 包月 |
| **Admin** | qwen-turbo | 日程、監控 | 包月 |
| **Sub-agents** | qwen-turbo | worker 任務 | 包月 |

**全部使用阿里雲 Coding Plan 包月，無額外費用！** ✅

---

## 🎯 下一步

### 1. 創建 Agent 工作區

```bash
# 創建 coding agent
openclaw agents add coding

# 創建 research agent
openclaw agents add research

# 創建 admin agent
openclaw agents add admin
```

### 2. 配置每個 Agent

為每個 agent 創建：
- `SOUL.md` - 性格和行為準則
- `AGENTS.md` - 職責和規範
- `TOOLS.md` - 工具配置
- `models.json` - 模型配置

### 3. 更新主配置

編輯 `openclaw.json` 添加 agents 和 bindings

### 4. 測試

```bash
openclaw agents list --bindings
openclaw gateway restart
```

---

## 📞 需要我幫你設置嗎？

我可以：
1. ✅ 創建所有 agent 的工作區文件
2. ✅ 配置 openclaw.json
3. ✅ 設置每個 agent 的 SOUL.md 和 AGENTS.md
4. ✅ 測試 sub-agent spawn

**告訴我你想先做什麼！** 🚀
