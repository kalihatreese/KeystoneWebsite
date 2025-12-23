import os
import json
import pandas as pd
from flask import Flask, render_template_string

app = Flask(__name__)
GW_ROOT = os.path.expanduser("~/KeystoneCreatorSuite/ghostwalker")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Ghost Walker Dashboard</title>
    <style>
        body { background: #0f0f0f; color: #00ff41; font-family: 'Courier New', monospace; padding: 20px; }
        .stat-card { border: 1px solid #00ff41; padding: 15px; margin: 10px; border-radius: 5px; background: #1a1a1a; }
        h1 { color: #fff; text-shadow: 0 0 10px #00ff41; }
        .resonance-high { color: #00ff41; font-weight: bold; }
    </style>
</head>
<body>
    <h1>🛰️ GHOST WALKER: RESONANCE DASHBOARD</h1>
    <div class="stat-card">
        <h3>KERNEL IDENTITY: {{ kernel }}</h3>
        <p>RESONANCE SCORE: <span class="resonance-high">{{ score }}</span></p>
        <p>ADMIN: {{ admin }}</p>
    </div>
    <div class="stat-card">
        <h3>CONTINUITY LOG (Latest Checkpoint)</h3>
        <pre>{{ summary }}</pre>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    # Load Resonance Data
    report_path = os.path.join(GW_ROOT, "reports/resonance_report.json")
    with open(report_path, 'r') as f:
        data = json.load(f)
    
    # Load latest summary
    today = pd.Timestamp.now().strftime("%Y-%m-%d")
    sum_path = os.path.join(GW_ROOT, f"logs/daily_summaries/summary_{today}.txt")
    summary = "No summary generated yet."
    if os.path.exists(sum_path):
        with open(sum_path, 'r') as f:
            summary = f.read()

    return render_template_string(HTML_TEMPLATE, 
                                kernel=data['kernel'], 
                                score=data['resonance_score'], 
                                admin=data['admin_verification'],
                                summary=summary)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
