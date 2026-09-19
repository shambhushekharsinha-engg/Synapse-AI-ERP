# 🚀 Synapse AI ERP: Next-Gen Supply Chain & Demand Forecasting Studio

Welcome to **Synapse AI ERP**! Whether you are a beginner exploring how supply chains work or an advanced data engineer looking for a production-grade forecasting architecture, this project represents a massive leap forward from traditional CRUD (Create, Read, Update, Delete) Enterprise Resource Planning systems.

Synapse is a full-stack, closed-loop enterprise analytics platform. It unifies relational data storage, advanced machine learning (XGBoost), deterministic inventory mathematics, and an interactive "What-If" business simulation sandbox. 

Moving beyond traditional static data tables, Synapse translates raw transactional ledger logs into real-time operational alerts, predictive revenue trendlines, and dynamic supplier risk matrices, ultimately allowing stakeholders to explore multiple realities through simulations without modifying production data.

---

## 🌟 What We Have Developed (Beginner to Advanced)

### 1. The Foundation: Relational Data & Math (Beginner Friendly)
At its core, an ERP tracks physical goods and money. We built a robust SQL-based backbone using **FastAPI** and **SQLAlchemy**. 
- **Inventory Mathematics:** The system autonomously calculates standard supply-chain metrics like **Reorder Point (ROP)**, **Economic Order Quantity (EOQ)**, and **Safety Stock** based on lead times and holding costs.
- **ABC Analysis:** Products are clustered into A (Top 80% revenue), B (Next 15%), and C (Bottom 5%) categories to prioritize attention.

### 2. The Brain: Machine Learning & Forecasting (Intermediate)
Instead of guessing future demand, Synapse uses **XGBoost Regression Models** to predict what customers will buy over the next 30 to 120 days.
- **Data Leakage Prevention:** We built strict chronological hold-out mechanisms and isolated product-warehouse time series. The model only learns from `lag_1` historical data, ensuring it never cheats by looking into the future.
- **Model Registry:** The ML models are loaded into memory asynchronously via a Singleton pattern, ensuring the FastAPI backend responds to requests instantly.

### 3. The Sandbox: What-If Simulation Engine (Advanced)
This is the flagship feature. What happens if a supplier is delayed by 5 days? What if demand spikes by 20%?
- **Pure, Non-Destructive Projections:** The Simulation Engine intercepts real database state and projects inventory depletion day-by-day in memory. It compares a untouched **Baseline** against your **Scenario**, outputting the exact *Delta* (e.g., "Additional Shortage: 344 Units"). 
- **Rule-Based Recommendations:** Based on the delta, the system flags exact actions (e.g., "Expedite Inbound Shipment").

### 4. The Face: Interactive Next.js Frontend (Production Grade)
We abandoned static Python dashboards for a premium **Next.js 14 App Router** frontend built with **React, Tailwind CSS, and Framer Motion**.
- **Dashboard:** A "What needs my attention right now?" control center highlighting Dead Stock, Delay Risks, and Forecast Accuracy.
- **Simulation UI:** A side-by-side impact visualizer that bridges the complex backend mathematics into an intuitive user experience.

---

## 🔮 The Unique Innovation: Autonomous Network Agent (Phase 5)

We are building something rarely seen in open-source ERPs: an **Autonomous Supply Chain Agent Loop**.

Instead of waiting for a human to run a "What-If" simulation, the **Synapse Autonomous Layer** runs overnight. It continuously scans thousands of SKUs. When it detects an impending stockout (e.g., due to a supplier delay), it autonomously simulates hundreds of routing and procurement counter-factuals. 

It wakes up the human operator in the morning with a pre-calculated, mathematically proven execution plan (e.g., "Cancel PO-9002, Re-route 400 units from Supplier C via Expedited Air to W-West to eliminate stockout risk").

*(Check the repository's interactive generative UI artifacts to see the prototype of this Dark Mode Autonomous Network dashboard!)*

---

## 🏗️ Core System Architecture (Technical Specs)

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER (UI)                         │
│   Next.js 14 | React | Tailwind CSS | Framer Motion | React-Three      │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Axios REST API Sync
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                       INTELLIGENCE API (FastAPI)                       │
│   Inventory Math | Supplier Risk | What-If Simulator | ML Registry     │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Memory Loaded Artifacts
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        MACHINE LEARNING (XGBoost)                      │
│   Lagged Feature Matrices | Chronological Splits | Python Scikit       │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ SQLAlchemy ORM
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        DATA PERSISTENCE LAYER                          │
│   PostgreSQL / SQLite3 Relational Engine | Alembic Migrations          │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Installation & Setup

**1. Clone the Repository**
```bash
git clone https://github.com/shambhushekharsinha-engg/Synapse-AI-ERP.git
cd Synapse-AI-ERP
```

**2. Configure Backend (Python 3.10+)**
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Or .venv\Scripts\Activate.ps1 on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Navigate to `http://localhost:8000/docs` to view the interactive Swagger API contract.

**3. Configure Frontend (Node.js)**
Open a new terminal.
```bash
cd frontend
npm install
npm run dev
```
Navigate to `http://localhost:3000` to access the Control Center.

---

## 👨‍💻 Developer Profile

**Shambhu Shekhar Sinha**  
*Computer Science & Engineering Student | Specialization in Artificial Intelligence & Machine Learning (AI & ML)*

- **GitHub:** [@shambhushekharsinha-engg](https://github.com/shambhushekharsinha-engg)
- **Core Technical Stack:** Python, FastAPI, Next.js, SQL, SQLAlchemy, Pandas, XGBoost, Scikit-Learn.
- **Domain Focus:** Full-Stack Data Engineering, Predictive Modeling, Machine Learning Pipeline Design, and Enterprise System Automation.

---

## 📄 License

Distributed under the MIT License. See the [LICENSE](LICENSE) file at the root of this repository for more details.
