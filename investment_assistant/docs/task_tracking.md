# 理財助理開發任務清單

## 階段一：單向推播 MVP (最小可行性產品)
- [x] 專案基礎建設
  - [x] 建立 requirements.txt 與基礎套件
  - [x] 建立 main.py 測試 yfinance 股價抓取
  - [x] 建立 .env 環境變數檔 (準備放入 API Keys)
- [x] 串接 Telegram Bot
  - [x] 讀取 TELEGRAM_BOT_TOKEN
  - [x] 實作發送訊息至指定 Chat ID 的功能
- [x] 串接 Google Gemini API
  - [x] 讀取 GEMINI_API_KEY
  - [x] 設計初步 Prompt (根據 ETF 價格給予短評)
  - [x] 實作呼叫 Gemini API 取得分析結果
- [x] 整合與自動化排程
  - [x] 結合 yfinance 抓股價 -> Gemini 分析 -> Telegram 推播
  - [x] 撰寫 GitHub Actions 排程腳本 (`daily_report.yml`) 並設定 Secrets

## 階段二：深度數據整合
- [x] 爬取 Goodinfo 台股與基本面指標 (EPS/本益比等) (改由 yfinance 實作)
- [x] 抓取總體經濟數據 (失業率、Fed 利率)
- [x] 根據筆記中的投資心法優化 Gemini 分析 Prompt

## 階段三：雙向互動助理
- [x] 將機器人改為可接收指令 (例如查詢特定股票或指標)
- [ ] 部署至雲端主機或 Serverless 平台 (目前於本地端測試)

## 階段四：Visual Dashboard (圖表化網頁 UI)
- [x] 建立前台網頁架構 (HTML/CSS/JS)
- [x] 撰寫資料匯出腳本：將 Python 爬到的報價與指標轉為 JSON 格式
- [x] 視覺化圖表開發
  - [x] 繪製 ETF 走勢圖、台股 EPS/本益比長條圖
  - [x] 繪製美國失業率與基準利率變化圖
- [x] 整合 GitHub Pages：設定 Actions 每日更新 JSON 並重新部署網頁
- [x] 與 Telegram Bot 串接：讓機器人在早報中附上專屬儀表板連結
