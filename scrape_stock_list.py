import requests
from bs4 import BeautifulSoup
import csv
import os
from urllib.parse import urlparse, parse_qs
import re
import json

def esun_bank_stock():
    # Get the absolute path of the directory where the script is located.
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the output path and create the directory if it doesn't exist.
    output_dir = os.path.join(script_dir, 'all_bank_stock')
    os.makedirs(output_dir, exist_ok=True)
    output_filename = os.path.join(output_dir, 'esun_bank.csv')

    # The URL of the page to scrape
    url = "https://wealth.esunbank.com.tw/usstock/esun/rank9001.xdjhtm"

    print(f"Fetching data from {url}...")

    # Send a GET request to the page
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return

    # The website content is often encoded in 'ms950' (a superset of 'big5').
    # Using response.content and letting BeautifulSoup handle the decoding is more robust.
    soup = BeautifulSoup(response.content, 'html.parser', from_encoding='ms950')

    # Find the main data table using its ID, which is a more reliable method.
    data_table = soup.find('table', id='oMainTable')

    if not data_table:
        print("Could not find the data table with id='oMainTable' on the page.")
        return

    print("Found data table. Parsing and saving data...")

    try:
        with open(output_filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            csv_writer = csv.writer(csvfile)

            # Write the desired headers directly.
            csv_writer.writerow(['股票名稱', '代碼'])

            # We still need to find the original headers to locate the '股票名稱' column index.
            original_headers = []
            thead = data_table.find('thead')
            if thead:
                original_headers = [th.get_text(strip=True) for th in thead.find_all('th')]

            stock_name_index = -1
            if original_headers:
                try:
                    stock_name_index = original_headers.index('股票名稱')
                except ValueError:
                    print("Could not find '股票名稱' header in the table.")
                    return
            else:
                print("Could not find table headers.")
                return

            # Extract data rows from the tbody section.
            tbody = data_table.find('tbody')
            if tbody:
                for row in tbody.find_all('tr'):
                    cells = row.find_all('td')
                    if not cells or len(cells) <= stock_name_index:
                        continue

                    stock_name = ''
                    ticker = ''

                    # Extract stock name text from the correct cell.
                    stock_name_cell = cells[stock_name_index]
                    stock_name = stock_name_cell.get_text(strip=True)

                    # Extract ticker from the link in the same cell.
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

                    # Write only the stock name and ticker to the CSV.
                    if stock_name or ticker:
                        csv_writer.writerow([stock_name, ticker])

        print(f"Data successfully scraped and saved to {output_filename}")

    except IOError as e:
        print(f"Error writing to file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during parsing or file writing: {e}")

def mega_bank_stock():
    # Get the absolute path of the directory where the script is located.
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the output path and create the directory if it doesn't exist.
    output_dir = os.path.join(script_dir, 'all_bank_stock')
    os.makedirs(output_dir, exist_ok=True)
    output_filename = os.path.join(output_dir, 'mega_bank.csv')

    # The URL of the page to scrape
    url = "https://fund.megabank.com.tw/w/stockindexrank.djhtm?a=us&b=1000&c=desc"

    print(f"Fetching data from {url}...")

    # Send a GET request to the page
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return

    # The website content seems to be encoded in 'ms950' or 'big5'.
    soup = BeautifulSoup(response.content, 'html.parser', from_encoding='ms950')

    # Find the main data table. A common class for such tables is 'datalist'.
    data_table = soup.find('table', class_='datalist')

    if not data_table:
        print("Could not find the data table on the page.")
        return

    print("Found data table. Parsing and saving data...")

    try:
        with open(output_filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            csv_writer = csv.writer(csvfile)

            # Standardize headers to '股票名稱' (Stock Name) and '代碼' (Ticker).
            headers = ['股票名稱', '代碼']
            csv_writer.writerow(headers)
            
            # Find all `tr` elements in the table and skip the first one (header row).
            # This is more robust as some tables might not have a `tbody` element.
            data_rows = data_table.find_all('tr')

            if len(data_rows) > 1:
                for row in data_rows[1:]: # Skip header row
                    cells = [cell.get_text(strip=True) for cell in row.find_all('td')]
                    # Ensure the row has at least two cells for Ticker and Name.
                    if len(cells) >= 2:
                        ticker = cells[0]
                        name = cells[1]
                        # Write in the standardized order: Name, Ticker.
                        csv_writer.writerow([name, ticker])

        print(f"Data successfully scraped and saved to {output_filename}")

    except IOError as e:
        print(f"Error writing to file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during parsing or file writing: {e}")

def CTBC_bank_stock():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, 'all_bank_stock')
    os.makedirs(output_dir, exist_ok=True)
    output_filename = os.path.join(output_dir, 'CTBC_bank.csv')
    url = "https://ctbcbank.moneydj.com/usstock/ctbcbank/rank0001.xdjhtm"

    print(f"Fetching data from {url}...")

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser', from_encoding='ms950')
    data_table = soup.find('table', id='oMainTable')

    if not data_table:
        print("Could not find the data table on the CTBC Bank page.")
        return

    print("Found data table. Parsing and saving data for CTBC Bank...")

    try:
        with open(output_filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['股票名稱', '代碼'])

            thead = data_table.find('thead')
            original_headers = [th.get_text(strip=True) for th in thead.find_all('th')] if thead else []
            
            stock_name_index = -1
            try:
                stock_name_index = original_headers.index('股票名稱')
            except ValueError:
                stock_name_index = 4 # Fallback based on observed structure

            data_rows = data_table.find_all('tr')
            if len(data_rows) > 1:
                for row in data_rows[1:]:
                    cells = row.find_all('td')
                    if len(cells) > stock_name_index:
                        stock_name_cell = cells[stock_name_index]
                        a_tag = stock_name_cell.find('a')
                        if a_tag:
                            ticker = ''
                            href = a_tag.get('href', '')
                            if href:
                                parsed_url = urlparse(href)
                                query_params = parse_qs(parsed_url.query)
                                ticker = query_params.get('a', [''])[0]
                            
                            raw_name = a_tag.get_text(strip=True)
                            stock_name = re.sub(r'＜[^＞]+＞', '', raw_name)
                            stock_name = re.sub(r'（[^）]+）', '', stock_name).strip()
                            
                            if stock_name and ticker:
                                csv_writer.writerow([stock_name, ticker])
        
        print(f"Data successfully scraped and saved to {output_filename}")

    except Exception as e:
        print(f"An error occurred during scraping CTBC bank: {e}")

def tashin_bank_stock():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, 'all_bank_stock')
    os.makedirs(output_dir, exist_ok=True)
    output_filename = os.path.join(output_dir, 'tashin_bank.csv')
    
    base_url = "https://taishinbankrwd.moneydj.com/w/html/ForeignStockPage.djhtm"
    
    print("Fetching data from Taishin Bank...")

    try:
        with open(output_filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['股票名稱', '代碼'])

            page = 1
            while True:
                url = f"{base_url}?a=ALL&Page={page}"
                print(f"Scraping page {page}: {url}")

                try:
                    response = requests.get(url)
                    response.raise_for_status()
                except requests.exceptions.RequestException as e:
                    print(f"Could not fetch page {page}. Error: {e}. Stopping.")
                    break
                
                # Use 'ms950' encoding based on previous experience with similar sites
                soup = BeautifulSoup(response.content, 'html.parser', from_encoding='ms950')
                
                # The main table seems to be the first one with class 'djclass_table' or a generic table
                data_table = soup.find('table', {'class': 'djclass_table'})
                if not data_table:
                    data_table = soup.find('table') # Fallback to the first table

                if not data_table:
                    print(f"No data table found on page {page}. Finished scraping.")
                    break
                
                rows = data_table.find_all('tr')
                
                # If only header row is present, we are done
                if len(rows) <= 1:
                    print(f"No data rows found on page {page}. Finished scraping.")
                    break

                rows_processed = 0
                for row in rows[1:]: # Skip header
                    cells = row.find_all('td')
                    if len(cells) > 2:
                        try:
                            # Stock name is in the second column, ticker in the third.
                            stock_name = cells[1].get_text(strip=True)
                            ticker = cells[3].get_text(strip=True) #交易所代碼
                            
                            stock_name = re.sub(r'＜[^＞]+＞', '', stock_name)
                            stock_name = re.sub(r'（[^）]+）', '', stock_name).strip()

                            if stock_name and ticker:
                                csv_writer.writerow([stock_name, ticker])
                                rows_processed += 1
                        except IndexError:
                            continue # Skip malformed rows
                
                if rows_processed == 0:
                    print(f"No valid data processed on page {page}. Finished scraping.")
                    break

                page += 1

        print(f"Data successfully scraped and saved to {output_filename}")

    except Exception as e:
        print(f"An error occurred during scraping Taishin bank: {e}")

def ubot_bank_stock():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, 'all_bank_stock')
    os.makedirs(output_dir, exist_ok=True)
    output_filename = os.path.join(output_dir, 'ubot_bank.csv')
    
    url = "https://www.yesfund.com.tw/w/djjson/overseasRankListJosn.djjson?A=1&B=0"
    
    print(f"Fetching data for UBOT from {url}...")

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return
    except json.JSONDecodeError:
        print("Error decoding JSON from response.")
        return

    try:
        results = data.get("ResultSet", {}).get("Result", [])
        if not results:
            print("No results found in JSON data for UBOT.")
            return

        with open(output_filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['股票名稱', '代碼'])

            for item in results:
                # V2 is the name, V3 is the ticker
                stock_name = item.get("V2", "").strip()
                ticker = item.get("V3", "").strip()
                
                # Basic cleaning of the name, similar to other functions
                stock_name = re.sub(r'＜[^＞]+＞', '', stock_name)
                stock_name = re.sub(r'（[^）]+）', '', stock_name).strip()

                if stock_name and ticker:
                    csv_writer.writerow([stock_name, ticker])
        
        print(f"Data successfully scraped and saved to {output_filename}")

    except Exception as e:
        print(f"An error occurred during scraping UBOT bank: {e}")

if __name__ == "__main__":
    #esun_bank_stock()
    #mega_bank_stock()
    #CTBC_bank_stock()
    tashin_bank_stock()
    #ubot_bank_stock()