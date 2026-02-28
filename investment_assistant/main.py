import os
import requests
import yfinance as yf
from dotenv import load_dotenv
import google.generativeai as genai

from data_fetchers.tw_stock_fetcher import get_stock_basic_info
from data_fetchers.macro_economy import get_fred_data
from data_fetchers.export_to_json import export_data_to_json

# 載入環境變數
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

def get_etf_data(ticker_symbol):
    """取得 ETF 基本資訊"""
    try:
        ticker = yf.Ticker(ticker_symbol)
        data = ticker.history(period="1d")
        if not data.empty:
            closing_price = data['Close'].iloc[-1]
            return {"symbol": ticker_symbol, "price": round(closing_price, 2)}
        return {"symbol": ticker_symbol, "error": "No data"}
    except Exception as e:
        return {"symbol": ticker_symbol, "error": str(e)}

def send_telegram_message(message):
    """發送訊息到 Telegram"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("未設定 Telegram Token 或 Chat ID，無法發送訊息。")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        res = requests.post(url, json=payload)
        if res.status_code == 200:
            print("📤 成功推播訊息至 Telegram！")
        else:
            # 如果因為 Markdown 解析失敗導致 400，嘗試退回純文字傳送
            if res.status_code == 400 and "parse entities" in res.text.lower():
                print("⚠️ Markdown 解析失敗，嘗試以純文字傳送...")
                payload.pop("parse_mode", None)
                res2 = requests.post(url, json=payload)
                if res2.status_code == 200:
                    print("📤 成功推播純文字訊息至 Telegram！")
                else:
                    print(f"發送純文字 Telegram 失敗，狀態碼：{res2.status_code}, 回應：{res2.text}")
            else:
                print(f"發送 Telegram 失敗，狀態碼：{res.status_code}, 回應：{res.text}")
    except Exception as e:
        print(f"發送訊息發生例外錯誤：{str(e)}")

def get_market_summary():
    """獲取台、美股與總經最新數據的字串摘要"""
    market_data_summary = "【美股 ETF 觀察清單】\n"
    etfs_to_track = ["SMH", "SHLD", "VPU", "BOTZ"]
    for etf in etfs_to_track:
        result = get_etf_data(etf)
        if "price" in result:
            market_data_summary += f"- [{result['symbol']}] 最新收盤價: ${result['price']}\n"
        else:
            market_data_summary += f"- [{result['symbol']}] 取得資料失敗: {result['error']}\n"
            
    market_data_summary += "\n【台股 個股基本面觀察】\n"
    tw_stocks_to_track = ["2330", "00892", "00881"]
    for stock in tw_stocks_to_track:
        tw_res = get_stock_basic_info(stock)
        if "error" not in tw_res:
            market_data_summary += f"- [{tw_res['symbol']}] {tw_res.get('name', '')} | 股價: {tw_res['price']} | P/E: {tw_res['pe']} | EPS: {tw_res['eps']} | 殖利率: {tw_res['yield']}\n"
        else:
            market_data_summary += f"- [{stock}] 取得資料失敗: {tw_res['error']}\n"
            
    market_data_summary += "\n【美國 總體經濟指標】\n"
    for indicator, series_id in [("失業率", "UNRATE"), ("基準利率", "FEDFUNDS")]:
        eco_res = get_fred_data(series_id)
        if "error" not in eco_res:
            market_data_summary += f"- {indicator} ({eco_res['date']}): {eco_res['value']}\n"
        else:
            market_data_summary += f"- {indicator} 取得失敗: {eco_res['error']}\n"
            
    return market_data_summary

def main():
    print("啟動投資理財助理...")
    
    market_data_summary = get_market_summary()

    print("\n--- 今日整理好的市場觀察數據 ---")
    print(market_data_summary)

    # 測試 Gemini API
    print("\n--- 測試 Gemini AI 分析功能 ---")
    if GEMINI_API_KEY and GEMINI_API_KEY != "your_google_gemini_api_key_here":
        try:
            prompt = f"這是我今天整理的台美股與總經報價摘要：\n\n{market_data_summary}\n\n請用繁體中文，扮演我的專屬理財幕僚。根據以上數據，給予我簡短且具洞察力的本日投資重點提醒。\n**思考方針**：\n1. 關注半導體、國防科技與公用事業的輪動。\n2. 若失業率上升或基準利率變動，評估防禦型機會。\n3. 若台股本益比(P/E)過高，提醒估值風險。\n請控制在 150 字以內，列點說明。"
            
            response = model.generate_content(prompt)
            ai_text = response.text
            print(f"🤖 理財幕僚分析：\n{ai_text}")
            
            # 將生數據與 AI 分析匯出為給網頁用的 data.json
            export_data_to_json(ai_text)
            
            # 推播訊息至 Telegram
            dashboard_url = "https://hoooooola.github.io/finace"
            final_message = f"📊 *今日投資早報*\n\n{market_data_summary}\n🤖 *理財幕僚分析*\n{ai_text}\n\n👉 [點此開啟您的專屬視覺化圖表儀表板]({dashboard_url})"
            send_telegram_message(final_message)
            
        except Exception as e:
            print(f"Gemini API 呼叫失敗： {e}")
    else:
        print("未設定有效的 Gemini API Key。")

    print("\n系統執行完畢！")

if __name__ == "__main__":
    main()
