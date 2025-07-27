/**
 * Header 載入器
 * 用於動態載入 header 組件到各個頁面
 */

class HeaderLoader {
    constructor() {
        this.headerContainer = null;
        this.pageType = null;
    }

    /**
     * 初始化 header
     * @param {string} pageType - 頁面類型 ('stocks', 'earnings', 'ipo', 'news')
     * @param {string} containerId - header 容器的 ID
     */
    async init(pageType, containerId = 'header-container') {
        this.pageType = pageType;
        this.headerContainer = document.getElementById(containerId);
        
        if (!this.headerContainer) {
            console.error(`Header container with ID '${containerId}' not found`);
            return;
        }

        try {
            await this.loadHeader();
            this.initializeHeader();
        } catch (error) {
            console.error('Failed to load header:', error);
            this.showFallbackHeader();
        }
    }

    /**
     * 載入 header HTML
     */
    async loadHeader() {
        const response = await fetch('components/header.html');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const headerHtml = await response.text();
        this.headerContainer.innerHTML = headerHtml;
    }

    /**
     * 初始化 header 功能
     */
    initializeHeader() {
        // 設置當前頁面的導航高亮
        this.setActiveNav(this.pageType);
    }

    /**
     * 顯示備用 header（當載入失敗時）
     */
    showFallbackHeader() {
        const fallbackHtml = `
            <nav class="navbar">
                <ul>
                    <li><a href="../index.html">🏠 首頁</a></li>
                    <li><a href="stock_summary_dynamic.html">📈 美股同業分析</a></li>
                    <li><a href="earnings_calendar.html">📅 財報日曆</a></li>
                    <li><a href="ipo_calendar.html">🚀 IPO 日曆</a></li>
                    <li><a href="us_stock_news.html">📰 美股新聞</a></li>
                </ul>
            </nav>
        `;
        this.headerContainer.innerHTML = fallbackHtml;
    }



    /**
     * 設置導航高亮
     * @param {string} pageType - 頁面類型
     */
    setActiveNav(pageType) {
        const navItems = document.querySelectorAll('.navbar a');
        navItems.forEach(item => {
            item.classList.remove('active');
        });

        const activeNav = document.getElementById(`nav-${pageType}`);
        if (activeNav) {
            activeNav.classList.add('active');
        }
    }
}

// 創建全局實例
window.headerLoader = new HeaderLoader();

// 簡化的初始化函數
function loadHeader(pageType, containerId = 'header-container') {
    return window.headerLoader.init(pageType, containerId);
} 