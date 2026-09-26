import streamlit as st
from core_engine import QuantumEngine
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Quantum Cashflow Terminal",
    page_icon="💎",
    layout="wide"
)

# --- GLASSMORPHISM CUSTOM CSS ---
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
        transition: transform 0.3s ease;
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
st.markdown('<p style="text-align: center; color: #888;">Institutional Forensic Alpha Leaderboard</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    ticker_input = st.text_input(
        "ENTER TICKERS (comma separated)",
        placeholder="e.g. NVDA, AAPL, MSFT, COST"
    ).upper()
    analyze_btn = st.button("RUN ALPHA SCAN", use_container_width=True)

if analyze_btn and ticker_input:
    ticker_list = [t.strip() for t in ticker_input.split(",") if t.strip()]
    if not ticker_list:
        st.warning("Please enter at least one ticker symbol.")
    else:
        with st.spinner(f"⚡ Scanning {len(ticker_list)} assets for Alpha signals..."):
            all_results = []
            for ticker in ticker_list:
                try:
                    engine = QuantumEngine(ticker)
                    res = engine.compute_quantum_metrics()
                    all_results.append(res)
                except Exception as e:
                    st.error(f"Could not analyze {ticker}: {e}")

            if all_results:
                df = pd.DataFrame(all_results)
                df = df.sort_values(by="Quantum Score", ascending=False).reset_index(drop=True)
                df.index = df.index + 1
                df.index.name = "Rank"

                # Display Top Leader
                top_ticker = df.iloc[0]["Ticker"]
                top_score = df.iloc[0]["Quantum Score"]
                st.markdown(
                    f"""
                    <div class="metric-card" style="border: 1px solid #ffd700; margin-bottom: 20px;">
                        <div class="metric-label">Current Market Leader</div>
                        <div class="metric-value">{top_ticker}</div>
                        <div style="color: #ffd700; font-weight: bold;">Quantum Score: {top_score}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # Display full table with the new insurance metrics
                st.markdown("### 🏆 ALPHA LEADERBOARD")
                st.table(df)
                st.success(f"Scan complete. {len(all_results)} assets ranked.")
            else:
                st.error("No valid data could be retrieved.")
elif not ticker_input and analyze_btn:
    st.warning("Please enter ticker symbols.")
