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

    // 2. 渲染左側：美股 ETF 圖表 (折線趨勢圖)
    const etfData = data.market_data.etfs.filter(e => !e.error && e.history && e.history.length > 0);
    const etfLabels = etfData.length > 0 ? etfData[0].history.map(h => h.date) : [];
    const etfColors = ['rgba(54, 162, 235, 1)', 'rgba(255, 99, 132, 1)', 'rgba(75, 192, 192, 1)', 'rgba(255, 205, 86, 1)'];

    const etfDatasets = etfData.map((e, index) => ({
        label: e.symbol,
        data: e.history.map(h => h.price),
        borderColor: etfColors[index % etfColors.length],
        backgroundColor: etfColors[index % etfColors.length].replace('1)', '0.1)'),
        borderWidth: 2,
        tension: 0.1,
        fill: false
    }));

    const ctxEtf = document.getElementById('etfChart').getContext('2d');
    new Chart(ctxEtf, {
        type: 'line',
        data: {
            labels: etfLabels,
            datasets: etfDatasets
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

    // 3. 渲染右側：台股股價趨勢 (折線圖)
    const twStockData = data.market_data.tw_stocks.filter(s => !s.error && s.history && s.history.length > 0);
    const twLabels = twStockData.length > 0 ? twStockData[0].history.map(h => h.date) : [];
    const twColors = ['rgba(255, 159, 64, 1)', 'rgba(153, 102, 255, 1)', 'rgba(201, 203, 207, 1)'];

    const twDatasets = twStockData.map((s, index) => ({
        label: `${s.symbol} ${s.name || ''}`.trim(),
        data: s.history.map(h => h.price),
        borderColor: twColors[index % twColors.length],
        backgroundColor: twColors[index % twColors.length].replace('1)', '0.1)'),
        borderWidth: 2,
        tension: 0.1,
        fill: false
    }));

    const ctxTw = document.getElementById('twStockChart').getContext('2d');
    new Chart(ctxTw, {
        type: 'line',
        data: {
            labels: twLabels,
            datasets: twDatasets
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

    // 4. 渲染底部：總體經濟趨勢 (折線圖)
    const macroData = data.market_data.macro_economy.filter(m => !m.error && m.history && m.history.length > 0);
    // 假設雙方日期數量一樣多，取第一組當 X 軸
    const macroLabels = macroData.length > 0 ? macroData[0].history.map(h => h.date) : [];

    const macroDatasets = macroData.map(m => {
        const isUnrate = m.series_id === 'UNRATE';
        const color = isUnrate ? 'rgba(255, 99, 132, 1)' : 'rgba(54, 162, 235, 1)';
        return {
            label: `${m.name} (%)`,
            data: m.history.map(h => h.value),
            borderColor: color,
            backgroundColor: color.replace('1)', '0.1)'),
            borderWidth: 2,
            tension: 0.1,
            fill: true
        };
    });

    const ctxMacro = document.getElementById('macroChart').getContext('2d');
    new Chart(ctxMacro, {
        type: 'line',
        data: {
            labels: macroLabels,
            datasets: macroDatasets
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
}
