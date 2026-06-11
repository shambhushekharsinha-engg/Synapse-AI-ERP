# 🚀 Synapse ERP: Next-Gen AI Supply Chain & Demand Forecasting Studio

Synapse ERP is a full-stack, closed-loop enterprise analytics platform that unifies relational data storage, multi-model time-series machine learning, and an interactive "What-If" business simulation sandbox. The system translates raw transactional ledger logs into real-time operational alerts, predictive revenue trendlines, and comparative business performance matrices.

---

## 🏗️ Core System Architecture

The platform is engineered using a robust 4-tier software architecture pattern, ensuring absolute decoupling of data persistence, algorithmic processing, and user presentation:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER (UI)                         │
│   Streamlit Web Interface | Control Center | Scenario Briefing Exporter│
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Input Streams & Configs
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                       INTELLIGENCE LAYER (ML)                          │
│   Scikit-Learn Regression Engines | Custom Pandas In-Memory Simulator  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Cleaned NumPy Data Matrices
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        DATA PERSISTENCE LAYER                          │
│   SQLite3 Relational Engine | Automated Julian Day Aggregation Pipes   │
└────────────────────────────────────────────────────────────────────────┘

```
## 📺 Live System Walkthrough & Interactive Demo

Watch the full 85-second end-to-end performance walkthrough demonstrating the multi-model machine learning architecture, transactional SQL ledger streams, and the in-memory "What-If" simulation sandbox interacting in real-time.

> 💡 **Developer Note:** Expand the video to full screen to view the real-time adjustments of the regression curves and performance deviation tags as data profiles shift.

🎥 **Live System Demonstration:**

[![▶️ Click here to Download the video Demonstartion Asset](https://raw.githubusercontent.com/shambhushekharsinha-engg/Synapse-AI-ERP/main/screenshots/dashboard_view.png)](https://github.com/shambhushekharsinha-engg/Synapse-AI-ERP/blob/main/Synapse_AI_ERP_Demonstatration.mp4)



🌟 Key Features Covered

1. Robust Data & Pipeline Engineering

Relational Storage Engine: Employs a persistent SQLite3 backend (erp_system.db) tracking enterprise schemas across primary key boundaries for Inventory and Transactions tables.

Continuous Timeline Processing: Uses optimized Julian Day SQL transformations (julianday()) to seamlessly map data strings over month boundaries into an incrementing, continuous timeline vector.

Defensive Pipeline Safeguards: Integrates Pandas in-memory validation routines (.dropna() and NumPy .astype('float64') array casting) to protect machine learning models from data type mismatches or missing elements.

2. Multi-Model Predictive Engine

Dynamic Algorithmic Switching: Features an on-the-fly model dropdown selector executing three distinct predictive models:

Linear Regression: Captures baseline revenue trajectory indicators.

Polynomial Regression (Degree 2): Detects curvature acceleration or cooling trends.

Exponential Moving Average (EMA): Prioritizes highly recent data volatility spikes over distant history.

Dynamic Horizon Exploration: Implemented an active slider extending target timelines out to Day 120, feeding values instantly to the active estimator to output financial predictions.

3. Business Simulation Sandbox

In-Memory "What-If" Stress Testing: Intercepts real database streams to virtually test heavy economic scenarios (Festive Booms or Supply Chain Freezes) via data modifiers without altering persistent storage tables.

Choice-Driven Comparison Matrix:

Calculates real-time variance deviations between active machine learning telemetry and custom manual user targets to output performance tags (Outperforming vs. Underperforming).

Corporate Document Exporter: Compiles active runtime model states, parameters, and tracking summaries into a binary byte-stream download panel for instant executive briefings (.TXT).

🛠️ Installation & Setup

1. Clone the Repository:

```bash
 git clone [https://github.com/shambhushekharsinha-engg/Synapse-AI-ERP.git](https://github.com/shambhushekharsinha-engg/Synapse-AI-ERP.git)
cd Synapse-AI-ERP
```
2. Configure Your Python Environment:
Ensure you have Python 3.10+ installed, then install the required dependencies:

```bash
pip install -r requirements.txt
```
3. Launch the Engine Workspace:
 
```bash
streamlit run app.py
```

Open your browser window and navigate to http://localhost:8501.

🔮 Future Upgrades: 
 Ingesting Custom Data Sources

To expand the application from a local sandbox to an automated global deployment, the core ingestion pipeline can be enhanced to capture live data arrays from multiple external ecosystems:

🌐 1. Live E-Commerce Webhook Integration
Connect the platform to live production transaction engines (such as Shopify, Stripe, or custom Amazon Seller central APIs) by implementing a lightweight API ingestion listener inside your data pipeline script:

```python

from flask import Flask, request
import sqlite3

app = Flask(__name__)

@app.route('/stripe-webhook', methods=['POST'])
def webhook_listener():
    payload = request.json
    amount = payload['data']['object']['amount'] / 100.0  # Convert cents
    date = payload['created_at']  # Parse timestamp string
    
    conn = sqlite3.connect("erp_system.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Transactions (Transaction_Date, Raw_String, Amount) VALUES (?, 'STRIPE_LIVE', ?)", 
        (date, amount)
    )
    conn.commit()
    conn.close()
    return '', 200

```

📊 2. Dynamic Financial Market Feeds (Upstox API)

Integrate external macroeconomic indicators or stock portfolio movements directly into the machine learning loop by pulling data frames via specialized broker REST APIs:

```python

import requests

def fetch_market_benchmark():
    url = "[https://api.upstox.com/v2/market-quote/quotes](https://api.upstox.com/v2/market-quote/quotes)"
    headers = {'Accept': 'application/json', 'Authorization': 'Bearer YOUR_ACCESS_TOKEN'}
    params = {'instrument_key': 'NSE_EQ|INE030A01027'}
    
    response = requests.get(url, headers=headers, params=params).json()
    live_price = response['data']['NSE_EQ|INE030A01027']['last_price']
    return live_price

```

📁 3. Enterprise CSV Batch-Upload Processing

Incorporate a fast file-uploader element directly into the interface sidebar to process batch records instantly via Pandas:

```python

uploaded_file = st.sidebar.file_drop_box("Upload Batch Ledger (CSV)", type=["csv"])
if uploaded_file is not None:
    df_batch = pd.read_csv(uploaded_file)
    conn = sqlite3.connect("erp_system.db")
    df_batch.to_sql("Transactions", conn, if_exists="append", index=False)
    conn.close()
    st.sidebar.success("Batch array ingested perfectly!")
 
```

👨‍💻 Developer Profile

Shambhu Shekhar Sinha
 Computer Science & Engineering Student |

Specialization in Artificial Intelligence & Machine Learning (AI & ML)

GitHub: @shambhushekharsinha-engg

Core Technical Stack: Python, C, C++, Java, SQL (SQLite3), Pandas, NumPy, Scikit-Learn, Streamlit, Matplotlib.

Domain Focus: Full-Stack Data Engineering, Predictive Modeling, Machine Learning Pipeline Design, and Enterprise System Automation.

Feel free to open an issue or submit a pull request if you want to collaborate on expanding this forecasting suite!

---

## 📄 License

Distributed under the MIT License. See the [LICENSE](LICENSE) file at the root of this repository for more details.



