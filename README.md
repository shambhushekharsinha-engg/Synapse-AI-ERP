# 🚀 Synapse AI ERP: Next-Gen Supply Chain & Demand Forecasting Studio

Synapse AI ERP is a full-stack, closed-loop enterprise analytics platform that unifies relational data storage, advanced machine learning (XGBoost), deterministic inventory mathematics, and an interactive "What-If" business simulation sandbox. 

Moving beyond traditional CRUD interfaces, Synapse translates raw transactional ledger logs into real-time operational alerts, predictive revenue trendlines, and dynamic supplier risk matrices, ultimately allowing stakeholders to explore multiple realities through simulations without modifying production data.

---

## 🏗️ Core System Architecture (Modernized Stack)

The platform has been aggressively modernized from its initial prototype into a scalable, production-grade 4-tier software architecture:

### 1. Presentation Layer (Next.js 14 Frontend - Phase 4)
- **Framework:** Next.js 14 (App Router), React, Tailwind CSS, Framer Motion.
- **Interfaces:** Dynamic interactive Dashboards, Stockout Risk matrices, 3D Warehouse/Supply Chain graphs (`react-three-fiber`), and a dedicated What-If Simulation Sandbox.
- **Philosophy:** "What needs my attention right now?" rather than overwhelming static data tables.

### 2. Intelligence API Layer (FastAPI)
- **Framework:** FastAPI providing strongly-typed, auto-documented endpoints.
- **Micro-Services:** 
  - **Inventory Math:** Deterministic EOQ, ROP, Safety Stock, ABC Analysis.
  - **Supplier Intelligence:** Delay Risk algorithms, Lead-Time Analytics, Performance Scoring.
  - **What-If Engine:** Pure, non-destructive scenario state projection (Supplier Delays, Demand Spikes, Supply Reductions).

### 3. Machine Learning Layer (XGBoost)
- **Engine:** XGBoost regression models.
- **Pipeline:** Comprehensive feature engineering guarding against data leakage (strict chronological holds, lagged features).
- **Execution:** Singleton Model Registry pattern loads artifacts into memory at server startup to prevent request-time bottlenecks.

### 4. Data Persistence Layer (PostgreSQL / SQLite via SQLAlchemy)
- **ORM:** SQLAlchemy managing robust domain models (`Product`, `Warehouse`, `Inventory`, `Supplier`, `PurchaseOrder`, `SalesOrder`).
- **Migrations:** Alembic for tracked schema evolution.

---

## 🌟 Key Features Developed

### Phase 2: Advanced Forecasting
- **XGBoost Predictor:** Outperforms legacy baselines (Naive, Moving Average) on strict chronological holds.
- **Leakage Prevention:** Features isolate product-warehouse series dynamically, ensuring contemporaneous supply chain variables strictly use `lag_1` history.

### Phase 3: Deterministic Intelligence & Simulation
- **Inventory Math Bedrock:** Explains inventory levels using standard financial models (Holding costs vs. Ordering costs).
- **Supplier Risk:** Tracks lead-time standard deviations and on-time performance dynamically.
- **What-If Simulation Sandbox:** Intercepts real database streams to project future inventory levels virtually. It measures the "Delta" (impact) of an event like a "+5 Day Supplier Delay" against the untouched baseline, generating rule-based recommendations like "Expedite Inbound Shipment".

### Phase 4: Interactive Frontend (In Progress)
- **Generative UI / Components:** Rich, component-driven layouts tailored for high-density enterprise operations.
- **3D Visualization:** Purpose-built rendering for spatial problems (Warehouse Zones, Network Logistics).

---

## 🛠️ Installation & Setup (Backend API)

**1. Clone the Repository**
```bash
git clone https://github.com/shambhushekharsinha-engg/Synapse-AI-ERP.git
cd Synapse-AI-ERP
```

**2. Configure Python Environment**
Ensure Python 3.10+ is installed.
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Or .venv\Scripts\Activate.ps1 on Windows
pip install -r requirements.txt
```

**3. Launch the FastAPI Backend**
```bash
uvicorn app.main:app --reload
```
Navigate to `http://localhost:8000/docs` to view the interactive Swagger API contract.

*(Frontend instructions will be added here upon completion of Phase 4).*

---

## 🔮 Future Upgrades
- **Phase 5 (Multi-Agent AI):** Instead of simple LLM wrappers, introducing autonomous agent loops that can interact directly with the Deterministic Simulation Engine to proactively hunt for supply chain optimizations overnight.
- **Network Expansions:** Multi-warehouse transshipment modeling.
- **Probabilistic Forecasting:** Confidence intervals alongside point predictions.

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
