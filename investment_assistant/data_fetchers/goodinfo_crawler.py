import requests
from bs4 import BeautifulSoup
import time
import random

def get_stock_basic_info(stock_id):
    """
    從 Goodinfo!台灣股市資訊網 爬取台股基本面資訊
    包含：收盤價、本益比、EPS等
    """
    print(f"📡 準備抓取台股 [{stock_id}] 基本面資訊...")
    url = f"https://goodinfo.tw/tw/StockDetail.asp?STOCK_ID={stock_id}"
    
    # 模擬真人瀏覽器，避免被阻擋
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://goodinfo.tw/tw/index.asp"
    }
    
    # 隨機延遲，尊重對方伺服器，也避免被當成惡意爬蟲
    time.sleep(random.uniform(1.5, 3.5))
    
    try:
        # 特別注意 Goodinfo 似乎需要設定 timeout
        res = requests.get(url, headers=headers, timeout=10)
        res.encoding = 'utf-8'
        
        if res.status_code != 200:
            return {"symbol": str(stock_id), "error": f"請求失敗，狀態碼: {res.status_code}"}
            
        soup = BeautifulSoup(res.text, "html.parser")
        
        # Goodinfo 網頁結構經常變動，這裡用比較通用的字串比對查找
        result = {"symbol": str(stock_id)}
        
        # 尋找所有表格儲存格
        tds = soup.find_all("td")
        for i, td in enumerate(tds):
            text = td.get_text(strip=True)
            if text == "成交價":
                result["price"] = tds[i+1].get_text(strip=True)
            elif text == "本益比":
                result["pe"] = tds[i+1].get_text(strip=True)
            elif text == "BPS(元)":
                result["bps"] = tds[i+1].get_text(strip=True)
            elif "稅後EPS" in text and "(元)" in text and len(text) < 15:
                # EPS 比較難抓，因為表格名稱很長
                result["eps"] = tds[i+1].get_text(strip=True)
                
        # 稍微清理空值
        if "eps" not in result: result["eps"] = "N/A"
        if "pe" not in result: result["pe"] = "N/A"
        if "price" not in result: result["price"] = "N/A"
        
        return result
        
    except Exception as e:
        return {"symbol": str(stock_id), "error": str(e)}

if __name__ == "__main__":
    # 測試抓取幾檔您關注的台股 (例如：台積電 2330, 富邦台灣核心半導體 00892)
    test_stocks = ["2330", "00892"]
    for sid in test_stocks:
        data = get_stock_basic_info(sid)
        print(f"結果: {data}")
