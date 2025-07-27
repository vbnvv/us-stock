import requests
from bs4 import BeautifulSoup
import csv
import os
from urllib.parse import urlparse, parse_qs
import re
import json
from datetime import datetime
import pandas as pd

class StockComparison:
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.path.dirname(self.script_dir)
        self.data_dir = os.path.join(self.project_root, 'data', 'all_bank_stock')
        self.log_dir = os.path.join(self.project_root, 'data', 'logs')
        os.makedirs(self.log_dir, exist_ok=True)
        
    def load_old_data(self, bank_name):
        """載入舊的銀行股票數據"""
        old_file = os.path.join(self.data_dir, f'{bank_name}_bank.csv')
        old_stocks = set()
        
        if os.path.exists(old_file):
            try:
                with open(old_file, 'r', encoding='utf-8-sig') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        ticker = row.get('代碼', '').strip()
                        if ticker:
                            old_stocks.add(ticker)
                
            except Exception as e:
                print(f"載入 {bank_name} 舊數據失敗: {e}")
        else:
            print(f"找不到 {bank_name} 舊數據檔案")
        
        return old_stocks
    
    def compare_stocks(self, bank_name, new_stocks):
        """比對新舊股票清單"""
        old_stocks = self.load_old_data(bank_name)
        
        # 找出新增和移除的股票
        added_stocks = new_stocks - old_stocks
        removed_stocks = old_stocks - new_stocks
        
        return {
            'bank_name': bank_name,
            'old_count': len(old_stocks),
            'new_count': len(new_stocks),
            'added': list(added_stocks),
            'removed': list(removed_stocks),
            'total_change': len(added_stocks) - len(removed_stocks)
        }
    
    def save_comparison_log(self, comparisons):
        """儲存比對記錄到list_change.csv檔案"""
        log_file = os.path.join(self.log_dir, 'list_change.csv')
        
        # 檢查檔案是否存在，如果不存在則建立標題行
        file_exists = os.path.exists(log_file)
        
        # 準備記錄數據
        log_data = []
        for comp in comparisons:
            # 新增股票記錄
            for ticker in comp['added']:
                log_data.append({
                    '日期': datetime.now().strftime('%Y-%m-%d'),
                    '銀行': comp['bank_name'],
                    '股票代碼': ticker,
                    '變更類型': '上架',
                    '舊數量': comp['old_count'],
                    '新數量': comp['new_count'],
                    '淨變化': comp['total_change']
                })
            
            # 移除股票記錄
            for ticker in comp['removed']:
                log_data.append({
                    '日期': datetime.now().strftime('%Y-%m-%d'),
                    '銀行': comp['bank_name'],
                    '股票代碼': ticker,
                    '變更類型': '下架',
                    '舊數量': comp['old_count'],
                    '新數量': comp['new_count'],
                    '淨變化': comp['total_change']
                })
            
            # 如果沒有變更，不記錄到檔案中
            # if not comp['added'] and not comp['removed']:
            #     log_data.append({
            #         '日期': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            #         '銀行': comp['bank_name'],
            #         '股票代碼': '無變更',
            #         '變更類型': '無變更',
            #         '舊數量': comp['old_count'],
            #         '新數量': comp['new_count'],
            #         '淨變化': comp['total_change']
            #     })
        
        # 儲存記錄檔 - 每次新增到檔案末尾
        if log_data:
            with open(log_file, 'a', newline='', encoding='utf-8-sig') as f:
                fieldnames = ['日期', '銀行', '股票代碼', '變更類型', '舊數量', '新數量', '淨變化']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                
                # 如果檔案不存在，寫入標題行
                if not file_exists:
                    writer.writeheader()
                
                writer.writerows(log_data)
            
            print(f"\n✅ 變更記錄已新增至: {log_file}")
        else:
            print("\n❌ 沒有發現任何變更")
        
        return log_file
    

# 全域變數來儲存比對結果
stock_comparison = StockComparison()

def esun_bank_stock():
    """玉山銀行股票爬蟲"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    output_dir = os.path.join(project_root, 'data', 'all_bank_stock')
    os.makedirs(output_dir, exist_ok=True)
    output_filename = os.path.join(output_dir, 'esun_bank.csv')
    
    # 儲存新爬取的股票代碼
    new_stocks = set()

    url = "https://wealth.esunbank.com.tw/usstock/esun/rank9001.xdjhtm"

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"獲取玉山銀行網址時發生錯誤: {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser', from_encoding='ms950')
    data_table = soup.find('table', id='oMainTable')

    if not data_table:
        print("在玉山銀行頁面上找不到資料表格。")
        return


    try:
        with open(output_filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['股票名稱', '代碼'])

            thead = data_table.find('thead')
            original_headers = [th.get_text(strip=True) for th in thead.find_all('th')] if thead else []
            
            stock_name_index = -1
            if original_headers:
                try:
                    stock_name_index = original_headers.index('股票名稱')
                except ValueError:
                    print("在表格中找不到 '股票名稱' 標題。")
                    return
            else:
                print("找不到表格標題。")
                return

            tbody = data_table.find('tbody')
            if tbody:
                for row in tbody.find_all('tr'):
                    cells = row.find_all('td')
                    if not cells or len(cells) <= stock_name_index:
                        continue

                    stock_name = ''
                    ticker = ''

                    stock_name_cell = cells[stock_name_index]
                    stock_name = stock_name_cell.get_text(strip=True)

                    a_tag = stock_name_cell.find('a')
                    if a_tag and 'href' in a_tag.attrs:
                        relative_link = a_tag['href']
                        try:
                            parsed_url = urlparse(relative_link)
                            query_params = parse_qs(parsed_url.query)
                            if 'a' in query_params:
                                ticker = query_params['a'][0]
                        except Exception:
                            ticker = ''

                    if stock_name or ticker:
                        csv_writer.writerow([stock_name, ticker])
                        if ticker:
                            new_stocks.add(ticker)

        return new_stocks

    except Exception as e:
        print(f"解析或寫入玉山銀行檔案時發生意外錯誤: {e}")
        return set()

def mega_bank_stock():
    """兆豐銀行股票爬蟲"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    output_dir = os.path.join(project_root, 'data', 'all_bank_stock')
    os.makedirs(output_dir, exist_ok=True)
    output_filename = os.path.join(output_dir, 'mega_bank.csv')
    
    # 儲存新爬取的股票代碼
    new_stocks = set()

    url = "https://fund.megabank.com.tw/w/stockindexrank.djhtm?a=us&b=1000&c=desc"

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"獲取兆豐銀行網址時發生錯誤: {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser', from_encoding='ms950')
    data_table = soup.find('table', class_='datalist')

    if not data_table:
        print("在兆豐銀行頁面上找不到資料表格。")
        return

    try:
        with open(output_filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            csv_writer = csv.writer(csvfile)
            headers = ['股票名稱', '代碼']
            csv_writer.writerow(headers)
            
            data_rows = data_table.find_all('tr')

            if len(data_rows) > 1:
                for row in data_rows[1:]:
                    cells = [cell.get_text(strip=True) for cell in row.find_all('td')]
                    if len(cells) >= 2:
                        ticker = cells[0]
                        name = cells[1]
                        csv_writer.writerow([name, ticker])
                        if ticker:
                            new_stocks.add(ticker)

        return new_stocks

    except Exception as e:
        print(f"解析或寫入兆豐銀行檔案時發生意外錯誤: {e}")
        return set()

def CTBC_bank_stock():
    """中信銀行股票爬蟲"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    output_dir = os.path.join(project_root, 'data', 'all_bank_stock')
    os.makedirs(output_dir, exist_ok=True)
    output_filename = os.path.join(output_dir, 'CTBC_bank.csv')
    
    # 儲存新爬取的股票代碼
    new_stocks = set()
    
    base_url = "https://ctbcbank.moneydj.com/usstock/ctbcbank/xdjjson/restalphalist.xdjjson?a={}"
    
    try:
        with open(output_filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['股票名稱', '代碼'])

            # 遍歷 A-Z 字母
            for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                url = base_url.format(letter)
                
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                    data = response.json()
                    
                    if data and isinstance(data, list):
                        for item in data:
                            ticker = item.get('id', '').strip()
                            stock_name = item.get('name', '').strip()
                            
                            if stock_name and ticker:
                                csv_writer.writerow([stock_name, ticker])
                                new_stocks.add(ticker)
                        
                    else:
                        print(f"字母 {letter} 沒有資料")
                        
                except requests.exceptions.RequestException as e:
                    print(f"獲取中信銀行字母 {letter} 時發生錯誤: {e}")
                except json.JSONDecodeError as e:
                    print(f"解析中信銀行字母 {letter} JSON 時發生錯誤: {e}")
                except Exception as e:
                    print(f"處理中信銀行字母 {letter} 時發生錯誤: {e}")
        
        return new_stocks

    except Exception as e:
        print(f"爬取中信銀行時發生錯誤: {e}")
        return set()

def tashin_bank_stock():
    """台新銀行股票爬蟲"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    output_dir = os.path.join(project_root, 'data', 'all_bank_stock')
    os.makedirs(output_dir, exist_ok=True)
    output_filename = os.path.join(output_dir, 'tashin_bank.csv')
    
    # 儲存新爬取的股票代碼
    new_stocks = set()
    
    base_url = "https://taishinbankrwd.moneydj.com/w/html/ForeignStockPage.djhtm"
    
    try:
        with open(output_filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['股票名稱', '代碼'])

            page = 1
            while True:
                url = f"{base_url}?a=ALL&Page={page}"

                try:
                    response = requests.get(url)
                    response.raise_for_status()
                except requests.exceptions.RequestException as e:
                    print(f"無法獲取第 {page} 頁。錯誤: {e}。停止。")
                    break
                
                # 根據之前類似網站的經驗使用 'ms950' 編碼
                soup = BeautifulSoup(response.content, 'html.parser', from_encoding='ms950')
                
                # 主要表格似乎是第一個具有 'djclass_table' 類別的表格或通用表格
                data_table = soup.find('table', {'class': 'djclass_table'})
                if not data_table:
                    data_table = soup.find('table') # 備用方案：第一個表格

                if not data_table:
                    print(f"在第 {page} 頁找不到資料表格。爬取完成。")
                    break
                
                rows = data_table.find_all('tr')
                
                # 如果只有標題列存在，我們就完成了
                if len(rows) <= 1:
                    break

                rows_processed = 0
                for row in rows[1:]: # 跳過標題
                    cells = row.find_all('td')
                    if len(cells) > 2:
                        try:
                            # 股票名稱在第二欄，代碼在第三欄
                            stock_name = cells[1].get_text(strip=True)
                            ticker = cells[3].get_text(strip=True) #交易所代碼
                            
                            stock_name = re.sub(r'＜[^＞]+＞', '', stock_name)
                            stock_name = re.sub(r'（[^）]+）', '', stock_name).strip()

                            if stock_name and ticker:
                                csv_writer.writerow([stock_name, ticker])
                                new_stocks.add(ticker)
                                rows_processed += 1
                        except IndexError:
                            continue # 跳過格式錯誤的列
                
                if rows_processed == 0:
                    print(f"在第 {page} 頁沒有處理到有效資料。爬取完成。")
                    break

                page += 1

        return new_stocks

    except Exception as e:
        print(f"爬取台新銀行時發生錯誤: {e}")
        return set()

def ubot_bank_stock():
    """UBOT 銀行股票爬蟲"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    output_dir = os.path.join(project_root, 'data', 'all_bank_stock')
    os.makedirs(output_dir, exist_ok=True)
    output_filename = os.path.join(output_dir, 'ubot_bank.csv')
    
    # 儲存新爬取的股票代碼
    new_stocks = set()
    
    url = "https://www.yesfund.com.tw/w/djjson/overseasRankListJosn.djjson?A=1&B=0"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"獲取 UBOT 網址時發生錯誤: {e}")
        return
    except json.JSONDecodeError:
        print("解析 UBOT 回應中的 JSON 時發生錯誤。")
        return

    try:
        results = data.get("ResultSet", {}).get("Result", [])
        if not results:
            print("在 UBOT 的 JSON 資料中找不到結果。")
            return

        with open(output_filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['股票名稱', '代碼'])

            for item in results:
                stock_name = item.get("V2", "").strip()
                ticker = item.get("V3", "").strip()
                
                stock_name = re.sub(r'＜[^＞]+＞', '', stock_name)
                stock_name = re.sub(r'（[^）]+）', '', stock_name).strip()

                if stock_name and ticker:
                    csv_writer.writerow([stock_name, ticker])
                    new_stocks.add(ticker)
        
        return new_stocks

    except Exception as e:
        print(f"爬取 UBOT 銀行時發生錯誤: {e}")
        return set()

def main():
    """主程式"""
    print("🚀 開始執行所有銀行的股票爬取...")
    
    # 儲存所有比對結果
    comparison_results = []
    
    # 執行各銀行爬蟲並收集結果
    banks = [
        ("esun", esun_bank_stock, "玉山銀行"),
        ("mega", mega_bank_stock, "兆豐銀行"),
        ("CTBC", CTBC_bank_stock, "中信銀行"),
        #("tashin", tashin_bank_stock, "台新銀行"),
        ("ubot", ubot_bank_stock, "UBOT 銀行")
    ]
    
    for bank_code, bank_func, bank_name in banks:
        print(f"\n🏦 正在處理 {bank_name}...")
        
        # 1. 先讀取舊的CSV (用獨立的變數)
        old_stocks = stock_comparison.load_old_data(bank_code)
        print(f"   舊資料: {len(old_stocks)} 檔")
        
        # 2. 開始爬蟲並存入CSV
        new_stocks = bank_func()
        print(f"   新資料: {len(new_stocks)} 檔")
        
        if new_stocks:
            # 3. 比對舊的CSV(這裡是變數)比較新爬蟲的內容
            added_stocks = new_stocks - old_stocks
            removed_stocks = old_stocks - new_stocks
            
            comparison = {
                'bank_name': bank_code,
                'old_count': len(old_stocks),
                'new_count': len(new_stocks),
                'added': list(added_stocks),
                'removed': list(removed_stocks),
                'total_change': len(added_stocks) - len(removed_stocks)
            }
            comparison_results.append(comparison)
            print(f"   {bank_name}比對完成: 新增 {len(comparison['added'])} 檔, 移除 {len(comparison['removed'])} 檔")

    # 4. 產生差異另存一個CSV紀錄上下架
    if comparison_results:
        stock_comparison.save_comparison_log(comparison_results)
    else:
        print("❌ 沒有比對結果可儲存")
    

if __name__ == "__main__":
    main() 