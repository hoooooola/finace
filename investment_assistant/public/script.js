document.addEventListener('DOMContentLoaded', () => {
    fetch('data.json')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            renderDashboard(data);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            document.getElementById('aiAnalysisText').innerHTML = `<span class="text-danger">無法載入資料 (請確認 data.json 是否存在或本地伺服器是否運行): ${error.message}</span>`;
        });
});

function renderDashboard(data) {
    // 1. 設置基本資訊
    document.getElementById('updateTime').innerText = `更新時間: ${data.update_time}`;
    document.getElementById('aiAnalysisText').innerText = data.ai_analysis;

    // 2. 渲染左側：美股 ETF 圖表 (長條圖)
    const etfData = data.market_data.etfs.filter(e => !e.error);
    const etfLabels = etfData.map(e => e.symbol);
    const etfPrices = etfData.map(e => e.price);

    const ctxEtf = document.getElementById('etfChart').getContext('2d');
    new Chart(ctxEtf, {
        type: 'bar',
        data: {
            labels: etfLabels,
            datasets: [{
                label: '最新收盤價 (USD)',
                data: etfPrices,
                backgroundColor: 'rgba(54, 162, 235, 0.6)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'top', labels: { color: '#e5e7eb' } }
            },
            scales: {
                y: { beginAtZero: false, grid: { color: '#333' }, ticks: { color: '#aaa' } },
                x: { grid: { color: '#333' }, ticks: { color: '#aaa' } }
            }
        }
    });

    // 3. 渲染右側：台股基本面 P/E (雷達圖)
    // 我們過濾出有 PE 資料的台股來畫圖
    const twStockData = data.market_data.tw_stocks.filter(s => !s.error && s.pe !== "N/A");
    const twLabels = twStockData.map(s => `${s.symbol} ${s.name || ''}`.trim());
    const twPE = twStockData.map(s => parseFloat(s.pe) || 0);

    const ctxTw = document.getElementById('twStockChart').getContext('2d');
    new Chart(ctxTw, {
        type: 'polarArea',  // 使用極座標圖展示本益比高低
        data: {
            labels: twLabels,
            datasets: [{
                label: '本益比 (P/E)',
                data: twPE,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.6)',
                    'rgba(75, 192, 192, 0.6)',
                    'rgba(255, 205, 86, 0.6)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'right', labels: { color: '#e5e7eb' } }
            },
            scales: {
                r: {
                    grid: { color: '#444' },
                    ticks: { color: '#ccc', backdropColor: 'transparent' }
                }
            }
        }
    });

    // 4. 渲染底部：總體經濟卡片
    const macroContainer = document.getElementById('macroCards');
    macroContainer.innerHTML = ''; // 清空預設

    data.market_data.macro_economy.forEach(macro => {
        if (macro.error) return;

        // 判斷顏色：失業率若大於某數可能要標紅，這邊先用預設 highlight
        let colorClass = macro.series_id === 'UNRATE' ? 'text-danger' : 'text-info';
        let icon = macro.series_id === 'UNRATE' ? '📉' : '🏦';

        const cardHtml = `
            <div class="col-md-6 mb-3">
                <div class="p-3 border border-secondary rounded bg-dark">
                    <h5 class="text-light">${icon} ${macro.name} (${macro.series_id})</h5>
                    <h2 class="mb-0 fw-bold ${colorClass}">${macro.value}</h2>
                    <small class="text-muted">資料時間: ${macro.date}</small>
                </div>
            </div>
        `;
        macroContainer.innerHTML += cardHtml;
    });
}
