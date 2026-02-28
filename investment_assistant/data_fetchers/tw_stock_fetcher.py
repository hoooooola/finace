import yfinance as yf

def get_stock_basic_info(stock_id):
    """
    使用 yfinance 抓取台股基本面資訊 (股價、EPS、本益比、殖利率)
    為了相容 yfinance，台股代碼後方需要加上 .TW (上市) 或 .TWO (上櫃)
    預設先嘗試 .TW，若失敗再嘗試 .TWO
    """
    # 判斷是否已經有後綴
    if not stock_id.endswith(".TW") and not stock_id.endswith(".TWO"):
        tw_symbol = f"{stock_id}.TW"
    else:
        tw_symbol = stock_id
        
    print(f"📡 準備抓取台股 [{tw_symbol}] 基本面資訊...")
    
    try:
        ticker = yf.Ticker(tw_symbol)
        info = ticker.info
        
        # 如果找不到資料，可能是上櫃股票 (.TWO)
        if not info or 'longName' not in info:
            if tw_symbol.endswith(".TW"):
                tw_symbol = f"{stock_id}.TWO"
                print(f"⚠️ 找不到上市資料，嘗試嘗試上櫃 [{tw_symbol}]...")
                ticker = yf.Ticker(tw_symbol)
                info = ticker.info
        
        if not info or ('regularMarketPrice' not in info and 'currentPrice' not in info):
             return {"symbol": str(stock_id), "error": "找不到該檔股票資料"}

        # 整理基本面資料
        price = info.get('currentPrice') or info.get('regularMarketPrice', 'N/A')
        eps = info.get('trailingEps', 'N/A')
        pe = info.get('trailingPE', 'N/A')
        dividend_yield = info.get('dividendYield', 'N/A')
        
        # 殖利率加上百分比號
        if isinstance(dividend_yield, (int, float)):
            dividend_yield = f"{round(dividend_yield, 2)}%"

        result = {
            "symbol": str(stock_id),
            "price": price,
            "eps": eps,
            "pe": pe,
            "yield": dividend_yield,
            "name": info.get('longName', '')
        }
        return result
        
    except Exception as e:
        return {"symbol": str(stock_id), "error": str(e)}

if __name__ == "__main__":
    # 測試抓取幾檔您關注的台股 (台積電 2330, 富邦台灣核心半導體 00892)
    test_stocks = ["2330", "00892"]
    for sid in test_stocks:
        data = get_stock_basic_info(sid)
        print(f"結果: {data}")
