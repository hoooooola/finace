# 專屬理財幕僚 (Investment Assistant)

這是一個基於 Google Gemini 與 Telegram Bot API 的自動化理財助理。它能夠每天定時爬取台、美股的基本面與報價，結合總體經濟指標，透過 AI 產出專屬的投資重點摘要，並推播至您的手機。

## 核心功能
* **每日推播 (`main.py`)**：定時執行，抓取自訂的關注名單與總經指標，產出並推播早報給您。
* **互動對答 (`interactive_bot.py`)**：常駐執行，隨時接收您的投資筆記與疑問，提供符合防禦型價值的投資見解。
* **自動排程 (GitHub Actions)**：透過 `.github/workflows/daily_report.yml`，每週一到週五早上準時推播，無需本機伺服器。

## 部署至 GitHub Actions 教學 (全自動每日推播)

要讓 GitHub 幫您每天自動跑程式發送早報，請先將此資料夾上傳至您個人的 GitHub Repository。

### 1. 設定 Repository Secrets
因為我們不能把私密的 API Key (像是 `.env` 裡面的那些密碼) 直接上傳到公開的 GitHub 上，我們需要把它們存在 GitHub 的保險箱裡：

1. 進入您剛剛建立的 GitHub Repository 網頁。
2. 點擊上方的 **Settings** (設定)。
3. 在左側選單找到 **Secrets and variables** -> **Actions**。
4. 點擊右上的 **New repository secret**，依序新增以下四個變數（名稱必須一模一樣，值請參考您的 `.env` 檔案）：
   * `TELEGRAM_BOT_TOKEN`
   * `TELEGRAM_CHAT_ID`
   * `GEMINI_API_KEY`
   * `FRED_API_KEY`

### 2. 測試手動觸發
1. 設定完畢後，點擊上方的 **Actions** 頁籤。
2. 在左側點選我們寫好的 **Daily Investment Market Report**。
3. 點擊右側的 **Run workflow** -> 綠色的 **Run workflow** 按鈕。
4. 如果設定正確，大約 30 秒後您的 Telegram 就會收到由 GitHub 伺服器發送的最新市場早報了！🎉

---
**免責聲明**：本專案產出之內容均由 AI 產生，僅供個人學習與輔助參考，不構成任何真實投資建議。
