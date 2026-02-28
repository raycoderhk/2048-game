# 📚 Anna Archive 自動下載工具

*創建日期：2026-02-26*
*作者：OpenClaw Coding Agent*

---

## ⚠️ 重要法律聲明

**使用本工具前請務必閱讀：**

- ✅ **僅用於**下載公共領域或開放授權的書籍
- ✅ **遵守**你所在地區的法律法規
- ✅ **僅供**個人學習/研究使用
- ❌ **不要**分發受版權保護的內容
- ❌ **不要**用於商業目的

**使用本工具即表示你同意以上條款。**

---

## 🚀 快速開始

### 1️⃣ 安裝依賴

```bash
pip install requests
```

### 2️⃣ 運行程序

```bash
python3 anna_archive_downloader.py
```

### 3️⃣ 按照提示操作

程序會引導你：
1. 同意法律聲明
2. 選擇操作（搜索/批量下載）
3. 輸入搜索關鍵詞
4. 選擇要下載的書籍

---

## 📋 功能特點

### ✅ 已實現功能

| 功能 | 說明 |
|------|------|
| **搜索書籍** | 支持關鍵詞搜索 |
| **內容類型** | book/article/comic/magazine |
| **結果顯示** | 顯示書名、作者、年份、大小等 |
| **單本下載** | 選擇單本書下載 |
| **批量下載** | 批量搜索和下載 |
| **進度顯示** | 顯示下載進度 |
| **法律聲明** | 使用前需同意條款 |

### 🔧 配置選項

```python
# 自定義下載目錄
downloader = AnnaArchiveDownloader(download_dir="my_books")

# 搜索參數
results = downloader.search(
    query="python programming",
    content_type="book",
    limit=10
)
```

---

## 💡 使用示例

### 示例 1：搜索書籍

```python
from anna_archive_downloader import AnnaArchiveDownloader

downloader = AnnaArchiveDownloader()

# 搜索 Python 編程書籍
results = downloader.search("python programming", limit=10)

# 顯示結果
downloader.display_results(results)
```

### 示例 2：批量下載

```python
# 批量下載多個主題的書籍
queries = [
    "machine learning",
    "data science",
    "artificial intelligence"
]

downloader.batch_download(queries, limit_per_query=3)
```

### 示例 3：命令行交互

```bash
$ python3 anna_archive_downloader.py

================================================================================
📚 Anna Archive 自動下載工具
================================================================================

⚠️  法律聲明：
   - 僅用於下載公共領域或開放授權的書籍
   - 遵守當地法律法規
   - 僅供個人學習/研究使用
   - 不要分發受版權保護的內容

使用本工具即表示你同意以上條款

是否同意？(y/n): y

請選擇操作：
1. 搜索書籍
2. 批量下載
3. 退出

> 1

輸入搜索關鍵詞：python programming
內容類型 (book/article/comic/magazine)，默認 book：
結果數量 (1-20)，默認 10：
```

---

## 📁 文件結構

```
workspace/
├── anna_archive_downloader.py    # 主程序
├── ANNA_ARCHIVE_README.md        # 使用說明（本文件）
└── downloads/                    # 下載目錄（自動創建）
    ├── download_abc123.pdf
    └── download_def456.epub
```

---

## 🛠️ 高級用法

### 自定義下載目錄

```python
# 設置特定下載目錄
downloader = AnnaArchiveDownloader(download_dir="/path/to/books")
```

### 搜索特定類型

```python
# 搜索文章
results = downloader.search("AI research", content_type="article")

# 搜索漫畫
results = downloader.search("manga", content_type="comic")

# 搜索雜誌
results = downloader.search("nature", content_type="magazine")
```

### 限制結果數量

```python
# 最多返回 20 條結果
results = downloader.search("python", limit=20)
```

---

## ⚠️ 注意事項

### 1. 法律風險

- 下載受版權保護的書籍可能違法
- 請僅下載公共領域或開放授權的內容
- 了解你所在地區的法律

### 2. 使用限制

- 避免短時間內大量請求（可能被封 IP）
- 程序已內置 2 秒延遲
- 建議批量下載時設置合理的 limit

### 3. 技術限制

- Anna Archive API 可能變化
- 下載鏈接可能失效
- 部分書籍可能需要特殊處理

---

## 🔧 故障排除

### 問題 1：搜索失敗

**症狀：** `❌ 搜索失敗：Connection timeout`

**解決：**
- 檢查網絡連接
- 檢查 Anna Archive 是否可訪問
- 稍後重試

### 問題 2：無法下載

**症狀：** `❌ 獲取下載鏈接失敗`

**解決：**
- 書籍可能已下架
- 下載鏈接可能失效
- 嘗試其他來源

### 問題 3：下載速度慢

**症狀：** 下載進度緩慢

**解決：**
- 檢查網絡速度
- 避免同時下載多個文件
- 稍後重試

---

## 📚 合法替代方案

如果你需要合法獲取書籍，考慮以下選項：

### 公共領域資源

| 網站 | 說明 |
|------|------|
| **Project Gutenberg** | 60,000+ 本公共領域書籍 |
| **Internet Archive** | 數百萬本免費書籍 |
| **Open Library** | 可借閱的數字圖書館 |
| **Google Books** | 部分免費預覽 |
| **Z-Library (合法部分)** | 開放授權學術論文 |

### 學術資源

| 網站 | 說明 |
|------|------|
| **arXiv** | 物理、數學、計算機科學論文 |
| **PubMed Central** | 生物醫學論文 |
| **DOAJ** | 開放獲取期刊 |
| **ResearchGate** | 研究論文分享 |

---

## 🎯 最佳實踐

### 1. 合法使用

- ✅ 僅下載公共領域內容
- ✅ 用於個人學習/研究
- ✅ 引用來源
- ❌ 不分發受版權保護內容

### 2. 尊重資源

- ✅ 限制請求頻率
- ✅ 使用合理的搜索限制
- ✅ 避免自動化爬蟲行為
- ❌ 不要濫用 API

### 3. 文件管理

- ✅ 組織下載的文件
- ✅ 添加書名和作者信息
- ✅ 定期清理不需要的文件
- ✅ 備份重要文件

---

## 📞 需要幫助？

如有問題或建議：

1. 查看本使用說明
2. 檢查故障排除章節
3. 考慮使用合法替代方案

---

## 📝 版本歷史

| 版本 | 日期 | 更新內容 |
|------|------|---------|
| 1.0 | 2026-02-26 | 初始版本，基本搜索和下載功能 |

---

**請合法使用本工具！** 📚⚖️
