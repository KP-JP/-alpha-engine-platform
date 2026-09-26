import streamlit as st
from core_engine import QuantumEngine
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Quantum Cashflow Terminal", page_icon="💎", layout="wide")

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

st.markdown('<h1 style="text-align: center; color: #00ffcc;">💎 QUANTUM CASHFLOW</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #888;">Forensic Signal Alerter & Temporal Backtester</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    ticker_input = st.text_input("ENTER TICKERS (comma separated)", placeholder="e.g. NVDA, AAPL, MSFT").upper()
    year_window = st.number_input("ANALYSIS WINDOW (YEARS)", min_value=1, max_value=30, value=5)
    analyze_btn = st.button("RUN SIGNAL SCAN", use_container_width=True)

if analyze_btn and ticker_input:
    ticker_list = [t.strip() for t in ticker_input.split(",") if t.strip()]
    if not ticker_list:
        st.warning("Please enter ticker symbols.")
    else:
        with st.spinner(f"⚡ Calculating Divergence over {year_window} years..."):
            all_results = {}
            for ticker in ticker_list:
                try:
                    engine = QuantumEngine(ticker)
                    res = engine.compute_temporal_metrics(start_year_idx=0, end_year_idx=year_window)
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

                # Mapping for the Leaderboard
                display_df = df.rename(columns={
                    "Signal": "SIGNAL",
                    "Actual_Years": "Yrs Found",
                    "Current_Score": "Now Score",
                    "Avg_Score": "Hist Avg",
                    "Average_IOER": "Avg IOER",
                    "Average_OER": "Avg OER",
                    "Average_SGA_OE": "Avg SGA/OE",
                    "Average_SGA_Cap": "Avg SGA/Cap",
                    "Average_P_OE": "Avg P/OE"
                })

                cols = [
                    "Ticker",
                    "SIGNAL",
                    "Yrs Found",
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
                        <div style="color: #888;">Current Score: {df.iloc[0]['Current_Score']} | Hist Avg: {df.iloc[0]['Avg_Score']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown("### 🏆 QUANTUM SIGNAL LEADERBOARD")
                st.table(display_df)

                st.markdown("---")
                st.markdown("<h2 style='text-align: center; color: #00ffcc;'>🔍 FORENSIC DEEP DIVE</h2>", unsafe_allow_html=True)
                selected_ticker = st.selectbox("SELECT TICKER FOR TEMPORAL TRENDS", options=list(all_results.keys()))

                if selected_ticker:
                    data = all_results[selected_ticker]["Temporal_Data"]
                    df_temp = pd.DataFrame(data).iloc[::-1]
                    c1, c2, c3 = st.columns(3)

                    fig1 = px.line(df_temp, x="Year", y="IOER", title="IOER Velocity", markers=True)
                    fig1.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font_color="#e0e0e0",
                        xaxis=dict(gridcolor='#333'),
                        yaxis=dict(gridcolor='#333')
                    )
                    fig1.update_traces(line_color='#00ffcc', line_width=3)
                    c1.plotly_chart(fig1, use_container_width=True)

                    fig2 = px.line(df_temp, x="Year", y="SGA/OE", title="Corporate Leanliness (SGA/OE)", markers=True)
                    fig2.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font_color="#e0e0e0",
                        xaxis=dict(gridcolor='#333'),
                        yaxis=dict(gridcolor='#333')
                    )
                    fig2.update_traces(line_color='#ffae00', line_width=3)
                    c2.plotly_chart(fig2, use_container_width=True)

                    scores = []
                    for d in data:
                        s = (
                            min(d['IOER'] * 100, 33.3)
                            + min(d['OER'] * 10, 33.3)
                            + (100 - min(d['P/OE'], 33.3))
                        )
                        scores.append(s)
                    df_temp['Quantum Score'] = scores[::-1]

                    fig3 = px.line(df_temp, x="Year", y="Quantum Score", title="Alpha Trajectory", markers=True)
                    fig3.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font_color="#e0e0e0",
                        xaxis=dict(gridcolor='#333'),
                        yaxis=dict(gridcolor='#333')
                    )
                    fig3.update_traces(line_color='#ff00ff', line_width=3)
                    c3.plotly_chart(fig3, use_container_width=True)
            else:
                st.error("No valid temporal data could be retrieved.")
elif not ticker_input and analyze_btn:
    st.warning("Please enter ticker symbols.")
