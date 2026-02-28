import os
import requests
from dotenv import load_dotenv

load_dotenv()
FRED_API_KEY = os.getenv("FRED_API_KEY")

def get_fred_data(series_id):
    """
    從 FRED 取得最新一筆總體經濟指標
    :param series_id:
        - 'UNRATE': 美國失業率
        - 'FEDFUNDS': 聯邦基金有效利率
    """
    if not FRED_API_KEY or FRED_API_KEY == "your_fred_api_key_here":
        return {"series_id": series_id, "error": "尚未設定 FRED_API_KEY"}
        
    print(f"📡 準備抓取 FRED 經濟指標 [{series_id}]...")
    
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "sort_order": "desc",
        "limit": 1  # 只取最新的一筆資料
    }
    
    try:
        res = requests.get(url, params=params)
        if res.status_code == 200:
            data = res.json()
            observations = data.get("observations", [])
            if observations:
                latest = observations[0]
                return {
                    "series_id": series_id,
                    "date": latest.get("date"),
                    "value": f"{latest.get('value')}%"
                }
            else:
                return {"series_id": series_id, "error": "回傳資料格式有誤"}
        else:
            return {"series_id": series_id, "error": f"API 請求失敗: {res.status_code}"}
            
    except Exception as e:
        return {"series_id": series_id, "error": str(e)}

if __name__ == "__main__":
    # 測試
    print(get_fred_data("UNRATE")) # 失業率
    print(get_fred_data("FEDFUNDS")) # 基準利率
