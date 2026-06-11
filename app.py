import streamlit as st # type: ignore
import sqlite3
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt

# ==========================================
# 1. UI/UX PAGE ARCHITECTURE
# ==========================================
st.set_page_config(page_title="Synapse AI ERP Portal", layout="wide")

# Enhanced corporate container framing style
st.markdown("""
    <style>
    div[data-testid="stMetricContainer"] {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Synapse ERP: Next-Gen AI Supply Chain Studio")
st.markdown("---")

# ==========================================
# 2. CONTROL CENTER SIDEBAR
# ==========================================
st.sidebar.header("📊 Control Center")
st.sidebar.info("Connected to local: `erp_system.db`")
st.sidebar.markdown("---")

# Target Settings Input
st.sidebar.subheader("🎯 Dashboard Target Settings")
target_daily_velocity = st.sidebar.number_input(
    "Target Growth Velocity ($/day)", min_value=0.0, value=500.0, step=50.0
)

st.sidebar.markdown("---")

# Forecasting Engine Selector
st.sidebar.subheader("🧠 Machine Learning Core")
selected_model_type = st.sidebar.selectbox(
    "Select Forecasting Engine:",
    ["Linear Regression", "Polynomial Regression (Deg 2)", "Exponential Moving Average (EMA)"]
)

st.sidebar.markdown("---")

# 'What-If' Simulation Sandbox Panel
st.sidebar.subheader("⚡ 'What-If' Simulation Sandbox")
enable_simulation = st.sidebar.checkbox("Activate Live Simulation Mode", value=False)

sim_multiplier = 1.0
sim_type = "None"

if enable_simulation:
    sim_type = st.sidebar.selectbox(
        "Select Simulation Event Type:",
        ["Festive Season Sale Spike (Boom)", "Supply Chain Disturbance (Freeze)"]
    )
    sim_multiplier = st.sidebar.slider(
        "Simulation Severity Scale Multiplier:", 
        min_value=0.1, max_value=3.0, value=2.0 if "Spike" in sim_type else 0.3, step=0.1
    )
    st.sidebar.warning("⚠️ Simulation Active: Data reflects modified trends.")

st.sidebar.markdown("---")

# Collapsible Data Ingestion Block
with st.sidebar.expander("📥 Ingest New Transaction Data", expanded=False):
    with st.form(key="transaction_form", clear_on_submit=True):
        new_day = st.number_input("Day Number", min_value=1, max_value=100, step=1)
        new_amount = st.number_input("Amount ($)", min_value=0.0, step=50.0)
        category = st.selectbox("Category", ["SALES // RETAIL", "STRIPE REVENUE", "REFUND"])
        submit_button = st.form_submit_button(label="Commit to Ledger")

if submit_button:
    if new_amount > 0:
        conn = sqlite3.connect("erp_system.db")
        cursor = conn.cursor()
        if int(new_day) <= 30:
            mock_date = f"2026-06-{int(new_day):02d}"
        else:
            extra_days = int(new_day) - 30
            mock_date = f"2026-07-{extra_days:02d}"
        mock_raw_string = f"{category} id:{conn.total_changes + 1000}"
        cursor.execute("INSERT INTO Transactions (Transaction_Date, Raw_String, Amount) VALUES (?, ?, ?)", (mock_date, mock_raw_string, new_amount))
        conn.commit()
        conn.close()
        st.sidebar.success(f"✔️ Day {new_day} logged!")
        st.rerun()
    else:
        st.sidebar.error("Amount must be greater than 0.")

# ==========================================
# 3. INTERFACE NAVIGATION TABS
# ==========================================
tab1, tab2 = st.tabs(["📦 Operational Ledger", "🔮 Interactive Comparison Matrix"])

with tab1:
    st.header("Real-Time Enterprise Ledger")
    conn = sqlite3.connect("erp_system.db")
    df_inv = pd.read_sql_query("SELECT Item_Name, Current_Stock, Reorder_Threshold FROM Inventory", conn)
    conn.close()
    st.subheader("Current Stock Levels")
    st.dataframe(df_inv, use_container_width=True)

# ------------------------------------------
# TAB 2: ADVANCED PREDICTIVE & EXPORT STUDIO
# ------------------------------------------
with tab2:
    st.header(f"🔮 Core Predictive Studio — Engine: `{selected_model_type}`")
    
    # Fetch In-Scope SQL Transaction Stream
    conn = sqlite3.connect("erp_system.db")
    perfect_query = """
    SELECT 
        CAST(julianday(Transaction_Date) - julianday('2026-06-01') + 1 AS INTEGER) as Day_Number,
        SUM(Amount) as Total_Sales
    FROM Transactions
    WHERE Amount > 0 AND Transaction_Date >= '2026-06-01'
    GROUP BY Day_Number ORDER BY Day_Number ASC;
    """
    df_perfect_sales = pd.read_sql_query(perfect_query, conn).dropna()
    conn.close()
    
    # Intercept data frame for in-memory simulation variations
    if enable_simulation:
        last_day = int(df_perfect_sales['Day_Number'].max())
        simulated_days = list(range(last_day + 1, last_day + 11))
        last_sales_baseline = df_perfect_sales['Total_Sales'].iloc[-1]
        
        simulated_sales = []
        for d in simulated_days:
            if "Spike" in sim_type:
                sim_value = last_sales_baseline * sim_multiplier * (1 + (d - last_day)*0.05)
            else:
                sim_value = last_sales_baseline * sim_multiplier
            simulated_sales.append(sim_value)
            
        df_sim_rows = pd.DataFrame({'Day_Number': simulated_days, 'Total_Sales': simulated_sales})
        df_display_sales = pd.concat([df_perfect_sales, df_sim_rows], ignore_index=True)
    else:
        df_display_sales = df_perfect_sales.copy()

    X_perf = df_display_sales['Day_Number'].values.astype('float64').reshape(-1, 1)
    y_perf = df_display_sales['Total_Sales'].values.astype('float64')
    
    # Train tracking models
    base_linear_model = LinearRegression().fit(X_perf, y_perf)
    linear_velocity = base_linear_model.coef_[0]

    if selected_model_type == "Linear Regression":
        final_model = LinearRegression().fit(X_perf, y_perf)
        velocity = final_model.coef_[0]
        y_plot_preds = final_model.predict(X_perf)
        
    elif selected_model_type == "Polynomial Regression (Deg 2)":
        poly_features = PolynomialFeatures(degree=2, include_bias=False)
        X_poly = poly_features.fit_transform(X_perf)
        poly_model = LinearRegression().fit(X_poly, y_perf)
        y_plot_preds = poly_model.predict(X_poly)
        velocity = (y_plot_preds[-1] - y_plot_preds[0]) / (X_perf[-1][0] - X_perf[0][0])
        
    elif selected_model_type == "Exponential Moving Average (EMA)":
        df_display_sales['EMA'] = df_display_sales['Total_Sales'].ewm(span=3, adjust=False).mean()
        y_plot_preds = df_display_sales['EMA'].values
        velocity = (y_plot_preds[-1] - y_plot_preds[-2]) if len(y_plot_preds) > 1 else linear_velocity

    # Metrics Matrix Execution
    st.subheader("📊 Performance Deviation Matrix")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric(label="Selected Engine Net Velocity", value=f"${velocity:.2f} / day")
    with c2:
        st.metric(label="Your Target Benchmark", value=f"${target_daily_velocity:.2f} / day")
    with c3:
        deviation = velocity - target_daily_velocity
        st.metric(
            label="Velocity Variance Margin", 
            value=f"${deviation:.2f} / day",
            delta=f"{'Outperforming' if deviation >= 0 else 'Underperforming'}"
        )
        
    st.markdown("---")
    st.subheader("🔮 Dynamic Horizon Forecasting")
    selected_horizon_day = st.slider("Select future projection milestone day:", min_value=40, max_value=120, value=55, step=1)
    
    if selected_model_type == "Linear Regression":
        dynamic_prediction = final_model.predict([[selected_horizon_day]])[0]
    elif selected_model_type == "Polynomial Regression (Deg 2)":
        features_future = poly_features.transform([[selected_horizon_day]])
        dynamic_prediction = poly_model.predict(features_future)[0]
    elif selected_model_type == "Exponential Moving Average (EMA)":
        days_forward = selected_horizon_day - X_perf[-1][0]
        dynamic_prediction = y_plot_preds[-1] + (velocity * days_forward)
        
    target_simulated_revenue = df_perfect_sales['Total_Sales'].iloc[0] + (target_daily_velocity * (selected_horizon_day - 1))
    
    col_pred1, col_pred2 = st.columns(2)
    with col_pred1:
        st.info(f"🎯 **`{selected_model_type}` Prediction:** **${dynamic_prediction:,.2f}**")
    with col_pred2:
        st.warning(f"🏁 **Your Target Path Projection:** **${target_simulated_revenue:,.2f}**")
    
    st.markdown("---")
    st.subheader("📈 Multi-Trend Visualization Engine")
    
    fig, ax = plt.subplots(figsize=(10, 4.5))
    if enable_simulation:
        split_idx = len(df_perfect_sales)
        ax.scatter(df_display_sales['Day_Number'].iloc[:split_idx], df_display_sales['Total_Sales'].iloc[:split_idx], color='#007bff', alpha=0.7, label='Actual Database Records')
        ax.scatter(df_display_sales['Day_Number'].iloc[split_idx:], df_display_sales['Total_Sales'].iloc[split_idx:], color='#6c757d', linestyle=':', alpha=0.6, label='Simulated Scenario Vector')
    else:
        ax.scatter(df_display_sales['Day_Number'], df_display_sales['Total_Sales'], color='#007bff', alpha=0.7, label='Cleaned SQL Data Points')
    
    ax.plot(df_display_sales['Day_Number'], y_plot_preds, color='#dc3545', linewidth=2.5, label=f'Active Engine: {selected_model_type}')
    
    user_trend_line = df_perfect_sales['Total_Sales'].iloc[0] + (target_daily_velocity * (df_display_sales['Day_Number'] - 1))
    ax.plot(df_display_sales['Day_Number'], user_trend_line, color='#ffc107', linestyle='--', linewidth=2, label='User Selected Target Path')
    
    ax.set_xlabel("Timeline Evolution (Days Passed)")
    ax.set_ylabel("Total Enterprise Sales ($)")
    ax.legend(facecolor='#ffffff', edgecolor='#e9ecef')
    ax.grid(True, linestyle=':', alpha=0.6)
    st.pyplot(fig)

    # ------------------------------------------
    # --- INNOVATION C: EXECUTIVE REPORT EXPORTER ---
    # ------------------------------------------
    st.markdown("---")
    st.subheader("📋 Corporate Reporting Suite")
    
    # Construct corporate data briefing layout in text/md bytes format
    report_content = f"""==================================================
EXECUTIVE DEMAND PERFORMANCE BRIEFING
Generated Session Metadata Timeline Frame
==================================================

[Core Architecture Parameters]
* Active Core ML Engine Model: {selected_model_type}
* Applied Target User Baseline Metric: ${target_daily_velocity:.2f}/day
* Live Computed Analytics Flow Rate: ${velocity:.2f}/day

[Performance Deviation Matrix Valuation]
* Net Target Variance Margin: ${deviation:.2f}/day
* Evaluated Operational Status: {'✅ EXCEEDING EXPECTATIONS TARGET' if deviation >= 0 else '⚠️ CRITICAL PERFORMANCE LAG WARNING'}

[Horizon Growth Scouting Projections]
* Targeted Horizon Milestone Evaluation: Day {selected_horizon_day}
* Core Algorithmic Model Prediction: ${dynamic_prediction:,.2f}
* User Defined Business Goal Metric: ${target_simulated_revenue:,.2f}

[Active Sandbox State Profile]
* Stress-Testing Mode Flag: {enable_simulation}
* Active Vector Event Triggered: {sim_type}
* Severity Parameter Multiplier Weight: {sim_multiplier}x

==================================================
End of Session Intelligence Briefing Document
==================================================
"""
    
    # Render the native download portal channel trigger link asset button
    st.download_button(
        label="📥 Download Executive Briefing Report (.TXT)",
        data=report_content,
        file_name="Synapse_ERP_Executive_Briefing.txt",
        mime="text/plain",
        help="Export all current database metrics, machine learning weights, and model evaluations instantly."
    )