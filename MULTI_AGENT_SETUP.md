# 🤖 Multi-Agent Team 使用指南

*最後更新：2026-02-26*

---

## ✅ 已完成的配置

### Agent 團隊架構

```
┌─────────────────────────────────────────────────────┐
│              🧠 Jarvis (主 Agent - main)            │
│         模型：aliyun/qwen3.5-plus (包月)            │
└─────────────────────────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          │               │               │
          ▼               ▼               ▼
    ┌──────────┐   ┌──────────┐   ┌──────────┐
    │  Coding  │   │ Research │   │  Admin   │
    │  Agent   │   │  Agent   │   │  Agent   │
    └──────────┘   └──────────┘   └──────────┘
   qwen3-coder    qwen3.5-plus    qwen-turbo
```

### 已創建的文件

**主配置：**
- ✅ `/home/node/.openclaw/openclaw.json` - 多 agent 配置

**Coding Agent：**
- ✅ `~/.openclaw/agents/coding/workspace/SOUL.md`
- ✅ `~/.openclaw/agents/coding/workspace/AGENTS.md`
- ✅ `~/.openclaw/agents/coding/agent/models.json`

**Research Agent：**
- ✅ `~/.openclaw/agents/research/workspace/SOUL.md`
- ✅ `~/.openclaw/agents/research/workspace/AGENTS.md`
- ✅ `~/.openclaw/agents/research/agent/models.json`

**Admin Agent：**
- ✅ `~/.openclaw/agents/admin/workspace/SOUL.md`
- ✅ `~/.openclaw/agents/admin/workspace/AGENTS.md`
- ✅ `~/.openclaw/agents/admin/agent/models.json`

**文檔：**
- ✅ `AGENT_TEAM_ARCHITECTURE.md` - 架構設計文檔
- ✅ `MULTI_AGENT_SETUP.md` - 本使用指南

---

## 🚀 啟動 Multi-Agent 系統

### 1️⃣ 驗證配置

```bash
# 檢查 agents 配置
openclaw agents list --bindings

# 檢查 gateway 狀態
openclaw gateway status

# 如有問題，查看日誌
openclaw logs --tail 50
```

### 2️⃣ 重啟 Gateway

```bash
# 重啟 gateway 使配置生效
openclaw gateway restart

# 等待 10-15 秒啟動完成
sleep 15

# 再次檢查狀態
openclaw status
```

### 3️⃣ 測試 Sub-agent Spawn

告訴我：
> "測試 spawn coding agent"

我會嘗試 spawn 一個 sub-agent 來測試配置。

---

## 💬 如何使用 Agent 團隊

### 直接與主 Agent 溝通（推薦）

**你只需要與 Jarvis（主 agent）對話**，我會自動分發任務：

```
用戶 → Jarvis → [自動分析並 spawn 合適的 sub-agent] → 整合結果 → 用戶
```

### 示例場景

#### 場景 1：編碼任務

**你說：** "幫我寫一個 Python 腳本來爬取天氣數據"

**Jarvis 處理：**
1. 分析任務 → 需要編碼
2. Spawn `coding` sub-agent
3. 等待 coding agent 完成
4. 整合結果回覆你

#### 場景 2：研究任務

**你說：** "幫我研究阿里雲 Coding Plan 和 DeepSeek 的對比"

**Jarvis 處理：**
1. 分析任務 → 需要研究
2. Spawn `research` sub-agent
3. Research agent 進行 web_search
4. 整合報告回覆你

#### 場景 3：日程管理

**你說：** "提醒我明天的匹克球活動"

**Jarvis 處理：**
1. 分析任務 → 日程管理
2. 檢查 HEARTBEAT.md
3. 設置提醒
4. 確認已設置

#### 場景 4：複雜任務（多 sub-agents）

**你說：** "幫我創建一個完整的股票分析系統"

**Jarvis 處理：**
1. 分析任務 → 複雜、多步驟
2. Spawn `coding` agent 作為 orchestrator
3. Coding agent 再 spawn 多個 worker sub-agents：
   - Worker 1: 數據爬取
   - Worker 2: 數據分析
   - Worker 3: 可視化
4. 整合所有結果回覆你

---

## 🎯 Sub-agent 配置說明

### Max Spawn Depth = 2

允許兩層 sub-agent 結構：

```
Main (Jarvis)
  └─→ Sub-agent Depth 1 (e.g., Coding Agent as orchestrator)
        └─→ Sub-agent Depth 2 (e.g., Worker agents)
```

**Depth 1 (Orchestrator):**
- 可以 spawn 子 agent
- 有 `sessions_spawn`、`subagents` 工具權限
- 可以管理子 agent

**Depth 2 (Worker):**
- 不能 spawn 子 agent
- 專注於具體任務
- 完成後向 parent 報告

### 成本優化

所有 sub-agents 使用 `aliyun/qwen-turbo`（便宜、快速）：

```json5
{
  "agents": {
    "defaults": {
      "subagents": {
        "model": "aliyun/qwen-turbo"  // sub-agents 用便宜模型
      }
    }
  }
}
```

**好處：**
- 主 agent 用高質量模型（qwen3.5-plus）
- sub-agents 用經濟模型（qwen-turbo）
- 全部在 Coding Plan 包月內，無額外費用 ✅

---

## 📊 監控和管理 Sub-agents

### 查看 Sub-agents

```bash
# 列出所有 sub-agents
/subagents list

# 查看特定 sub-agent 信息
/subagents info <id>

# 查看日誌
/subagents log <id>
```

### 控制 Sub-agents

```bash
# 停止特定 sub-agent
/subagents kill <id>

# 停止所有 sub-agents
/subagents kill all

# 發送消息給 sub-agent
/subagents send <id> <message>

# 指導 sub-agent
/subagents steer <id> <message>
```

### 手動 Spawn Sub-agent

```bash
# 手動 spawn sub-agent
/subagents spawn coding "創建一個 Python 腳本"

# 指定模型
/subagents spawn coding "任務" --model aliyun/qwen3-coder-plus

# 指定思考級別
/subagents spawn coding "任務" --thinking high
```

---

## 🔧 故障排除

### 問題 1：Sub-agent Spawn 失敗

**症狀：** 錯誤信息 "subagents not allowed" 或 "tool denied"

**解決：**
1. 檢查 `openclaw.json` 中 `subagents.allowAgents` 配置
2. 確認 sub-agent 配置正確
3. 重啟 gateway

### 問題 2：Agent 未響應

**症狀：** Sub-agent spawn 後無響應

**解決：**
```bash
# 檢查 sub-agent 狀態
/subagents list

# 查看日誌
/subagents log <id>

# 如卡住，停止並重試
/subagents kill <id>
```

### 問題 3：配置不生效

**症狀：** 修改 openclaw.json 後無變化

**解決：**
```bash
# 完全重啟 gateway
openclaw gateway stop
sleep 5
openclaw gateway start

# 驗證配置
openclaw agents list --bindings
```

---

## 💡 最佳實踐

### 1. 任務分發策略

**簡單任務：** Jarvis 直接處理
- 日程查詢
- 簡單問答
- 文件操作

**中等任務：** Spawn 單一 sub-agent
- 編寫腳本
- 研究分析
- 數據整理

**複雜任務：** Spawn orchestrator + workers
- 完整系統開發
- 多模塊項目
- 大型研究報告

### 2. 成本優化

- 主 agent：高質量模型（qwen3.5-plus）
- Sub-agents：經濟模型（qwen-turbo）
- 編碼任務：專用模型（qwen3-coder-plus）

### 3. 並行控制

- `maxConcurrent: 8` - 同時最多 8 個 sub-agents
- `maxChildrenPerAgent: 5` - 每個 agent 最多 5 個子 agent
- 避免同時 spawn 過多 sub-agents

### 4. 清理策略

- `archiveAfterMinutes: 60` - 60 分鐘後自動歸檔
- 定期清理舊的 sub-agent sessions
- 保持系統整潔

---

## 📈 性能監控

### 查看 Token 使用

```bash
# 查看會話狀態（包括 token 使用）
openclaw status
```

### 查看 Sub-agent 統計

```bash
# 列出 sub-agents 及其狀態
/subagents list

# 查看詳細信息（包括 token 使用）
/subagents info <id>
```

### 成本估算

所有 agent 都使用阿里雲 Coding Plan：

| Agent | 模型 | 使用場景 | 成本 |
|-------|------|----------|------|
| Jarvis | qwen3.5-plus | 主對話、決策 | 包月 |
| Coding | qwen3-coder-plus | 編碼任務 | 包月 |
| Research | qwen3.5-plus | 研究分析 | 包月 |
| Admin | qwen-turbo | 日程、監控 | 包月 |
| Sub-agents | qwen-turbo | worker 任務 | 包月 |

**全部在包月額度內，無額外費用！** ✅

---

## 🎯 下一步

### 立即測試

告訴我：
> "測試 spawn 一個 sub-agent"

我會嘗試 spawn 一個 coding sub-agent 來驗證配置。

### 實際使用

開始使用 agent 團隊：
1. **編碼任務** - "幫我寫一個 Python 腳本"
2. **研究任務** - "幫我研究..."
3. **日程管理** - "提醒我..."

### 持續優化

根據使用情況調整：
- 添加更多專門 agent
- 調整模型配置
- 優化 sub-agent 策略

---

## 📞 需要幫助？

隨時告訴我：
- "如何 spawn sub-agent？"
- "查看 sub-agent 狀態"
- "停止所有 sub-agents"
- "優化 agent 配置"

---

**你的 Agent 團隊已準備就緒！** 🎉
