# 投資理財助理 (Investment Assistant) 階段二與三：深度整合計畫

## 1. 目標回顧
經過「階段一」的實作，我們已經成功搭建起一個基礎的 Telegram 機器人，具備以下能力：
1.  **被動推播 (main.py)**：定時抓取特定 ETF (SMH, SHLD, VPU, BOTZ) 的價格，並透過 Gemini 產出分析摘要，推送給您。
2.  **主動對答 (interactive_bot.py)**：常駐執行，隨時接收您的文字（或筆記），丟給 Gemini 分析後回傳精要見解，且已解決字數過長的問題。

為完成您的最終目標，接下來的重點將放在**擴充資料源（Data Sources）**，也就是階段二。

## 2. 階段二 擴充開發計畫 (Proposed Changes)

我們將新增兩支專門負責爬取數據的模組（Data Fetchers），並將它們整合進現有的 `main.py` 與 `interactive_bot.py` 中。

### [NEW] `data_fetchers/goodinfo_crawler.py`
負責爬取 [Goodinfo!台灣股市資訊網](https://goodinfo.tw/tw/index.asp) 的台股基本面數據。
*   **預計實作**：使用 `requests` 加上適當的 Headers (模擬瀏覽器) 來獲取 HTML，並用 `BeautifulSoup` 或是 `pandas.read_html` 萃取表格資料。
*   **目標指標**：輸入台股代號 (如 2330, 892, 881)，回傳其：
    *   最新收盤價
    *   EPS (每股盈餘)
    *   本益比 (P/E)
    *   殖利率
    *   *(進階)* 淨利率與負債比

### [NEW] `data_fetchers/macro_economy.py`
負責抓取美國與全球的總體經濟指標。您筆記提及「實時失業率、美聯儲利率等重要基準面」。
*   **預計實作**：串接 **FRED API** (Federal Reserve Economic Data)。這是最穩定且免費的官方總經數據庫。
*   **目標指標**：
    *   美國失業率 (UNRATE)
    *   聯邦基金有效利率 (FEDFUNDS)
*   *備註：我們需要再申請一把免費的 FRED API Key 寫入 `.env`。*

### [MODIFY] `main.py`
*   **修改內容**：在每日早晨的推播中，除了 ETF 報價外，加入從 `goodinfo_crawler.py` 取得的台股關注標的現況，以及從 `macro_economy.py` 取得的最新總經數據。
*   **Prompt 優化**：將這些多元數據統整成一個大字串餵給 Gemini，並在 Prompt 中嚴格要求 AI **「根據 P/E 判斷是否過熱、根據失業率與利率判斷 Fed 態度是鷹是鴿」**。

### [MODIFY] `interactive_bot.py`
*   **修改內容**：讓對話機器人具有「呼叫工具 (Tool Calling)」的能力，或是在背後預先載入當日所有數據。當您在 Telegram 詢問「台積電現在可以買嗎？」時，程式會先去呼叫 `goodinfo_crawler` 取得 2330 最新資料，再連同您的問題一起丟給 Gemini 分析。

## 3. 驗證與測試計畫 (Verification Plan)

### 自動化測試
1.  **模組獨立測試**：分別執行 `python data_fetchers/goodinfo_crawler.py` 和 `python data_fetchers/macro_economy.py`，確認終端機能正確印出 2330 的本益比與美國最新失業率。
2.  **整合推播測試**：執行 `python main.py`，確認 Telegram 收到一則包含「美股 ETF、台股基本面、總體經濟」三大面向的長篇綜合分析。

### 手動驗證
1.  **防呆測試**：在 Telegram 對機器人輸入錯誤的台股代號 (例如 9999)，確認系統不會崩潰，且能友善回覆查無此檔股票。
2.  **對答品質測試**：手動傳送筆記中關於「防禦型投資」的段落給機器人，並觀察它整合台美股最新數據後，是否能給出符合「高利率環境防範融資壓力」等條件的實用建議。

## 4. [User Review Required] 🚨
由於我們需要抓取美國聯準會的總經數據，會使用到官方的 FRED 服務：
1.  我會寫一段腳本教您如何自動/手動申請 **FRED API Key**。
2.  關於台股的部分，Goodinfo 有時會阻擋機器爬蟲，我會盡量加上偽裝機制。如果在伺服器上被擋，我們可能需要改用開放資料如 `FinMind`。
請您確認上述的「階段二」架構是否符合您的期待？如果沒問題，我們就可以開始動工寫爬蟲了！
