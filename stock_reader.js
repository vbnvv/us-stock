class StockDataReader {
    constructor() {
        this.allData = [];
        this.bankNameMap = {
            'Ctbc': '中信',
            'Esun': '玉山', 
            'Fubon': '富邦',
            'Mega': '兆豐',
            'Tashin': '台新',
            'Ubot': '聯邦'
        };
        this.uniqueBanks = [];
        this.uniqueIndustries = [];
        this.gicsIndustries = [
            '能源',
            '原材料',
            '工業',
            '非必需消費品',
            '必需消費品',
            '醫療保健',
            '金融服務',
            '資訊科技',
            '通訊服務',
            '公用事業',
            '房地產'
        ];
        this.tableData = [];
        this.currentFilteredData = [];
        this.stockInfo = new Map(); // 存儲 stock_info.csv 的數據
        this.sortConfig = { column: null, direction: 'asc' };

        
        this.initializeElements();
        this.initialize();
    }

    async initialize() {
        await this.loadStockInfo();
        await this.loadDataFiles();
    }

    initializeElements() {
        this.tableBody = document.getElementById('stock-table-body');
        this.tableInfo = document.getElementById('table-info');
        this.searchInput = document.getElementById('searchInput');
        this.bankFilterContainer = document.querySelector('.bank-filter-container');
        this.industryFilterContainer = document.querySelector('.industry-filter-container');
        this.ubotFilterContainer = document.querySelector('.ubot-filter-container');
        this.minRangeInput = document.getElementById('minRange');
        this.maxRangeInput = document.getElementById('maxRange');
        this.minValueDisplay = document.getElementById('minValue');
        this.maxValueDisplay = document.getElementById('maxValue');
        this.rangeTrack = document.getElementById('rangeTrack');
        this.minTooltip = document.getElementById('minTooltip');
        this.maxTooltip = document.getElementById('maxTooltip');
        
        // 綁定搜索事件
        if (this.searchInput) {
            this.searchInput.addEventListener('input', () => this.filterTable());
        }
        
        // 綁定排序事件
        setTimeout(() => {
            const sortableHeaders = document.querySelectorAll('.sortable');
            sortableHeaders.forEach(header => {
                header.addEventListener('click', () => {
                    const column = header.dataset.sort;
                    this.sortTable(column);
                });
            });
        }, 100);
        
        // 綁定聯邦銀行篩選事件
        if (this.ubotFilterContainer) {
            this.ubotFilterContainer.addEventListener('change', () => this.filterTable());
        }
        
        // 綁定範圍篩選事件
        if (this.minRangeInput) {
            this.minRangeInput.addEventListener('input', () => {
                this.updateRangeSlider();
                this.filterTable();
            });
            
            // tooltip事件
            this.minRangeInput.addEventListener('mousedown', () => {
                this.showTooltip(this.minTooltip, this.minRangeInput);
            });
            this.minRangeInput.addEventListener('mousemove', () => {
                if (this.minTooltip.style.display === 'block') {
                    this.updateTooltip(this.minTooltip, this.minRangeInput);
                }
            });
            this.minRangeInput.addEventListener('mouseup', () => {
                this.hideTooltip(this.minTooltip);
            });
            this.minRangeInput.addEventListener('mouseleave', () => {
                this.hideTooltip(this.minTooltip);
            });
        }
        if (this.maxRangeInput) {
            this.maxRangeInput.addEventListener('input', () => {
                this.updateRangeSlider();
                this.filterTable();
            });
            
            // tooltip事件
            this.maxRangeInput.addEventListener('mousedown', () => {
                this.showTooltip(this.maxTooltip, this.maxRangeInput);
            });
            this.maxRangeInput.addEventListener('mousemove', () => {
                if (this.maxTooltip.style.display === 'block') {
                    this.updateTooltip(this.maxTooltip, this.maxRangeInput);
                }
            });
            this.maxRangeInput.addEventListener('mouseup', () => {
                this.hideTooltip(this.maxTooltip);
            });
            this.maxRangeInput.addEventListener('mouseleave', () => {
                this.hideTooltip(this.maxTooltip);
            });
        }
    }

    async loadDataFiles() {
        try {
            const dataDir = 'all_bank_stock/';
            const files = [
                'CTBC_bank.csv',
                'esun_bank.csv', 
                'fubon_bank.xlsx',
                'mega_bank.csv',
                'tashin_bank.csv',
                'ubot_bank.csv'
            ];
            
            this.showLoadingMessage('正在讀取數據文件...');
            
            for (const filename of files) {
                try {
                    const bankName = this.extractBankName(filename);
                    const filePath = dataDir + filename;
                    
                    let data;
                    if (filename.endsWith('.csv')) {
                        data = await this.readCSVFile(filePath);
                    } else if (filename.endsWith('.xlsx')) {
                        data = await this.readExcelFile(filePath);
                    }
                    
                    if (data && data.length > 0) {
                        this.processFileData(data, bankName);
                    }
                } catch (error) {
                    console.warn(`無法讀取文件 ${filename}:`, error);
                }
            }
            
            await this.processAllData();
            this.createBankFilters();
            this.renderTable(this.tableData);
            this.hideLoadingMessage();
            
        } catch (error) {
            console.error('讀取數據文件時出錯:', error);
            this.showErrorMessage('讀取數據文件失敗，請檢查文件路徑');
        }
    }

    extractBankName(filename) {
        const bankName = filename.split('_')[0].toLowerCase();
        return this.bankNameMap[bankName.charAt(0).toUpperCase() + bankName.slice(1)] || bankName;
    }

    async readCSVFile(filePath) {
        try {
            const response = await fetch(filePath);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const text = await response.text();
            return this.parseCSV(text);
        } catch (error) {
            console.error(`讀取CSV文件失敗: ${filePath}`, error);
            return null;
        }
    }

    async readExcelFile(filePath) {
        try {
            const response = await fetch(filePath);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const arrayBuffer = await response.arrayBuffer();
            
            // 需要引入 xlsx 庫來處理 Excel 文件
            if (typeof XLSX === 'undefined') {
                console.error('需要引入 xlsx 庫來讀取 Excel 文件');
                return null;
            }
            
            const workbook = XLSX.read(arrayBuffer, { type: 'array' });
            const sheetName = workbook.SheetNames[0];
            const worksheet = workbook.Sheets[sheetName];
            const jsonData = XLSX.utils.sheet_to_json(worksheet);
            
            return jsonData;
        } catch (error) {
            console.error(`讀取Excel文件失敗: ${filePath}`, error);
            return null;
        }
    }

    parseCSV(csvText) {
        const lines = csvText.split('\n');
        const headers = lines[0].split(',').map(h => h.trim());
        const data = [];
        
        for (let i = 1; i < lines.length; i++) {
            const line = lines[i].trim();
            if (line) {
                const values = this.parseCSVLine(line);
                if (values.length === headers.length) {
                    const row = {};
                    headers.forEach((header, index) => {
                        row[header] = values[index];
                    });
                    data.push(row);
                }
            }
        }
        
        return data;
    }

    parseCSVLine(line) {
        const values = [];
        let current = '';
        let inQuotes = false;
        
        for (let i = 0; i < line.length; i++) {
            const char = line[i];
            
            if (char === '"') {
                inQuotes = !inQuotes;
            } else if (char === ',' && !inQuotes) {
                values.push(current.trim());
                current = '';
            } else {
                current += char;
            }
        }
        
        values.push(current.trim());
        return values;
    }

    processFileData(data, bankName) {
        data.forEach(row => {
            // 標準化列名
            const normalizedRow = this.normalizeColumnNames(row);
            
            if (normalizedRow['代碼'] && normalizedRow['股票名稱']) {
                const code = normalizedRow['代碼'].toString().trim();
                const name = normalizedRow['股票名稱'].toString().trim();
                
                if (code && name && code !== 'nan' && name !== 'nan') {
                    this.allData.push({
                        代碼: code,
                        股票名稱: name,
                        bank: bankName
                    });
                }
            }
        });
    }

    normalizeColumnNames(row) {
        const normalized = {};
        
        // 常見的列名映射
        const columnMapping = {
            '商品代號': '代碼',
            '商品名稱': '股票名稱',
            '代號': '代碼',
            '名稱': '股票名稱',
            'symbol': '代碼',
            'name': '股票名稱',
            'Symbol': '代碼',
            'Name': '股票名稱'
        };
        
        Object.keys(row).forEach(key => {
            const mappedKey = columnMapping[key] || key;
            normalized[mappedKey] = row[key];
        });
        
        return normalized;
    }

    async processAllData() {
        // 獲取唯一銀行列表
        this.uniqueBanks = [...new Set(this.allData.map(item => item.bank))].sort();
        
        // 按股票代碼分組，統計銀行信息
        const groupedData = {};
        
        this.allData.forEach(item => {
            const code = item.代碼;
            
            if (!groupedData[code]) {
                groupedData[code] = {
                    標的代號: code,
                    標的名稱: item.股票名稱,
                    banks: new Set(),
                    bankCount: 0
                };
            }
            
            groupedData[code].banks.add(item.bank);
        });
        
        // 轉換為最終表格數據
        this.tableData = Object.values(groupedData).map(item => {
            const ticker = item.標的代號;
            const stockInfo = this.stockInfo.get(ticker);
            
            return {
                標的代號: ticker,
                標的名稱: stockInfo ? stockInfo.name : item.標的名稱,
                產業: stockInfo ? stockInfo.industry : '',
                同業上架數量: item.banks.size,
                上架銀行: Array.from(item.banks).sort().join(', ')
            };
        });
        
        // 按上架數量和代碼排序
        this.tableData.sort((a, b) => {
            if (a.同業上架數量 !== b.同業上架數量) {
                return b.同業上架數量 - a.同業上架數量;
            }
            return a.標的代號.localeCompare(b.標的代號);
        });
        
        this.currentFilteredData = [...this.tableData];
        
        // 獲取數據中實際存在的產業列表（保留供參考）
        this.uniqueIndustries = [...new Set(this.tableData.map(item => item.產業).filter(industry => industry))].sort();
        
        // 設置範圍篩選器的最大值
        this.updateRangeInputs();
        
        // 創建產業篩選按鈕（使用GICS 11大產業）
        this.createIndustryFilters();
    }

    updateRangeInputs() {
        if (!this.tableData || this.tableData.length === 0) return;
        
        const maxCount = Math.max(...this.tableData.map(item => item.同業上架數量));
        
        if (this.minRangeInput) {
            this.minRangeInput.setAttribute('max', maxCount);
            this.minRangeInput.value = 1;
        }
        if (this.maxRangeInput) {
            this.maxRangeInput.setAttribute('max', maxCount);
            this.maxRangeInput.value = maxCount;
        }
        
        // 更新顯示值
        this.updateRangeDisplay();
    }

    updateRangeSlider() {
        const minVal = parseInt(this.minRangeInput.value);
        const maxVal = parseInt(this.maxRangeInput.value);
        
        // 確保最小值不大於最大值
        if (minVal > maxVal) {
            this.minRangeInput.value = maxVal;
        }
        
        // 確保最大值不小於最小值
        if (maxVal < minVal) {
            this.maxRangeInput.value = minVal;
        }
        
        // 更新顯示值
        this.updateRangeDisplay();
    }

    updateRangeDisplay() {
        if (this.minValueDisplay) {
            this.minValueDisplay.textContent = this.minRangeInput.value;
        }
        if (this.maxValueDisplay) {
            this.maxValueDisplay.textContent = this.maxRangeInput.value;
        }
        
        // 更新軌道顯示
        this.updateRangeTrack();
    }

    updateRangeTrack() {
        if (!this.rangeTrack || !this.minRangeInput || !this.maxRangeInput) return;
        
        const min = parseInt(this.minRangeInput.min);
        const max = parseInt(this.minRangeInput.max);
        const minVal = parseInt(this.minRangeInput.value);
        const maxVal = parseInt(this.maxRangeInput.value);
        
        const leftPercent = ((minVal - min) / (max - min)) * 100;
        const rightPercent = ((maxVal - min) / (max - min)) * 100;
        
        this.rangeTrack.style.left = leftPercent + '%';
        this.rangeTrack.style.width = (rightPercent - leftPercent) + '%';
    }

    createBankFilters() {
        if (!this.bankFilterContainer) return;
        
        // 清除現有的篩選器
        const existingFilters = this.bankFilterContainer.querySelectorAll('.bank-toggle');
        existingFilters.forEach(filter => filter.remove());
        
        // 統計每個銀行的原始數據數量
        const bankCounts = {};
        this.uniqueBanks.forEach(bank => {
            bankCounts[bank] = this.allData.filter(item => item.bank === bank).length;
        });
        
        // 創建新的篩選器
        const filterLabel = this.bankFilterContainer.querySelector('.filter-label');
        
        this.uniqueBanks.forEach(bank => {
            const label = document.createElement('label');
            label.className = 'bank-toggle';
            
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.value = bank;
            checkbox.addEventListener('change', () => this.filterTable());
            
            const span = document.createElement('span');
            span.innerHTML = `<span class="bank-name">${bank}</span><span class="bank-count">${bankCounts[bank]}</span>`;
            
            label.appendChild(checkbox);
            label.appendChild(span);
            
            if (filterLabel) {
                filterLabel.insertAdjacentElement('afterend', label);
            }
        });
    }

    createIndustryFilters() {
        if (!this.industryFilterContainer) return;
        
        // 清除現有的篩選器
        const existingFilters = this.industryFilterContainer.querySelectorAll('.industry-toggle');
        existingFilters.forEach(filter => filter.remove());
        
        // 統計每個產業的股票數量
        const industryCounts = {};
        this.gicsIndustries.forEach(industry => {
            industryCounts[industry] = this.tableData.filter(item => item.產業 === industry).length;
        });
        
        // 創建新的篩選器
        const filterLabel = this.industryFilterContainer.querySelector('.filter-label');
        
        this.gicsIndustries.forEach(industry => {
            const label = document.createElement('label');
            label.className = 'bank-toggle industry-toggle';
            
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.value = industry;
            checkbox.addEventListener('change', () => this.filterTable());
            
            const span = document.createElement('span');
            span.innerHTML = `<span class="bank-name">${industry}</span><span class="bank-count">${industryCounts[industry]}</span>`;
            
            label.appendChild(checkbox);
            label.appendChild(span);
            
            if (filterLabel) {
                filterLabel.insertAdjacentElement('afterend', label);
            }
        });
    }

    filterTable() {
        const searchFilter = this.searchInput ? this.searchInput.value.toLowerCase() : '';
        
        // 獲取選中的銀行
        const selectedBanks = Array.from(
            this.bankFilterContainer.querySelectorAll('input[type="checkbox"]:checked')
        ).map(cb => cb.value);
        
        // 獲取選中的產業
        const selectedIndustries = Array.from(
            this.industryFilterContainer.querySelectorAll('input[type="checkbox"]:checked')
        ).map(cb => cb.value);
        
        // 獲取聯邦銀行篩選
        const ubotFilter = this.ubotFilterContainer ? 
            this.ubotFilterContainer.querySelector('input[name="ubotFilter"]:checked')?.value : 'all';
        
        // 獲取範圍篩選
        const minRange = this.minRangeInput ? parseInt(this.minRangeInput.value) || 1 : 1;
        const maxRange = this.maxRangeInput ? parseInt(this.maxRangeInput.value) || 10 : 10;
        
        // 篩選數據
        this.currentFilteredData = this.tableData.filter(row => {
            // 聯邦銀行篩選
            if (ubotFilter === 'exclude' && row['上架銀行'].includes('聯邦')) {
                return false;
            }
            
            // 搜索篩選
            const matchesSearch = !searchFilter || 
                row['標的代號'].toLowerCase().includes(searchFilter) ||
                row['標的名稱'].toLowerCase().includes(searchFilter) ||
                row['產業'].toLowerCase().includes(searchFilter);
            
            // 銀行篩選
            const matchesBanks = selectedBanks.length === 0 || 
                selectedBanks.every(bank => row['上架銀行'].includes(bank));
            
            // 產業篩選
            const matchesIndustries = selectedIndustries.length === 0 || 
                selectedIndustries.includes(row['產業']);
            
            // 範圍篩選
            const matchesRange = row['同業上架數量'] >= minRange && row['同業上架數量'] <= maxRange;
            
            return matchesSearch && matchesBanks && matchesIndustries && matchesRange;
        });
        
        this.renderTable(this.currentFilteredData);
    }

    renderTable(data) {
        if (!this.tableBody) return;
        
        // 更新排序指示器
        document.querySelectorAll('.sortable').forEach(header => {
            header.classList.remove('sort-asc', 'sort-desc');
            if (this.sortConfig.column === header.dataset.sort) {
                header.classList.add(`sort-${this.sortConfig.direction}`);
            }
        });
        
        // 更新統計信息
        if (this.tableInfo) {
            this.tableInfo.innerHTML = `共 <span style="color: #E87A90; font-weight: 600;">${data.length}</span> 檔`;
        }
        
        // 顯示或隱藏下載按鈕
        const downloadBtn = document.getElementById('download-btn');
        if (downloadBtn) {
            downloadBtn.style.display = data.length > 0 ? 'flex' : 'none';
        }
        
        // 清空表格
        this.tableBody.innerHTML = '';
        
        // 添加新數據
        data.forEach(row => {
            const tr = document.createElement('tr');
            
            // 如果不包含聯邦銀行，使用藍色字體
            if (!row['上架銀行'].includes('聯邦')) {
                tr.style.color = '#0056b3';
            }
            
            tr.innerHTML = `
                <td>${row['標的代號']}</td>
                <td>${row['標的名稱']}</td>
                <td>${row['產業']}</td>
                <td>${row['同業上架數量']}</td>
                <td>${row['上架銀行']}</td>
            `;
            
            this.tableBody.appendChild(tr);
        });
    }

    showLoadingMessage(message) {
        if (this.tableInfo) {
            this.tableInfo.innerHTML = `<span style="color: #999;">${message}</span>`;
        }
        if (this.tableBody) {
            this.tableBody.innerHTML = `
                <tr>
                    <td colspan="5" style="text-align: center; padding: 2rem; color: #999;">
                        ${message}
                    </td>
                </tr>
            `;
        }
    }

    hideLoadingMessage() {
        // 加載完成後會調用 renderTable，不需要特別處理
    }

    showErrorMessage(message) {
        if (this.tableInfo) {
            this.tableInfo.innerHTML = `<span style="color: #dc3545;">${message}</span>`;
        }
        if (this.tableBody) {
            this.tableBody.innerHTML = `
                <tr>
                    <td colspan="5" style="text-align: center; padding: 2rem; color: #dc3545;">
                        ${message}
                    </td>
                </tr>
            `;
        }
    }

    // 公共方法：手動刷新數據
    async refresh() {
        this.allData = [];
        this.tableData = [];
        await this.loadDataFiles();
    }

    // 公共方法：導出當前篩選的數據
    exportFilteredData() {
        return this.currentFilteredData;
    }

    // 公共方法：獲取統計信息
    getStatistics() {
        return {
            totalStocks: this.tableData.length,
            filteredStocks: this.currentFilteredData.length,
            totalBanks: this.uniqueBanks.length,
            averageBankCount: this.tableData.reduce((sum, item) => sum + item.同業上架數量, 0) / this.tableData.length
        };
    }

    // 公共方法：重置範圍篩選器
    resetRangeFilter() {
        if (this.tableData && this.tableData.length > 0) {
            const maxCount = Math.max(...this.tableData.map(item => item.同業上架數量));
            
            if (this.minRangeInput) {
                this.minRangeInput.value = 1;
            }
            if (this.maxRangeInput) {
                this.maxRangeInput.value = maxCount;
            }
            
            // 更新顯示值
            this.updateRangeDisplay();
            
            this.filterTable();
        }
    }

    // 公共方法：下載當前篩選的數據為CSV
    downloadCSV() {
        if (!this.currentFilteredData || this.currentFilteredData.length === 0) {
            alert('沒有可下載的數據！');
            return;
        }

        // 創建CSV內容
        const headers = ['標的代號', '標的名稱', '產業', '同業上架數量', '上架銀行'];
        const csvContent = [
            headers.join(','),
            ...this.currentFilteredData.map(row => [
                row.標的代號,
                `"${row.標的名稱}"`, // 用雙引號包圍可能包含逗號的名稱
                `"${row.產業}"`, // 用雙引號包圍可能包含逗號的產業
                row.同業上架數量,
                `"${row.上架銀行}"` // 用雙引號包圍可能包含逗號的銀行列表
            ].join(','))
        ].join('\n');

        // 創建並下載文件
        const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        
        // 生成文件名
        const now = new Date();
        const dateStr = now.toISOString().split('T')[0];
        const dataCount = this.currentFilteredData.length;
        const filename = `美股複委託上架統計_${dateStr}_${dataCount}檔.csv`;
        
        link.setAttribute('download', filename);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
        
        console.log(`已下載 ${this.currentFilteredData.length} 筆資料`);
    }

    async loadStockInfo() {
        try {
            const response = await fetch('stock_info.csv');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const text = await response.text();
            const lines = text.split('\n');
            const headers = lines[0].split(',').map(h => h.trim());
            
            for (let i = 1; i < lines.length; i++) {
                const line = lines[i].trim();
                if (line) {
                    const values = this.parseCSVLine(line);
                    if (values.length === headers.length) {
                        const stockInfo = {};
                        headers.forEach((header, index) => {
                            stockInfo[header] = values[index];
                        });
                        this.stockInfo.set(values[0], stockInfo);
                    }
                }
            }
            console.log(`已加載 ${this.stockInfo.size} 筆股票信息`);
        } catch (error) {
            console.warn('讀取 stock_info.csv 時出錯:', error);
            // 靜默失敗，不顯示錯誤信息
        }
    }

    sortTable(column) {
        if (!this.tableData || this.tableData.length === 0) return;
        
        const direction = this.sortConfig.column === column ? this.sortConfig.direction === 'asc' ? 'desc' : 'asc' : 'asc';
        this.sortConfig = { column, direction };
        
        this.tableData.sort((a, b) => {
            const aValue = a[column];
            const bValue = b[column];
            
            if (typeof aValue === 'string' && typeof bValue === 'string') {
                return direction === 'asc' ? aValue.localeCompare(bValue) : bValue.localeCompare(aValue);
            } else if (typeof aValue === 'number' && typeof bValue === 'number') {
                return direction === 'asc' ? aValue - bValue : bValue - aValue;
            }
            return 0;
        });
        
        // 重新應用篩選器
        this.filterTable();
    }
}

// 當文檔加載完成時初始化
document.addEventListener('DOMContentLoaded', () => {
    window.stockDataReader = new StockDataReader();
    window.stockReader = window.stockDataReader; // 提供另一個名稱以便HTML調用
});

// 重置範圍篩選器的全局函數
function resetRangeFilter() {
    if (window.stockDataReader) {
        window.stockDataReader.resetRangeFilter();
    }
} 