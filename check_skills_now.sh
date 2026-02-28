#!/bin/bash
# 手動立即檢查技能狀態

echo "🔧 立即技能檢查"
echo "================"

cd /home/node/.openclaw/workspace
python3 skills_check_cron.py

exit $?
