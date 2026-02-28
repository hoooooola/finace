import json
import os
import sys
from datetime import datetime

# 將專案根目錄加入路徑，讓子目錄的腳本能正確匯入套件
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_fetchers.tw_stock_fetcher import get_stock_basic_info
from data_fetchers.macro_economy import get_fred_data
# 為了不重複定義，我們將從 main.py 引進 yfinance 爬蟲，
# 但為避免循環 import，我們在這裡重新簡單定義 get_etf_data，或是之後將其搬移。
import yfinance as yf

def get_etf_data(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        data = ticker.history(period="3mo")
        if not data.empty:
            closing_price = data['Close'].iloc[-1]
            history = [{"date": d.strftime("%Y-%m-%d"), "price": round(r['Close'], 2)} for d, r in data.iterrows()]
            return {"symbol": ticker_symbol, "price": round(closing_price, 2), "history": history}
        return {"symbol": ticker_symbol, "error": "No data"}
    except Exception as e:
        return {"symbol": ticker_symbol, "error": str(e)}

def export_data_to_json(ai_analysis_text):
    """
    將今日爬取的市場資料與 AI 分析整合成一份 JSON，存入 public 資料夾供網頁讀取
    """
    print("💾 準備匯出資料至 public/data.json ...")
    
    # 建立回傳的資料結構
    dashboard_data = {
        "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ai_analysis": ai_analysis_text,
        "market_data": {
            "etfs": [],
            "tw_stocks": [],
            "macro_economy": []
        }
    }
    
    # 1. 收集 ETF 資料
    etfs_to_track = ["SMH", "SHLD", "VPU", "BOTZ"]
    for etf in etfs_to_track:
        res = get_etf_data(etf)
        if "price" in res:
            dashboard_data["market_data"]["etfs"].append(res)
            
    # 2. 收集台股資料
    tw_stocks_to_track = ["2330", "00892", "00881"]
    for stock in tw_stocks_to_track:
        res = get_stock_basic_info(stock)
        if "error" not in res:
            dashboard_data["market_data"]["tw_stocks"].append(res)
            
    # 3. 收集美國總經資料
    for indicator, series_id in [("美國失業率", "UNRATE"), ("聯邦基準利率", "FEDFUNDS")]:
        res = get_fred_data(series_id)
        if "error" not in res:
            # 加入中文名稱方便前端顯示
            res["name"] = indicator
            dashboard_data["market_data"]["macro_economy"].append(res)
            
    # 將資料寫入 public/data.json
    os.makedirs("public", exist_ok=True)
    with open("public/data.json", "w", encoding="utf-8") as f:
        json.dump(dashboard_data, f, ensure_ascii=False, indent=2)
        
    print("✅ 資料匯出完成！")
    return dashboard_data

if __name__ == "__main__":
    # 獨立執行測試
    export_data_to_json("這是一段測試用的 AI 分析文案...")
