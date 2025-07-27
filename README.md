# 📈 美股分析工具

專業的美股投資分析平台，提供全面的市場數據和工具。

## 🏗️ 專案結構

```
us-stock/
├── index.html                 # 主頁面
├── html/                      # HTML 頁面
│   ├── stock_summary_dynamic.html    # 美股同業分析
│   ├── earnings_calendar.html        # 財報日曆
│   ├── ipo_calendar.html             # IPO 日曆
│   ├── us_stock_news.html            # 美股新聞

│   └── components/                   # 組件檔案
│       └── header.html               # Header 組件
├── js/                       # JavaScript 檔案
│   ├── stock_reader.js       # 股票數據讀取器
│   └── header-loader.js      # Header 載入器
├── css/                      # CSS 樣式檔案 (預留)
├── data/                     # 數據檔案
│   ├── stock_info.csv        # 股票資訊
│   ├── all_bank_link.xlsx    # 銀行連結數據
│   └── all_bank_stock/       # 銀行股票數據
├── python/                   # Python 腳本
│   ├── gemini_client.py      # Gemini AI 客戶端
│   ├── gemini_1.5.py         # Gemini 1.5 測試
│   ├── scrape_stock_list.py  # 股票列表爬蟲
│   ├── requirements.txt      # Python 依賴
│   └── requirements_gemini.txt # Gemini 依賴
└── docs/                     # 文檔
    └── README_dynamic.md     # 動態功能說明
```

## 🚀 功能特色

### 📊 美股同業分析
- 財務比率分析
- 同業比較功能
- 歷史數據追蹤
- 視覺化圖表

### 📅 財報日曆
- 財報日期提醒
- EPS 預估與實際值
- 營收數據分析
- 智能排序功能

### 🚀 IPO 日曆
- IPO 日期追蹤
- 發行價格資訊
- 募資額統計
- 交易所分類

### 📰 美股新聞
- 即時新聞更新
- 關鍵字標籤
- 分頁瀏覽
- 新聞摘要

## 🛠️ 技術架構

### 前端技術
- **HTML5**: 語義化標籤，響應式設計
- **CSS3**: 現代化樣式，漸層背景，動畫效果
- **JavaScript**: 動態數據處理，API 整合
- **組件化設計**: 獨立的 header 組件，可重複使用

### 組件系統
- **Header 組件**: 統一的導航欄和頁面標題
- **動態載入**: 使用 JavaScript 動態載入組件
- **模組化管理**: 便於維護和更新

### 後端技術
- **Python**: 數據爬蟲，API 客戶端
- **Finnhub API**: 股票數據來源
- **Google Gemini AI**: AI 分析功能

### 數據來源
- **Finnhub API**: 股票財務數據
- **鉅亨網**: 美股新聞資訊
- **Google Gemini**: AI 分析支援

## 📦 安裝與使用

### 1. 克隆專案
```bash
git clone [repository-url]
cd us-stock
```

### 2. 安裝 Python 依賴
```bash
cd python
pip install -r requirements.txt
pip install -r requirements_gemini.txt
```

### 3. 啟動本地服務器
```bash
python -m http.server 8000
```

### 4. 訪問應用
打開瀏覽器訪問：`http://localhost:8000`

### 5. Header 組件使用


## 🔧 配置說明

### API 密鑰配置
在對應的 HTML 檔案中配置您的 API 密鑰：
- Finnhub API Token
- Google Gemini API Key

### 數據更新
- 股票數據：通過 Finnhub API 自動更新
- 新聞數據：即時從鉅亨網獲取
- IPO 數據：定期從 Finnhub 更新

### Header 組件使用
```html
<!-- 1. 在 HTML 中添加容器 -->
<div id="header-container"></div>

<!-- 2. 引入 header 載入器 -->
<script src="../js/header-loader.js"></script>

<!-- 3. 初始化 header -->
<script>
document.addEventListener('DOMContentLoaded', async () => {
    await loadHeader('stocks'); // 頁面類型
});
</script>
```

支援的頁面類型：
- `'stocks'` - 美股同業分析
- `'earnings'` - 財報日曆  
- `'ipo'` - IPO 日曆
- `'news'` - 美股新聞

**特色功能：**
- 置頂導航欄，滾動時保持可見
- 統一的財報日曆風格設計
- 自動設置當前頁面高亮

## 📱 響應式設計

所有頁面都支援響應式設計，可在以下設備上正常使用：
- 桌面電腦
- 平板電腦
- 手機設備

## 🎨 設計特色

- **現代化 UI**: 使用漸層背景和毛玻璃效果
- **直觀導航**: 清晰的導航結構
- **數據視覺化**: 豐富的圖表和統計資訊
- **用戶體驗**: 流暢的動畫和交互效果

## 📄 授權說明

本專案僅供學習和研究使用，請勿用於商業用途。

## ⚠️ 免責聲明

- 本工具提供的數據僅供參考
- 投資有風險，請謹慎決策
- 不構成投資建議

## 🤝 貢獻指南

歡迎提交 Issue 和 Pull Request 來改善專案。

## 📞 聯絡資訊

如有問題或建議，請通過以下方式聯絡：
- 提交 GitHub Issue
- 發送郵件至：[your-email@example.com]

---

© 2025 美股分析工具 | 數據來源：Finnhub API, 鉅亨網 