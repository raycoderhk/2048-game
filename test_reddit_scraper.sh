#!/bin/bash
# 測試Reddit抓取器

echo "🧪 測試Reddit抓取器"
echo "=================="

WORKSPACE="/home/node/.openclaw/workspace"
SCRAPER_DIR="$WORKSPACE/skills/reddit_scraper"

cd "$SCRAPER_DIR"

echo "1. 測試幫助信息..."
python3 simple_reddit_scraper.py --help

echo ""
echo "2. 測試簡單Reddit帖子..."
# 使用一個已知的Reddit帖子進行測試
TEST_URL="https://www.reddit.com/r/OpenClawUseCases/comments/1rbmrup/11_openclaw_hacks_that_completely_changed_how_i/"

echo "測試URL: $TEST_URL"
echo ""

# 嘗試獲取內容
echo "嘗試獲取Reddit內容..."
python3 simple_reddit_scraper.py "$TEST_URL" markdown 2>&1 | head -50

echo ""
echo "3. 測試JSON輸出..."
python3 simple_reddit_scraper.py "$TEST_URL" json 2>&1 | head -30

echo ""
echo "📊 測試完成"
echo "💡 如果遇到403錯誤，可能是由於Reddit的安全限制"
echo "🔧 可能的解決方案:"
echo "   - 使用不同的用戶代理"
echo "   - 添加延遲避免速率限制"
echo "   - 使用Reddit官方API (需要API憑證)"
echo "   - 使用緩存減少請求"