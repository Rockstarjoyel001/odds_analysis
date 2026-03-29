Submission: Real-Time Odds Analysis Assessment

Overview

I have developed a complete end-to-end data pipeline to process, analyze, and visualize real-time Betfair Exchange streaming data. The solution includes raw data parsing, financial feature 

engineering, automated signal detection, and a dual-interface output (Web API + Power BI Dashboard).

Completed Tasks

Task 1 — Data Parsing (Scraping & Cleaning):

Extracted MATCH_ODDS market updates from raw JSONL data.

Mapped numerical runner IDs to team names (Northern Brave and Wellington Firebirds) by parsing marketDefinition blocks.

Task 2 — Feature Engineering:

Price Change (Delta): Real-time tick-by-tick movement calculation.

Rolling Average: Calculated over a 5-tick window.

Volatility: Calculated as the standard deviation of the rolling 5-tick window.

Task 3 — Signal Detection:

Implemented an automated detection engine to flag SPIKES (price moves >10% within the 5-tick time window).

Task 4 — Prediction Logic:

Developed a Mean-Reversion rule-based model. The system predicts an UP direction if the current price is below the rolling average and DOWN if it exceeds it, identifying potential 

overreactions in the market.

Task 5 — Output Interface (Dual Delivery):

FastAPI & Web Dashboard: A live web terminal (Python FastAPI) that serves real-time JSON data and a custom HTML/Bootstrap frontend.

Power BI Analytics: A comprehensive BI report for deep-dive trend and volatility analysis.

How to Run the Project

Environment Setup: Ensure Python is installed. Install dependencies via terminal:

pip install fastapi uvicorn pandas

Step 1: Run the Data Engine (Scraper):

Open a command prompt and run:

python main.py

(This processes data.txt and generates the structured odds_analysis_results.csv file).

Step 2: Run the Web Dashboard (API):

Open a second command prompt and run:

python api.py

Step 3: View the Results:
Web Terminal: Open your browser to http://127.0.0.1:8000 to see the live trading feed.

Power BI: Open the attached .pbix file (or view the provided screenshot) to see the full match trend and volatility report.

Attached Deliverables

main.py: The core data processing and logic engine.

api.py: The FastAPI backend and frontend dashboard code.

odds_analysis_results.csv: The cleaned and structured output data with all engineered features.

Power_BI_Dashboard_Screenshot.png: A visual report showing the match trends and signals.

README.txt: Detailed technical approach and logic explanation.
