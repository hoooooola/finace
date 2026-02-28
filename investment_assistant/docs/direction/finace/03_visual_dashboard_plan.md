# 投資理財助理 (Investment Assistant) 階段四：Visual Dashboard (視覺化網頁 UI) 計畫

## 1. 目標回顧
經過前三個階段的實作，我們已經獲得了非常穩定的核心引擎：
*   ✅ Python 每日自動收集台/美股報價、基本面 (P/E)、聯準會失業率。
*   ✅ Google Gemini AI 進行大盤風險分析。
*   ✅ Telegram Bot 每日早晨精要推播，並可雙向互動。

**階段四的終極目標：** 將生硬的數字與文字，轉換為一目了然的「**圖表化網頁 (Visual Dashboard)**」，讓您能用看盤軟體的體驗，深度檢視自己的理財策略，並且**完全免費託管於 GitHub Pages 上**。

## 2. 階段四 擴充開發計畫 (Proposed Changes)

我們將新增三個主要元件，將原本只存在終端機的數據，打通至網頁前端。

### [NEW] `data_fetchers/export_to_json.py` (資料匯出層)
在每日抓取完資料後，我們需要一個腳本將這些數據結構化並存下來，供網頁讀取。
*   **預計實作**：呼叫 `get_market_summary()` 中的各個爬蟲模組，將收集到的股價、EPS、本益比、總經指標等數據，組裝成一個標準的 JSON 格式檔案。
*   **輸出位置**：`public/data.json`

### [NEW] `public/index.html`, `public/style.css`, `public/script.js` (前端視覺層)
這將是您的專屬理財儀表板。我們會使用現代且無須編譯的原生 Web 技術來打造。
*   **使用套件**：引入強大且免費的 [Chart.js](https://www.chartjs.org/) 來繪製圖表。
*   **介面規劃**：
    *   **頂部摘要區**：顯示 Gemini 今日的重點文字分析 (AI 投資觀點)。
    *   **左側圖表 (ETF走勢與殖利率)**：使用長條圖比較美股 ETF (SMH, SHLD, VPU, BOTZ) 的價格變化。
    *   **右側圖表 (台股基本面掃描)**：使用雷達圖或混合圖表，檢視台積電 (2330)、892、881 的本益比 (P/E) 是否超過警戒區間。
    *   **底部圖表 (總經風向標)**：顯示美國失業率與基準利率的雙軸圖表。

### [MODIFY] `main.py` 與 `.github/workflows/daily_report.yml` (自動化串接層)
*   **修改內容 1 (`main.py`)**：在 Telegram 早報的結尾，加上專屬的 GitHub Pages 網址，讓您可以一鍵從手機點開圖表。
*   **修改內容 2 (`daily_report.yml`)**：設定 GitHub Actions 在推播完 Telegram 後，自動將新產生的 `public/data.json` 部署 (Deploy) 到您的 `hoooooola/finace` 儲存庫的 `gh-pages` 分支上，讓網頁永遠保持最新內容。

## 3. 驗證與測試計畫 (Verification Plan)

### 自動化測試
1.  **資料匯出測試**：於本地端執行 `python export_to_json.py`，驗證 `public/data.json` 是否成功生成且格式無誤。
2.  **前端本地預覽**：開啟本地伺服器 (`python -m http.server 8000 --directory public`)，開啟瀏覽器檢查各項圖表是否成功渲染 `data.json` 內的數值，並確認 Chart.js 動畫與樣式正常。

### 手動驗證流程 (GitHub Pages 部署)
1.  推播所有程式碼至 GitHub `main` 分支。
2.  前往 GitHub 專案 `Settings -> Pages`，確認來源已設定為 GitHub Actions 部署 (或對應的分支)。
3.  手動觸發 `daily_report.yml`，等待執行完畢。
4.  開啟您的專屬網址 (`https://hoooooola.github.io/finace`)，確認網頁內容已更新為方才抓取的最新市場數據。
5.  檢查 Telegram 手機端是否同步收到早報，且網址能正確連至您的儀表板。

## 4. [User Review Required] 🚨
由於我們即將開始撰寫網頁前端，這會牽涉到畫面的「美觀度與版面配置」：
1. 您偏好深色模式 (Dark Mode) 還是淺色模式 (Light Mode) 的儀表板？
2. 除了上述規劃的三大圖表區塊外，您還有特別想在網頁上看到的心法或是其他視覺化資訊嗎？

請您審閱這份圖表規劃，若方向沒有問題，我們就馬上開始為您設計網頁！
