#!/usr/bin/env python3
"""
Anna Archive 快速下載工具（命令行版本）

用法：
    python3 anna_archive_quick.py "搜索關鍵詞" [下載目錄]

示例：
    python3 anna_archive_quick.py "python programming"
    python3 anna_archive_quick.py "machine learning" ./books
"""

import sys
import requests
import json
from pathlib import Path
import hashlib


def search_books(query: str, limit: int = 10):
    """搜索書籍"""
    api_url = "https://annas-archive.org/api/search"
    
    params = {
        "q": query,
        "content_type": "book",
        "limit": limit,
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
    }
    
    try:
        response = requests.get(api_url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        
        results = response.json()
        
        if isinstance(results, dict):
            return results.get("results", [])
        elif isinstance(results, list):
            return results
        else:
            return []
            
    except Exception as e:
        print(f"❌ 搜索失敗：{e}")
        return []


def display_results(results):
    """顯示結果"""
    if not results:
        print("❌ 未找到結果")
        return
    
    print(f"\n📚 找到 {len(results)} 本書籍：\n")
    print("=" * 80)
    
    for i, item in enumerate(results, 1):
        title = item.get("title", "無標題")
        author = item.get("author", "未知作者")
        year = item.get("year", "")
        size = item.get("file_size", 0)
        
        # 格式化大小
        if size:
            if size > 1024 * 1024:
                size_str = f"{size / (1024 * 1024):.1f} MB"
            elif size > 1024:
                size_str = f"{size / 1024:.1f} KB"
            else:
                size_str = f"{size} B"
        else:
            size_str = "未知"
        
        print(f"{i}. {title}")
        print(f"   作者：{author} | 年份：{year} | 大小：{size_str}")
        print(f"   ID: {item.get('id', 'N/A')}")
        print()
    
    print("=" * 80)


def main():
    if len(sys.argv) < 2:
        print("用法：python3 anna_archive_quick.py \"搜索關鍵詞\" [下載目錄]")
        print("\n示例：")
        print("  python3 anna_archive_quick.py \"python programming\"")
        print("  python3 anna_archive_quick.py \"machine learning\" ./books")
        sys.exit(1)
    
    query = sys.argv[1]
    download_dir = sys.argv[2] if len(sys.argv) > 2 else "downloads"
    
    print(f"🔍 搜索：{query}")
    print(f"📁 下載目錄：{download_dir}")
    
    # 創建下載目錄
    Path(download_dir).mkdir(exist_ok=True)
    
    # 搜索
    results = search_books(query, limit=10)
    
    if not results:
        print("❌ 未找到結果")
        sys.exit(1)
    
    # 顯示結果
    display_results(results)
    
    # 選擇下載
    print("\n請輸入要下載的書籍編號（1-10），或輸入 0 退出：")
    choice = input("> ").strip()
    
    if choice == "0":
        print("👋 退出")
        sys.exit(0)
    
    try:
        index = int(choice) - 1
        if 0 <= index < len(results):
            item = results[index]
            item_id = item.get("id")
            
            if item_id:
                print(f"✅ 選擇：{item.get('title', 'Unknown')}")
                print(f"🔗 ID: {item_id}")
                print("\n⚠️  請注意：")
                print("   - 僅用於下載公共領域或開放授權的書籍")
                print("   - 遵守當地法律法規")
                print("   - 僅供個人學習/研究使用")
            else:
                print("❌ 缺少項目 ID")
        else:
            print("❌ 無效的編號")
    except ValueError:
        print("❌ 無效的輸入")


if __name__ == "__main__":
    main()
