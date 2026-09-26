import streamlit as st
from core_engine import QuantumEngine
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Quantum Cashflow Terminal",
    page_icon="💎",
    layout="wide"
)

# --- INSTITUTIONAL CSS ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    html, body, [class*="st-"] {
        font-family: 'JetBrains Mono', monospace;
        background-color: #0a0a0a;
        color: #e0e0e0;
    }
    .stApp {
        background: radial-gradient(circle at top right, #1a1a2e, #0a0a0a);
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #00ffcc;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #888;
        text-transform: uppercase;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- UI LAYOUT ---
st.markdown('<h1 style="text-align: center; color: #00ffcc;">💎 QUANTUM CASHFLOW</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #888;">Forensic Signal Alerter & Backtester</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    ticker_input = st.text_input(
        "ENTER TICKERS (comma separated)",
        placeholder="e.g. NVDA, AAPL, MSFT"
    ).upper()
    year_window = st.number_input(
        "ANALYSIS WINDOW (YEARS)",
        min_value=2,
        max_value=30,
        value=5
    )
    analyze_btn = st.button("RUN SIGNAL SCAN", use_container_width=True)

if analyze_btn and ticker_input:
    ticker_list = [t.strip() for t in ticker_input.split(",") if t.strip()]
    if not ticker_list:
        st.warning("Please enter ticker symbols.")
    else:
        with st.spinner(f"⚡ Calculating Divergence for {len(ticker_list)} assets..."):
            all_results = {}
            for ticker in ticker_list:
                try:
                    engine = QuantumEngine(ticker)
                    res = engine.compute_temporal_metrics(
                        start_year_idx=0,
                        end_year_idx=year_window
                    )
                    if res:
                        all_results[ticker] = res
                except Exception as e:
                    st.error(f"Error {ticker}: {e}")

            if all_results:
                leaderboard_data = []
                for t, r in all_results.items():
                    flat = {k: v for k, v in r.items() if k != "Temporal_Data"}
                    leaderboard_data.append(flat)

                df = pd.DataFrame(leaderboard_data)
                df = df.sort_values(by="Current_Score", ascending=False).reset_index(drop=True)

                # Column mapping for display
                display_df = df.rename(columns={
                    "Signal": "SIGNAL",
                    "Current_Score": "Now Score",
                    "Avg_Score": "Hist Avg",
                    "Average_IOER": "Avg IOER",
                    "Average_OER": "Avg OER",
                    "Average_SGA_OE": "Avg SGA/OE",
                    "Average_SGA_Cap": "Avg SGA/Cap",
                    "Average_P_OE": "Avg P/OE"
                })

                # Reorder columns to put SIGNAL upfront
                cols = [
                    "Ticker",
                    "SIGNAL",
                    "Divergence",
                    "Now Score",
                    "Hist Avg",
                    "Avg IOER",
                    "Avg OER",
                    "Avg SGA/OE",
                    "Avg SGA/Cap",
                    "Avg P/OE"
                ]
                display_df = display_df[[c for c in cols if c in display_df.columns]]

                display_df.index = display_df.index + 1
                display_df.index.name = "Rank"

                top_ticker = df.iloc[0]["Ticker"]
                top_signal = df.iloc[0]["Signal"]

                st.markdown(
                    f"""
                    <div class="metric-card" style="border: 1px solid #00ffcc; margin-bottom: 20px;">
                        <div class="metric-label">Current Alpha Signal</div>
                        <div class="metric-value">{top_ticker} : {top_signal}</div>
                        <div style="color: #888;">Current Score: {df.iloc[0]['Current_Score']} | Hist Avg: {df.iloc[0]['Avg_Score']} | Divergence: {df.iloc[0]['Divergence']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown("### 🏆 QUANTUM SIGNAL LEADERBOARD")
                st.table(display_df)
            else:
                st.error("No valid temporal data could be retrieved.")

elif not ticker_input and analyze_btn:
    st.warning("Please enter ticker symbols.")
