#!/usr/bin/env python3
"""
OpenClaw CLI Starter Template (Python)
版本：1.0
日期：2026-03-04

使用方法:
    python3 cli-starter.py <command> [args]

示例:
    python3 cli-starter.py top
    python3 cli-starter.py search "query"
"""

import sys
import requests
import json

# 配置
BASE_URL = "http://127.0.0.1:18789"  # OpenClaw Gateway
API_KEY = "your-api-key-here"  # 如果需要

def get_top_items(limit=10):
    """獲取熱門項目"""
    response = requests.get(f"{BASE_URL}/api/items/top?limit={limit}")
    return response.json()

def search_items(query):
    """搜尋項目"""
    response = requests.get(f"{BASE_URL}/api/items/search?q={query}")
    return response.json()

def print_table(data):
    """打印表格"""
    if not data:
        print("無數據")
        return
    
    # 打印表頭
    headers = data[0].keys()
    print(" | ".join(headers))
    print("-" * 50)
    
    # 打印數據
    for item in data:
        print(" | ".join(str(item[h]) for h in headers))

def main():
    if len(sys.argv) < 2:
        print("使用方法：python3 cli-starter.py <command> [args]")
        print("可用命令：top, search, help")
        return
    
    command = sys.argv[1]
    
    if command == "top":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        items = get_top_items(limit)
        print_table(items)
    
    elif command == "search":
        query = sys.argv[2] if len(sys.argv) > 2 else ""
        items = search_items(query)
        print_table(items)
    
    elif command == "help":
        print("""
可用命令:
  top [limit]     - 獲取熱門項目
  search <query>  - 搜尋項目
  help            - 顯示幫助
        """)
    
    else:
        print(f"未知命令：{command}")
        print("使用 'help' 查看可用命令")

if __name__ == "__main__":
    main()
