import json
import statistics
import csv
from collections import deque
import os


OUTPUT_CSV = "odds_analysis_results.csv"


class BetfairProcessor:
    def __init__(self):
        self.runner_names = {}
        self.match_odds_markets = set()
        self.history = {}
        self.csv_file = open(OUTPUT_CSV, mode='w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(
            ['timestamp', 'team', 'ltp', 'delta', 'rolling_avg', 'volatility', 'signal', 'prediction'])

    def run(self):
        print(f"--- SCRAPER RUNNING ---")
        print(f"--- SAVING TO: {os.path.abspath(OUTPUT_CSV)} ---\n")

        with open("33892257", 'r') as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                    if 'mc' not in data: continue
                    timestamp = data.get('pt')
                    for mc in data['mc']:
                        m_id = mc.get('id')
                        if 'marketDefinition' in mc:
                            mdef = mc['marketDefinition']
                            if mdef.get('marketType') == 'MATCH_ODDS':
                                self.match_odds_markets.add(m_id)
                                for r in mdef.get('runners', []):
                                    self.runner_names[r['id']] = r['name']

                        if m_id not in self.match_odds_markets or 'rc' not in mc: continue

                        for rc in mc['rc']:
                            rid = rc.get('id');
                            ltp = rc.get('ltp')
                            if ltp and rid in self.runner_names:
                                team = self.runner_names[rid]
                                if rid not in self.history: self.history[rid] = deque(maxlen=5)
                                prev_ltp = self.history[rid][-1] if self.history[rid] else ltp
                                self.history[rid].append(ltp)
                                hist_list = list(self.history[rid])
                                delta = round(ltp - prev_ltp, 3)
                                avg = round(statistics.mean(hist_list), 3)
                                vol = round(statistics.stdev(hist_list), 3) if len(hist_list) > 1 else 0.0
                                signal = "SPIKE" if abs(ltp - hist_list[0]) / hist_list[0] > 0.10 else ""
                                prediction = "UP" if ltp < avg else "DOWN"

                                self.csv_writer.writerow([timestamp, team, ltp, delta, avg, vol, signal, prediction])
                except:
                    continue
        self.csv_file.close()
        print("Done!")


if __name__ == "__main__":
    BetfairProcessor().run()