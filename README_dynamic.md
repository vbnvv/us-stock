# 美股複委託同業上架數量 - 動態版本

## 功能特色

✅ **即時讀取CSV/Excel文件** - 不需要預先生成靜態HTML，直接讀取CSV和Excel文件
✅ **動態篩選和搜索** - 即時搜索標的代號和名稱，動態篩選銀行
✅ **範圍篩選功能** - 使用雙拉桿設定同業上架數量篩選範圍（如2~5檔）
✅ **自動檢測文件格式** - 支援CSV和Excel文件，自動識別列名
✅ **即時統計信息** - 顯示總檔數、篩選結果、銀行數量等統計
✅ **CSV下載功能** - 一鍵下載當前篩選的數據為CSV文件

✅ **錯誤處理** - 完善的錯誤處理和使用者提示

## 文件結構

```
us-stock/
├── stock_summary_dynamic.html    # 動態版本的HTML頁面
├── stock_reader.js              # JavaScript數據讀取器

├── README_dynamic.md            # 使用說明（本文件）
└── all_bank_stock/             # 數據文件夾
    ├── CTBC_bank.csv           # 中信銀行數據
    ├── esun_bank.csv           # 玉山銀行數據
    ├── fubon_bank.xlsx         # 富邦銀行數據（Excel格式）
    ├── mega_bank.csv           # 兆豐銀行數據
    ├── tashin_bank.csv         # 台新銀行數據
    └── ubot_bank.csv           # 聯邦銀行數據
```



## 如何使用

### 1. 設置文件

1. 將所有銀行的股票數據文件放入 `all_bank_stock/` 文件夾
2. 確保文件命名符合規則：`[銀行名稱]_bank.csv` 或 `[銀行名稱]_bank.xlsx`
3. 支援的銀行名稱映射：
   - `CTBC` → 中信
   - `esun` → 玉山
   - `fubon` → 富邦
   - `mega` → 兆豐
   - `tashin` → 台新
   - `ubot` → 聯邦

### 2. CSV文件格式要求

CSV文件需要包含以下列名（支援多種變體）：
- 標的代號：`代碼`、`商品代號`、`代號`、`symbol`、`Symbol`
- 標的名稱：`股票名稱`、`商品名稱`、`名稱`、`name`、`Name`

範例CSV格式：
```csv
代碼,股票名稱
AAPL,蘋果電腦
MSFT,微軟
GOOGL,Google
```

### 3. 啟動系統

1. 將 `stock_summary_dynamic.html` 和 `stock_reader.js` 放在Web伺服器上
2. 在瀏覽器中打開 `stock_summary_dynamic.html`
3. 系統會自動讀取 `all_bank_stock/` 文件夾中的數據文件

### 4. 使用功能

- **搜索**：在搜索框中輸入標的代號或名稱進行即時搜索
- **銀行篩選**：點擊銀行標籤篩選包含該銀行的股票
- **聯邦銀行篩選**：選擇是否顯示聯邦銀行的股票
- **刷新數據**：點擊"刷新數據"按鈕重新載入最新的CSV文件
- **統計信息**：頁面底部顯示即時統計信息

## 技術特點

### JavaScript類別設計
- **模組化設計**：使用ES6 Class組織代碼
- **事件驅動**：基於事件的互動處理
- **錯誤處理**：完善的錯誤捕獲和使用者提示
- **非同步處理**：使用async/await處理文件讀取

### 支援的文件格式
- **CSV文件**：使用自定義CSV解析器，支援引號和逗號處理
- **Excel文件**：使用xlsx.js庫讀取Excel文件
- **自動檢測**：根據文件副檔名自動選擇讀取方式

### 數據處理流程
1. **讀取文件** → 2. **解析數據** → 3. **標準化列名** → 4. **合併數據** → 5. **分組統計** → 6. **排序顯示**

## 與Python版本的比較

| 功能 | Python版本 | JavaScript版本 |
|------|------------|----------------|
| 數據讀取 | 預處理生成靜態HTML | 即時讀取CSV/Excel |
| 更新數據 | 需要重新執行Python腳本 | 點擊按鈕即可刷新 |
| 部署方式 | 需要Python環境 | 只需要Web伺服器 |
| 即時互動 | 基於靜態JSON數據 | 動態讀取和處理 |
| 錯誤處理 | 控制台輸出 | 使用者友好的錯誤提示 |

## 錯誤處理

系統包含完善的錯誤處理機制：

1. **文件讀取錯誤**：顯示具體的文件讀取失敗信息
2. **格式錯誤**：自動跳過格式不正確的文件
3. **網絡錯誤**：提示檢查網絡連接
4. **解析錯誤**：顯示數據解析失敗的詳細信息

## 瀏覽器支援

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## 疑難排解

### 常見問題

1. **數據不顯示**
   - 檢查文件路徑是否正確
   - 確認CSV文件格式是否符合要求
   - 查看瀏覽器控制台的錯誤信息

2. **Excel文件讀取失敗**
   - 確認xlsx.js庫是否正確載入
   - 檢查Excel文件是否損壞
   - 嘗試轉換為CSV格式

3. **篩選功能不工作**
   - 確認數據已完全載入
   - 檢查瀏覽器控制台是否有JavaScript錯誤

### 開發者選項

```javascript
// 在瀏覽器控制台中使用這些命令進行調試

// 查看當前數據
console.log(window.stockDataReader.tableData);

// 查看統計信息
console.log(window.stockDataReader.getStatistics());

// 導出篩選後的數據
console.log(window.stockDataReader.exportFilteredData());

// 手動刷新數據
await window.stockDataReader.refresh();
```

## 自定義和擴展

### 添加新銀行
1. 在 `stock_reader.js` 中的 `bankNameMap` 添加新的銀行映射
2. 將新銀行的CSV文件放入 `all_bank_stock/` 文件夾
3. 文件命名格式：`[銀行代碼]_bank.csv`

### 修改樣式
所有樣式都在HTML文件的 `<style>` 標籤中，可以根據需要修改顏色、字體、佈局等。

### 添加新功能
`StockDataReader` 類別提供了多個公共方法，可以用於擴展功能：
- `refresh()`: 重新載入數據
- `exportFilteredData()`: 導出篩選後的數據
- `getStatistics()`: 獲取統計信息

## 版本更新

### v1.0.0
- 初始版本
- 支援CSV和Excel文件讀取
- 動態篩選和搜索功能
- 即時統計信息顯示 

### v1.1.0
- 新增CSV下載功能
- 在表格右上角添加"下載CSV"按鈕
- 支援下載當前篩選的數據為CSV文件
- 自動生成帶時間戳的文件名

### v1.1.1
- 修改CSV文件名格式，將時間戳改為檔數
- 文件名格式：`美股複委託上架統計_YYYY-MM-DD_檔數檔.csv`

### v1.2.0
- 新增同業上架數量範圍篩選功能
- 可設定最小值和最大值（如2~5檔）
- 自動根據數據設定範圍上限
- 提供重置按鈕一鍵恢復預設範圍

### v1.2.1
- 將範圍篩選器改為雙拉桿設計
- 移動到第二列（篩選銀行下方）
- 即時顯示拉桿數值，操作更直觀
- 拉桿具有防衝突邏輯，最小值不會大於最大值

### v1.2.2
- 移除"刷新數據"按鈕，簡化界面

### v1.3.0
- 優化表格布局，調整欄位寬度
- 改進用戶界面體驗
- 提升系統穩定性和性能

## 💡 使用技巧

### CSV下載功能
1. **位置**：CSV下載按鈕位於表格右上角，與統計信息同一行
2. **功能**：下載當前篩選和搜索結果的數據
3. **格式**：包含標的代號、標的名稱、同業上架數量、上架銀行列表
4. **文件名**：自動生成格式為 `美股複委託上架統計_YYYY-MM-DD_檔數檔.csv`
5. **編碼**：支援中文，使用UTF-8編碼
6. **提示**：如果沒有數據會顯示提示信息

### 使用步驟
1. 開啟命令提示符，進入 `us-stock` 目錄
2. 啟動Web服務器：`python -m http.server 8000`
3. 瀏覽器打開 `http://localhost:8000/stock_summary_dynamic.html`
4. 等待數據載入完成
5. 使用搜索框或銀行篩選器篩選需要的數據
6. 設定上架數量範圍（可選）
7. 點擊右上角的"📥 下載CSV"按鈕
8. 選擇保存位置即可完成下載

### 範圍篩選功能
1. **位置**：位於第二列，篩選銀行下方，顯示"同業上架數量"
2. **操作方式**：使用雙拉桿進行範圍設定
   - 綠色拉桿：設定最小值
   - 藍色拉桿：設定最大值
   - 中間數值：即時顯示當前範圍（如：2~5）
3. **自動範圍**：系統會自動根據數據設定可選擇的最大值
4. **防衝突邏輯**：拉桿會自動防止最小值大於最大值的情況
5. **重置功能**：點擊"重置"按鈕可恢復到預設範圍（1到最大值）
6. **即時篩選**：拖動拉桿時即時更新顯示數值和篩選結果