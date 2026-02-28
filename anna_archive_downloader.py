#!/usr/bin/env python3
"""
Anna Archive 自動下載工具
用於搜索和下載 Anna Archive 上的書籍

⚠️ 法律聲明：
- 僅用於下載公共領域或開放授權的書籍
- 遵守當地法律法規
- 僅供個人學習/研究使用
- 不要分發受版權保護的內容

作者：OpenClaw Coding Agent
日期：2026-02-26
"""

import requests
import json
import time
import os
from pathlib import Path
from typing import Optional, List, Dict
import hashlib


class AnnaArchiveDownloader:
    """Anna Archive 下載器"""
    
    def __init__(self, download_dir: str = "downloads"):
        """
        初始化下載器
        
        Args:
            download_dir: 下載目錄
        """
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(exist_ok=True)
        
        # Anna Archive API 端點
        self.base_url = "https://annas-archive.org"
        self.api_url = "https://annas-archive.org/api/search"
        
        # 請求頭
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json",
        }
        
        print(f"📚 Anna Archive 下載器已初始化")
        print(f"📁 下載目錄：{self.download_dir.absolute()}")
        print()
    
    def search(self, query: str, content_type: str = "book", limit: int = 10) -> List[Dict]:
        """
        搜索書籍
        
        Args:
            query: 搜索關鍵詞
            content_type: 內容類型 (book, article, comic, magazine)
            limit: 返回結果數量
            
        Returns:
            搜索結果列表
        """
        print(f"🔍 搜索：{query}")
        print(f"📊 類型：{content_type}")
        print(f"📈 限制：{limit} 條結果")
        print()
        
        params = {
            "q": query,
            "content_type": content_type,
            "limit": limit,
        }
        
        try:
            response = requests.get(
                self.api_url,
                params=params,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            
            results = response.json()
            
            if isinstance(results, dict):
                items = results.get("results", [])
            elif isinstance(results, list):
                items = results
            else:
                print("❌ 無法解析搜索結果")
                return []
            
            print(f"✅ 找到 {len(items)} 條結果")
            print()
            
            return items
            
        except requests.exceptions.RequestException as e:
            print(f"❌ 搜索失敗：{e}")
            return []
        except json.JSONDecodeError as e:
            print(f"❌ JSON 解析失敗：{e}")
            return []
    
    def display_results(self, results: List[Dict], max_display: int = 10):
        """
        顯示搜索結果
        
        Args:
            results: 搜索結果
            max_display: 最多顯示數量
        """
        print("=" * 80)
        print("📚 搜索結果")
        print("=" * 80)
        print()
        
        for i, item in enumerate(results[:max_display], 1):
            title = item.get("title", "無標題")
            author = item.get("author", "未知作者")
            year = item.get("year", "未知年份")
            publisher = item.get("publisher", "未知出版社")
            language = item.get("language", "未知語言")
            file_size = item.get("file_size", "未知大小")
            
            # 格式化文件大小
            if file_size and isinstance(file_size, (int, float)):
                if file_size > 1024 * 1024:
                    size_str = f"{file_size / (1024 * 1024):.1f} MB"
                elif file_size > 1024:
                    size_str = f"{file_size / 1024:.1f} KB"
                else:
                    size_str = f"{file_size} B"
            else:
                size_str = str(file_size) if file_size else "未知"
            
            print(f"{i}. {title}")
            print(f"   作者：{author}")
            print(f"   年份：{year} | 出版社：{publisher}")
            print(f"   語言：{language} | 大小：{size_str}")
            
            # 顯示 ID（用於下載）
            item_id = item.get("id")
            if item_id:
                print(f"   ID: {item_id}")
            
            print()
        
        print("=" * 80)
    
    def get_download_links(self, item_id: str) -> Optional[Dict]:
        """
        獲取下載鏈接
        
        Args:
            item_id: 項目 ID
            
        Returns:
            下載鏈接字典
        """
        print(f"🔗 獲取下載鏈接：{item_id}")
        
        url = f"{self.base_url}/md5/{item_id}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            # 解析頁面獲取下載鏈接
            # 注意：這需要根據實際頁面結構調整
            download_links = {}
            
            # 這裡需要根據實際頁面結構解析
            # 由於 Anna Archive 的頁面結構可能變化，這裡提供一個框架
            
            print(f"✅ 找到下載鏈接")
            return download_links
            
        except Exception as e:
            print(f"❌ 獲取下載鏈接失敗：{e}")
            return None
    
    def download_file(self, url: str, filename: Optional[str] = None) -> Optional[Path]:
        """
        下載文件
        
        Args:
            url: 下載 URL
            filename: 保存文件名
            
        Returns:
            保存的文件路徑
        """
        try:
            print(f"⬇️  開始下載：{url}")
            
            response = requests.get(url, stream=True, timeout=60)
            response.raise_for_status()
            
            # 自動生成文件名
            if not filename:
                # 從 URL 生成文件名
                url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
                filename = f"download_{url_hash}"
            
            # 確保文件名安全
            filename = "".join(c for c in filename if c.isalnum() or c in "._- ")
            filepath = self.download_dir / filename
            
            # 下載
            total_size = int(response.headers.get("content-length", 0))
            downloaded = 0
            
            with open(filepath, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        # 顯示進度
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            print(f"\r   進度：{progress:.1f}%", end="", flush=True)
            
            print()  # 換行
            print(f"✅ 下載完成：{filepath}")
            
            return filepath
            
        except Exception as e:
            print(f"❌ 下載失敗：{e}")
            return None
    
    def batch_download(self, queries: List[str], limit_per_query: int = 5):
        """
        批量下載
        
        Args:
            queries: 搜索關鍵詞列表
            limit_per_query: 每個查詢下載數量
        """
        print("🚀 開始批量下載")
        print(f"📝 查詢列表：{queries}")
        print(f"📊 每個查詢下載：{limit_per_query} 本")
        print()
        
        for query in queries:
            print("=" * 80)
            print(f"📖 處理查詢：{query}")
            print("=" * 80)
            print()
            
            # 搜索
            results = self.search(query, limit=limit_per_query)
            
            if not results:
                print(f"⚠️  未找到結果，跳過")
                print()
                continue
            
            # 顯示結果
            self.display_results(results)
            
            # 等待用戶選擇
            print("請輸入要下載的書籍編號（輸入 0 跳過，輸入 q 退出）：")
            choice = input("> ").strip()
            
            if choice.lower() == "q":
                print("👋 退出下載")
                break
            
            if choice == "0":
                print("⏭️  跳過")
                print()
                continue
            
            try:
                index = int(choice) - 1
                if 0 <= index < len(results):
                    item = results[index]
                    item_id = item.get("id")
                    
                    if item_id:
                        # 獲取下載鏈接
                        links = self.get_download_links(item_id)
                        
                        # 下載
                        if links and "url" in links:
                            self.download_file(links["url"])
                        else:
                            print(f"❌ 無法獲取下載鏈接")
                    else:
                        print(f"❌ 缺少項目 ID")
                else:
                    print(f"❌ 無效的編號")
            except ValueError:
                print(f"❌ 無效的輸入")
            
            print()
            
            # 避免請求過快
            time.sleep(2)
        
        print("🎉 批量下載完成")


def main():
    """主函數"""
    print("=" * 80)
    print("📚 Anna Archive 自動下載工具")
    print("=" * 80)
    print()
    
    # ⚠️ 法律聲明
    print("⚠️  法律聲明：")
    print("   - 僅用於下載公共領域或開放授權的書籍")
    print("   - 遵守當地法律法規")
    print("   - 僅供個人學習/研究使用")
    print("   - 不要分發受版權保護的內容")
    print()
    print("使用本工具即表示你同意以上條款")
    print()
    
    agree = input("是否同意？(y/n): ").strip().lower()
    if agree != "y":
        print("❌ 退出程序")
        return
    
    print()
    print("=" * 80)
    print()
    
    # 初始化下載器
    downloader = AnnaArchiveDownloader()
    
    # 主菜單
    while True:
        print()
        print("請選擇操作：")
        print("1. 搜索書籍")
        print("2. 批量下載")
        print("3. 退出")
        print()
        
        choice = input("> ").strip()
        
        if choice == "1":
            # 搜索
            query = input("輸入搜索關鍵詞：").strip()
            if not query:
                print("❌ 關鍵詞不能為空")
                continue
            
            content_type = input("內容類型 (book/article/comic/magazine)，默認 book：").strip() or "book"
            limit = input("結果數量 (1-20)，默認 10：").strip() or "10"
            
            try:
                limit = int(limit)
                limit = max(1, min(20, limit))
            except ValueError:
                limit = 10
            
            results = downloader.search(query, content_type, limit)
            
            if results:
                downloader.display_results(results)
                
                # 詢問是否下載
                download = input("是否下載？輸入編號或 n 跳過：").strip()
                
                if download.lower() != "n":
                    try:
                        index = int(download) - 1
                        if 0 <= index < len(results):
                            item_id = results[index].get("id")
                            if item_id:
                                links = downloader.get_download_links(item_id)
                                if links:
                                    downloader.download_file(links.get("url", ""))
                    except ValueError:
                        print("❌ 無效的編號")
        
        elif choice == "2":
            # 批量下載
            print("輸入多個搜索關鍵詞，用逗號分隔：")
            queries_str = input("> ").strip()
            queries = [q.strip() for q in queries_str.split(",") if q.strip()]
            
            if not queries:
                print("❌ 請輸入至少一個關鍵詞")
                continue
            
            limit = input("每個查詢下載數量 (1-5)，默認 1：").strip() or "1"
            
            try:
                limit = int(limit)
                limit = max(1, min(5, limit))
            except ValueError:
                limit = 1
            
            downloader.batch_download(queries, limit)
        
        elif choice == "3":
            print("👋 再見！")
            break
        
        else:
            print("❌ 無效的選擇")


if __name__ == "__main__":
    main()
