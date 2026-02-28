import os
import requests
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def get_chat_id():
    """取得最近與 Bot 互動的使用者的 Chat ID"""
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "your_telegram_bot_token_here":
        print("錯誤：找不到有效的 TELEGRAM_BOT_TOKEN")
        return

    print("正在向 Telegram 取得最近的訊息...")
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    
    try:
        response = requests.get(url).json()
        if response.get("ok"):
            results = response.get("result", [])
            if not results:
                print("\n找不到任何對話紀錄。")
                print(">>> 請先打開 Telegram，去和您的機器人說聲嗨（或按下 /start）！然後再執行一次這個腳本。")
            else:
                # 取最後一筆訊息的 chat id
                last_message = results[-1]
                if "message" in last_message:
                    chat_id = last_message["message"]["chat"]["id"]
                    first_name = last_message["message"]["chat"].get("first_name", "User")
                    print(f"\n🎉 成功找到！！")
                    print(f"您的名稱是：{first_name}")
                    print(f"您的 Chat ID 是：{chat_id}")
                    print("\n>>> 請將這串數字複製下來告訴我，或是直接存入 .env 中的 TELEGRAM_CHAT_ID 變數！")
                else:
                    print("收到的更新不是一般訊息格式。")
        else:
            print(f"API 請求失敗: {response}")
    except Exception as e:
        print(f"發生錯誤: {str(e)}")

if __name__ == "__main__":
    get_chat_id()
