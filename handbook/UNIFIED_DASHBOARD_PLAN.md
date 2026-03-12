# 🦞 Kanban + Bot Review Dashboard 整合方案

**目標：** 將 OpenClaw-bot-review 整合到 Kanban Board，共享 OAuth + 統一界面

---

## 📋 整合計劃

### 階段 1: 項目合併 (1-2 小時)

### 階段 2: OAuth 共享 (30 分鐘)

### 階段 3: UI 整合 (1 小時)

### 階段 4: 部署測試 (30 分鐘)

---

## 🏗️ 技術架構

### 當前狀態

| 項目 | 技術棧 | OAuth | 部署 |
|------|--------|-------|------|
| **Kanban Board** | Vanilla HTML/JS + Supabase | Google OAuth | Zeabur |
| **Bot Review** | Next.js 16 + TS | 無 | 本地 |

### 目標狀態

| 特性 | 方案 |
|------|------|
| **框架** | Next.js 16 (統一) |
| **OAuth** | Google OAuth (共享) |
| **數據庫** | Supabase (共享) |
| **部署** | Zeabur (單一服務) |
| **路由** | `/kanban` + `/bot-review` |

---

## 📁 新項目結構

```
openclaw-unified-dashboard/
├── app/
│   ├── layout.tsx          # 根佈局 (共享 OAuth)
│   ├── page.tsx            # 首頁 (導航)
│   ├── kanban/             # Kanban Board
│   │   ├── page.tsx
│   │   └── ...
│   ├── bot-review/         # Bot Review Dashboard
│   │   ├── page.tsx
│   │   ├── api/
│   │   └── ...
│   └── api/
│       ├── auth/           # 共享認證
│       └── ...
├── lib/
│   ├── supabase.ts         # 共享 Supabase 客戶端
│   ├── auth.ts             # 共享 OAuth 邏輯
│   └── ...
├── components/
│   ├── sidebar.tsx         # 共享側邊欄
│   ├── tab-nav.tsx         # Tab 導航
│   └── ...
├── package.json
└── .env.local
```

---

## 🔐 OAuth 共享方案

### 當前問題

- Kanban 有 Google OAuth
- Bot Review 無認證
- 用戶需要登入兩次

### 解決方案

```typescript
// lib/auth.ts
import { NextAuthOptions } from 'next-auth'
import GoogleProvider from 'next-auth/providers/google'
import { SupabaseAdapter } from '@auth/supabase-adapter'

export const authOptions: NextAuthOptions = {
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
  ],
  adapter: SupabaseAdapter({
    url: process.env.SUPABASE_URL!,
    secret: process.env.SUPABASE_SECRET!,
  }),
  session: {
    strategy: 'jwt',
  },
  callbacks: {
    async session({ session, token }) {
      // 共享會話到兩個 Dashboard
      return session
    },
  },
}
```

### 使用方式

```typescript
// 兩個 Dashboard 都用同一個 Hook
import { useSession } from 'next-auth/react'

function Dashboard() {
  const { data: session } = useSession()
  
  if (!session) {
    // 跳轉到登入頁面 (共享)
    return <SignIn />
  }
  
  return <DashboardContent />
}
```

---

## 🎨 UI 整合方案

### Tab 導航組件

```typescript
// components/tab-nav.tsx
'use client'

import { usePathname } from 'next/navigation'
import Link from 'next/link'

export function TabNav() {
  const pathname = usePathname()
  
  return (
    <nav className="flex border-b">
      <Link
        href="/kanban"
        className={`px-4 py-2 ${
          pathname === '/kanban'
            ? 'border-b-2 border-blue-500 text-blue-500'
            : 'text-gray-500'
        }`}
      >
        📋 Kanban Board
      </Link>
      <Link
        href="/bot-review"
        className={`px-4 py-2 ${
          pathname === '/bot-review'
            ? 'border-b-2 border-purple-500 text-purple-500'
            : 'text-gray-500'
        }`}
      >
        🤖 Bot Monitor
      </Link>
      <Link
        href="/settings"
        className={`px-4 py-2 ${
          pathname === '/settings'
            ? 'border-b-2 border-gray-500 text-gray-500'
            : 'text-gray-500'
        }`}
      >
        ⚙️ Settings
      </Link>
    </nav>
  )
}
```

---

## 🚀 遷移步驟

### Phase 1: 創建統一項目

```bash
# 1. 創建新項目
npx create-next-app@latest openclaw-unified-dashboard
cd openclaw-unified-dashboard

# 2. 安裝依賴
npm install next-auth @auth/supabase-adapter @supabase/supabase-js
npm install tailwindcss postcss autoprefixer

# 3. 配置環境變數
cp .env.example .env.local
# 編輯 .env.local:
# - GOOGLE_CLIENT_ID
# - GOOGLE_CLIENT_SECRET
# - SUPABASE_URL
# - SUPABASE_ANON_KEY
```

---

### Phase 2: 遷移 Kanban Board

```bash
# 1. 複製 Kanban 代碼
cp -r ../kanban-board/app/* ./app/kanban/

# 2. 適配 Next.js
# - 改 HTML 為 TSX
# - 改 CommonJS 為 ESM
# - 添加 TypeScript 類型

# 3. 測試
npm run dev
# 訪問 http://localhost:3000/kanban
```

---

### Phase 3: 遷移 Bot Review

```bash
# 1. 複製 Bot Review 代碼
cp -r ../OpenClaw-bot-review/app/* ./app/bot-review/

# 2. 整合 OAuth
# - 添加 useSession Hook
# - 共享認證狀態

# 3. 測試
npm run dev
# 訪問 http://localhost:3000/bot-review
```

---

### Phase 4: 整合 OAuth

```bash
# 1. 配置 NextAuth
# lib/auth.ts (見上面)

# 2. 添加 API Route
# app/api/auth/[...nextauth]/route.ts

# 3. 添加登入頁面
# app/login/page.tsx

# 4. 測試登入流程
# - 登入一次
# - 訪問 /kanban (自動通過)
# - 訪問 /bot-review (自動通過)
```

---

### Phase 5: 部署到 Zeabur

```bash
# 1. 推送到 GitHub
git init
git add .
git commit -m "Unified Dashboard: Kanban + Bot Review"
git push origin main

# 2. Zeabur 部署
# - 連接 GitHub Repo
# - 添加環境變數
# - 部署

# 3. 測試生產環境
# https://openclaw-dashboard.zeabur.app
```

---

## 📊 數據共享方案

### Supabase Schema

```sql
-- 共享用戶表
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email TEXT UNIQUE,
  name TEXT,
  avatar_url TEXT,
  created_at TIMESTAMPTZ
);

-- Kanban 項目表
CREATE TABLE kanban_projects (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  title TEXT,
  status TEXT,
  priority TEXT,
  created_at DATE
);

-- Bot 會話表
CREATE TABLE bot_sessions (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  agent_id TEXT,
  token_usage INTEGER,
  created_at TIMESTAMPTZ
);
```

### 共享數據客戶端

```typescript
// lib/supabase.ts
import { createClient } from '@supabase/supabase-js'

export const supabase = createClient(
  process.env.SUPABASE_URL!,
  process.env.SUPABASE_ANON_KEY!
)

// 兩個 Dashboard 都用同一個客戶端
```

---

## 🎯 成功標準

| 標準 | 當前 | 目標 |
|------|------|------|
| **登入次數** | 2 次 (每個 Dashboard 一次) | 1 次 (共享) |
| **部署服務** | 2 個 (Kanban + Bot Review) | 1 個 (統一) |
| **域名** | 2 個 | 1 個 |
| **OAuth 配置** | 2 套 | 1 套 |
| **用戶體驗** | 割裂 | 統一 |

---

## ⏱️ 時間估算

| 任務 | 預計時間 |
|------|---------|
| 項目合併 | 1-2 小時 |
| OAuth 整合 | 30 分鐘 |
| UI 整合 | 1 小時 |
| 測試修復 | 30 分鐘 |
| 部署配置 | 30 分鐘 |
| **總計** | **3.5-4.5 小時** |

---

## 🚨 潛在問題

### 問題 1: Next.js vs Vanilla JS

**當前 Kanban:** Vanilla HTML/JS  
**Bot Review:** Next.js 16

**解決方案:**
- 選項 A: 將 Kanban 遷移到 Next.js (推薦)
- 選項 B: 用 iframe 嵌入 (快速但有局限)

---

### 問題 2: Supabase Schema 衝突

**風險:** 兩個項目可能有不同嘅表結構

**解決方案:**
- 添加前綴 (kanban_*, bot_*)
- 或者統一命名

---

### 問題 3: 樣式衝突

**風險:** Tailwind 類名衝突

**解決方案:**
- 使用 CSS Modules
- 或者添加前綴

---

## 💡 未來擴展

### 添加更多 Tab

```
[Tab 1: Kanban]
[Tab 2: Bot Monitor]
[Tab 3: Mission Control]
[Tab 4: Nutrition App]
[Tab 5: Settings]
```

### 統一通知中心

```
所有應用嘅通知集中到一個地方：
- Kanban: 任務更新
- Bot Monitor: Agent 告警
- Mission Control: 事件提醒
```

### 統一設置頁面

```
- Google OAuth 配置
- Supabase 配置
- 主題設置
- 通知偏好
```

---

## 📝 下一步行動

### 立即行動

1. **確認方案**
   - 用戶同意整合方向
   - 選擇技術方案 (Next.js 統一)

2. **創建 Repo**
   ```bash
   npx create-next-app@latest openclaw-unified-dashboard
   ```

3. **開始遷移**
   - 先遷移 Kanban (簡單)
   - 再遷移 Bot Review (複雜)

### 本週完成

- [ ] 項目合併
- [ ] OAuth 整合
- [ ] UI 整合
- [ ] 部署測試

---

**Ready to start?** 🦞🚀
