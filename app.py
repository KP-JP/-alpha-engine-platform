import streamlit as st
from core_engine import QuantumEngine
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

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
st.markdown('<p style="text-align: center; color: #888;">Temporal Forensic Alpha Terminal</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    ticker_input = st.text_input(
        "ENTER TICKERS (comma separated)",
        placeholder="e.g. NVDA, AAPL, MSFT, COST"
    ).upper()
    year_window = st.number_input(
        "ANALYSIS WINDOW (YEARS)",
        min_value=1,
        max_value=30,
        value=5
    )
    analyze_btn = st.button("RUN TEMPORAL SCAN", use_container_width=True)

if analyze_btn and ticker_input:
    ticker_list = [t.strip() for t in ticker_input.split(",") if t.strip()]
    if not ticker_list:
        st.warning("Please enter at least one ticker symbol.")
    else:
        with st.spinner(f"⚡ Scanning {len(ticker_list)} assets..."):
            all_results = {}  # Store temporal data for charts

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
                    st.error(f"Could not analyze {ticker}: {e}")

            if all_results:
                # 1. LEADERBOARD SECTION
                leaderboard_data = []
                for t, r in all_results.items():
                    flat = {k: v for k, v in r.items() if k != "Temporal_Data"}
                    leaderboard_data.append(flat)

                df = pd.DataFrame(leaderboard_data)
                df = df.sort_values(by="Quantum Score", ascending=False).reset_index(drop=True)

                display_df = df.rename(columns={
                    "Average_IOER": "Avg IOER",
                    "Average_OER": "Avg OER",
                    "Average_SGA_OE": "Avg SGA/OE",
                    "Average_SGA_Cap": "Avg SGA/Cap",
                    "Average_P_OE": "Avg P/OE"
                })
                display_df.index = display_df.index + 1
                display_df.index.name = "Rank"

                top_ticker = df.iloc[0]["Ticker"]
                top_score = df.iloc[0]["Quantum Score"]

                st.markdown(
                    f"""
                    <div class="metric-card" style="border: 1px solid #ffd700; margin-bottom: 20px;">
                        <div class="metric-label">{year_window}-Year Epoch Leader</div>
                        <div class="metric-value">{top_ticker}</div>
                        <div style="color: #ffd700; font-weight: bold;">Temporal Quantum Score: {top_score}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown("### 🏆 ALPHA LEADERBOARD")
                st.table(display_df)

                # 2. DEEP DIVE VISUALIZATION SECTION
                st.markdown("---")
                st.markdown(
                    "<h2 style='text-align: center; color: #00ffcc;'>🔍 FORENSIC DEEP DIVE</h2>",
                    unsafe_allow_html=True
                )

                selected_ticker = st.selectbox(
                    "SELECT TICKER FOR TEMPORAL TRENDS",
                    options=list(all_results.keys())
                )

                if selected_ticker:
                    data = all_results[selected_ticker]["Temporal_Data"]
                    df_temp = pd.DataFrame(data)
                    # Reverse order so it goes from oldest year to newest
                    df_temp = df_temp.iloc[::-1]

                    # 3 columns for charts
                    c1, c2, c3 = st.columns(3)

                    # Chart 1: IOER Trend
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

                    # Chart 2: SGA/OE Trend
                    fig2 = px.line(
                        df_temp,
                        x="Year",
                        y="SGA/OE",
                        title="Corporate Leanliness (SGA/OE)",
                        markers=True
                    )
                    fig2.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font_color="#e0e0e0",
                        xaxis=dict(gridcolor='#333'),
                        yaxis=dict(gridcolor='#333')
                    )
                    fig2.update_traces(line_color='#ffae00', line_width=3)
                    c2.plotly_chart(fig2, use_container_width=True)

                    # Chart 3: Quantum Score Trend
                    scores = []
                    for d in data:
                        s = (
                            min(d['IOER'] * 100, 33.3)
                            + min(d['OER'] * 10, 33.3)
                            + (100 - min(d['P/OE'], 33.3))
                        )
                        scores.append(s)

                    df_temp['Quantum Score'] = scores[::-1]  # Reverse to match chronologically

                    fig3 = px.line(
                        df_temp,
                        x="Year",
                        y="Quantum Score",
                        title="Alpha Trajectory",
                        markers=True
                    )
                    fig3.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font_color="#e0e0e0",
                        xaxis=dict(gridcolor='#333'),
                        yaxis=dict(gridcolor='#333')
                    )
                    fig3.update_traces(line_color='#ff00ff', line_width=3)
                    c3.plotly_chart(fig3, use_container_width=True)

                    st.markdown(
                        f"<p style='text-align: center; color: #888;'>Analysis based on {len(data)} years of forensic data for {selected_ticker}.</p>",
                        unsafe_allow_html=True
                    )

elif not ticker_input and analyze_btn:
    st.warning("Please enter ticker symbols.")
