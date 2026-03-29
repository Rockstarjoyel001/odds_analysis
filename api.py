from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pandas as pd
import uvicorn
import os

app = FastAPI()


CSV_FILE = "odds_analysis_results.csv"


@app.get("/api/data")
def get_data():
    if not os.path.exists(CSV_FILE):
        return {"error": "Scraper data file not found yet..."}

    try:

        df = pd.read_csv(CSV_FILE)


        df_clean = df.fillna("")


        return df_clean.tail(20).to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}


@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Odds Terminal</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { background-color: #000; color: #0f0; font-family: 'Courier New', monospace; padding: 20px; }
            .spike { background-color: #400 !important; color: #f88; font-weight: bold; border: 1px solid red; }
            .up { color: #0f0; }
            .down { color: #f00; }
            .card { background-color: #111; border: 1px solid #0f0; margin-bottom: 20px; padding: 15px; }
            table { border-color: #0f0 !important; }
            th { color: #fff; border-bottom: 2px solid #0f0 !important; }
        </style>
    </head>
    <body>
        <div class="container text-center">
            <h2 class="mb-4">REAL-TIME ODDS PREDICTION TERMINAL</h2>
            <div class="card">
                <h4>LIVE SENTIMENT: <span id="current-pred">CONNECTING...</span></h4>
            </div>
            <table class="table table-dark table-hover">
                <thead>
                    <tr>
                        <th>TEAM</th>
                        <th>PRICE</th>
                        <th>DELTA</th>
                        <th>SIGNAL</th>
                        <th>PREDICTION</th>
                    </tr>
                </thead>
                <tbody id="data-table"></tbody>
            </table>
        </div>
        <script>
    async function refreshData() {
                try {
                    const res = await fetch('/api/data');
                    const data = await res.json();
                    if (data.error) return;

                    const tableBody = document.getElementById('data-table');
                    tableBody.innerHTML = '';

                    // Create a map to store the LATEST prediction for each team
                    const latestByTeam = {};

                    // Process data (newest first for the table)
                    const displayData = [...data].reverse(); 
                    displayData.forEach(row => {
                        // Store the first time we see a team (which is the newest)
                        if (!latestByTeam[row.team]) {
                            latestByTeam[row.team] = row.prediction;
                        }

                        const isSpike = row.signal === 'SPIKE' ? 'spike' : '';
                        tableBody.innerHTML += `
                            <tr class="${isSpike}">
                                <td>${row.team}</td>
                                <td>${row.ltp}</td>
                                <td class="${row.delta >= 0 ? 'up' : 'down'}">${row.delta}</td>
                                <td>${row.signal || '-'}</td>
                                <td class="${row.prediction === 'UP' ? 'up' : 'down'}">${row.prediction}</td>
                            </tr>
                        `;
                    });

                    // Update the LIVE SENTIMENT card to show both teams
                    let sentimentHTML = "";
                    for (const [team, pred] of Object.entries(latestByTeam)) {
                        const color = pred === 'UP' ? 'up' : 'down';
                        sentimentHTML += `${team}: <span class="${color}">${pred}</span> | `;
                    }
                    document.getElementById('current-pred').innerHTML = sentimentHTML.slice(0, -3);

                } catch (e) { console.log("Refresh Error"); }
            }
            setInterval(refreshData, 1000);
            refreshData();
        </script>
    </body>
    </html>
    """


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)