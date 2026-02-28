#!/bin/bash

# 🚀 快速部署腳本 - Gameworld + Kanban
# 用法：./deploy.sh [gameworld|kanban|all]

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}=====================================${NC}"
echo -e "${GREEN}🚀 快速部署腳本${NC}"
echo -e "${GREEN}=====================================${NC}"

# 檢查參數
DEPLOY_TARGET="${1:-all}"

# 函數：檢查 Git 狀態
check_git_status() {
    echo -e "${YELLOW}📊 檢查 Git 狀態...${NC}"
    cd /home/node/.openclaw/workspace
    
    if git diff --quiet && git diff --cached --quiet; then
        echo -e "${GREEN}✅ Git working tree clean${NC}"
    else
        echo -e "${YELLOW}⚠️  有未 commit 的更改，正在 commit...${NC}"
        git add -A
        git commit -m "💾 Auto-commit before deployment"
        git push origin main
    fi
}

# 函數：部署 Gameworld
deploy_gameworld() {
    echo -e "${YELLOW}=====================================${NC}"
    echo -e "${YELLOW}🎮 部署 Gameworld...${NC}"
    echo -e "${YELLOW}=====================================${NC}"
    
    echo -e "${GREEN}✅ 步驟 1/4:${NC} 檢查文件結構"
    if [ -d "games/2048-game" ]; then
        echo "   ✅ games/2048-game 存在"
    else
        echo -e "${RED}❌ games/2048-game 不存在！${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ 步驟 2/4:${NC} Push 到 GitHub"
    git push origin main
    
    echo -e "${GREEN}✅ 步驟 3/4:${NC} 觸發 GitHub Actions"
    echo "   🔄 GitHub Actions 會自動部署到 Zeabur"
    
    echo -e "${GREEN}✅ 步驟 4/4:${NC} 完成！"
    echo ""
    echo -e "${GREEN}🌐 Gameworld URL: https://gameworld.zeabur.app${NC}"
    echo ""
}

# 函數：部署 Kanban
deploy_kanban() {
    echo -e "${YELLOW}=====================================${NC}"
    echo -e "${YELLOW}📊 部署 Kanban Board...${NC}"
    echo -e "${YELLOW}=====================================${NC}"
    
    echo -e "${GREEN}✅ 步驟 1/4:${NC} 檢查文件結構"
    if [ -d "kanban-zeabur" ]; then
        echo "   ✅ kanban-zeabur 存在"
    else
        echo -e "${RED}❌ kanban-zeabur 不存在！${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ 步驟 2/4:${NC} 檢查環境變量"
    if [ -f "kanban-zeabur/.env" ]; then
        echo "   ✅ .env 文件存在"
    else
        echo -e "${YELLOW}⚠️  .env 文件不存在，請確保 Zeabur 已配置環境變量${NC}"
    fi
    
    echo -e "${GREEN}✅ 步驟 3/4:${NC} Push 到 GitHub"
    git push origin main
    
    echo -e "${GREEN}✅ 步驟 4/4:${NC} 觸發 GitHub Actions"
    echo "   🔄 GitHub Actions 會自動部署到 Zeabur"
    
    echo ""
    echo -e "${GREEN}🌐 Kanban URL: https://kanban.zeabur.app${NC}"
    echo ""
}

# 主邏輯
case "$DEPLOY_TARGET" in
    gameworld)
        check_git_status
        deploy_gameworld
        ;;
    kanban)
        check_git_status
        deploy_kanban
        ;;
    all)
        check_git_status
        deploy_gameworld
        deploy_kanban
        ;;
    *)
        echo -e "${RED}用法：$0 [gameworld|kanban|all]${NC}"
        echo ""
        echo "Examples:"
        echo "  $0 gameworld   # 只部署 Gameworld"
        echo "  $0 kanban      # 只部署 Kanban"
        echo "  $0 all         # 部署所有 (默認)"
        exit 1
        ;;
esac

echo -e "${GREEN}=====================================${NC}"
echo -e "${GREEN}✅ 部署完成！${NC}"
echo -e "${GREEN}=====================================${NC}"
echo ""
echo -e "${YELLOW}📊 檢查部署狀態:${NC}"
echo "   GitHub Actions: https://github.com/raycoderhk/2048-game/actions"
echo "   Zeabur Dashboard: https://zeabur.com/dashboard"
echo ""
echo -e "${YELLOW}🎮 測試連結:${NC}"
echo "   Gameworld: https://gameworld.zeabur.app"
echo "   Kanban: https://kanban.zeabur.app"
echo ""
echo -e "${YELLOW}⏱️  部署需時：2-5 分鐘${NC}"
echo ""
