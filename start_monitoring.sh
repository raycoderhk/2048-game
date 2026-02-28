#!/bin/bash
# 啟動技能監控

echo "啟動技能監控系統..."

# 運行每日檢查
/home/node/.openclaw/workspace/check_skills_daily.sh

# 設置定時任務（使用簡單的 sleep 循環）
while true; do
    # 每小時運行簡化檢查
    /home/node/.openclaw/workspace/check_skills_hourly.sh
    
    # 等待1小時
    sleep 3600
done
