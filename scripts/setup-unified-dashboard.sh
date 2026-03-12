#!/bin/bash
# 統一 Dashboard 快速啟動腳本
# 用法：./setup-unified-dashboard.sh

set -e

echo "🦞 OpenClaw Unified Dashboard Setup"
echo "===================================="

# Step 1: Create Next.js project
echo "📦 Step 1: Creating Next.js project..."
npx create-next-app@latest openclaw-unified-dashboard --typescript --tailwind --app --no-src-dir --import-alias "@/*"
cd openclaw-unified-dashboard

# Step 2: Install dependencies
echo "📦 Step 2: Installing dependencies..."
npm install next-auth @auth/supabase-adapter @supabase/supabase-js
npm install tailwindcss postcss autoprefixer

# Step 3: Copy Kanban Board
echo "📋 Step 3: Copying Kanban Board..."
mkdir -p app/kanban
# TODO: Copy and adapt Kanban code

# Step 4: Copy Bot Review
echo "🤖 Step 4: Copying Bot Review..."
mkdir -p app/bot-review
# TODO: Copy and adapt Bot Review code

# Step 5: Setup environment
echo "🔐 Step 5: Setting up environment..."
cp .env.example .env.local
echo "請編輯 .env.local 並填寫以下環境變數："
echo "  - GOOGLE_CLIENT_ID"
echo "  - GOOGLE_CLIENT_SECRET"
echo "  - SUPABASE_URL"
echo "  - SUPABASE_ANON_KEY"
echo "  - SUPABASE_SECRET"

# Step 6: Git setup
echo "📦 Step 6: Setting up Git..."
git init
git add .
git commit -m "Initial commit: Unified Dashboard setup"

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env.local with your credentials"
echo "2. Run: npm run dev"
echo "3. Open: http://localhost:3000"
echo ""
