import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai
from main import get_market_summary

# 載入環境變數
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 初始化 Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """處理 /start 指令"""
    await update.message.reply_text('您好！我是您的專屬理財幕僚。您可以直接傳送新聞、股票代號或是您的筆記給我，我會立刻為您分析。\n您也可以隨時輸入 /market 來獲取最新的市場快照與分析。')

async def market(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """處理 /market 指令，獲取即時市場數據並分析"""
    wait_msg = await update.message.reply_text("📊 正在為您搜集最新台、美股與總經數據，請稍候...")
    
    try:
        # 取得市場摘要
        market_data_summary = get_market_summary()
        
        # 編輯提示訊息，讓使用者知道現在正在分析
        await wait_msg.edit_text("🤖 數據搜集完畢！理財幕僚正在進行深度分析中...")
        
        # 呼叫 Gemini 進行大盤分析
        prompt = f"這是我今天整理的台美股與總經報價摘要：\n\n{market_data_summary}\n\n請用繁體中文，扮演我的專屬理財幕僚。根據以上數據，給予我簡短且具洞察力的投資重點提醒。\n請控制在 150 字以內，列點說明。"
        response = model.generate_content(prompt)
        
        final_message = f"📊 *今日投資快照*\n\n{market_data_summary}\n🤖 *理財幕僚分析*\n{response.text}"
        
        # 由於內容可能有未跳脫的 Markdown，此處若不想處理例外，直接使用純文字
        await wait_msg.edit_text(final_message)
        
    except Exception as e:
        await wait_msg.edit_text(f"擷取市場資訊時發生錯誤 ❌：{str(e)}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """處理一般文字訊息"""
    user_text = update.message.text
    
    # 告訴使用者 AI 正在思考（因為 Gemini 可能會需要幾秒鐘的時間）
    wait_msg = await update.message.reply_text("🤖 收到您的訊息，理財幕僚正在分析中，請稍候...")
    
    try:
        # 設計給幕僚的專屬 Prompt，並加入使用者傳來的對話
        prompt = f"你現在是我的專屬理財幕僚。請根據我傳送的以下訊息，給予專業且精要的繁體中文分析與建議，並請符合價值投資與防禦型風險控管的角度。請盡量控制在重點，避免過於冗長：\n\n{user_text}"
        
        # 呼叫 Gemini
        response = model.generate_content(prompt)
        text = response.text
        
        # 編輯原本的「思考中」訊息，如果超過 Telegram 字數限制 (4096字元) 則分段送出
        if len(text) < 4000:
            try:
                await wait_msg.edit_text(text, parse_mode="Markdown")
            except:
                # 避免 Markdown 語法解析錯誤導致崩潰，改為純文字
                await wait_msg.edit_text(text)
        else:
            await wait_msg.edit_text(text[:4000])
            for i in range(4000, len(text), 4000):
                await update.message.reply_text(text[i:i+4000])
                
    except Exception as e:
        # 更新原先那則「思考中」的訊息顯示錯誤
        await wait_msg.edit_text(f"分析時發生錯誤 ❌：{str(e)}")

def main() -> None:
    """全天候監聽 Telegram 訊息的主程式"""
    if not TELEGRAM_BOT_TOKEN:
        print("未設定 TELEGRAM_BOT_TOKEN")
        return

    # 建立 Application 並傳入 Token
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # 註冊處理器 (Handlers)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("market", market))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # 開始輪詢 (Polling)，這樣程式就不會結束，會一直等待新訊息
    print("🤖 互動式理財機器人已經啟動！正在監聽來自 Telegram 的訊息... (在終端機按 Ctrl+C 可停止。)")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
