import streamlit as st`nfrom core_engine import
  QuantumEngine`nimport pandas as pd`nst.set_page_config(page_title="Quantum Cashflow
  Terminal", page_icon="💎", layout="wide")`nst.markdown("""<style>@import url("https://f
  onts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap");html, body,
  [class*="st-"] {font-family: "JetBrains Mono", monospace; background-color: #0a0a0a;
  color: #e0e0e0;} .stApp {background: radial-gradient(circle at top right, #1a1a2e,
  #0a0a0a);} .metric-card {background: rgba(255, 255, 255, 0.05); backdrop-filter:
  blur(10px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 15px; padding:
  20px; text-align: center;} .metric-value {font-size: 2rem; font-weight: bold; color:
  #00ffcc;} .metric-label {font-size: 0.9rem; color: #888; text-transform: uppercase;}
  .verdict-text {font-size: 3rem; font-weight: 800; text-align: center; margin: 20px 0;
  text-shadow: 0 0 20px rgba(0, 255, 204, 0.5);}</style>""",
  unsafe_allow_html=True)`nst.markdown("<h1 style="text-align: center; color:
  #00ffcc;">💎 QUANTUM CASHFLOW</h1>", unsafe_allow_html=True)`nst.markdown("<p
  style="text-align: center; color: #888;">Institutional Forensic Alpha Detection
  Terminal</p>", unsafe_allow_html=True)`ncol1, col2, col3 = st.columns([1, 2, 1])`nwith
  col2:`n    ticker_input = st.text_input("ENTER TICKER SYMBOL", placeholder="e.g. NVDA,
  AAPL, RELIANCE.NS").upper()`n    analyze_btn = st.button("RUN FORENSIC ANALYSIS",
  use_container_width=True)`nif analyze_btn and ticker_input:`n    with st.spinner("⚡
  Computing Quantum Ratios..."):`n        try:`n            engine =
  QuantumEngine(ticker_input)`n            results = engine.compute_quantum_metrics()`n
           st.markdown(f"<div class="verdict-text">{results["Verdict"]}</div>",
  unsafe_allow_html=True)`n            m1, m2, m3, m4 = st.columns(4)`n            with
  m1: st.markdown(f"<div class="metric-card"><div class="metric-label">Quantum
  Score</div><div class="metric-value">{results["Quantum Score"]}</div></div>",
  unsafe_allow_html=True)`n            with m2: st.markdown(f"<div
  class="metric-card"><div class="metric-label">IOER (Alpha)</div><div
  class="metric-value">{results["IOER"]:.2%}</div></div>", unsafe_allow_html=True)`n
        with m3: st.markdown(f"<div class="metric-card"><div class="metric-label">OER
  (Efficiency)</div><div class="metric-value">{results["OER"]:.2f}</div></div>",
  unsafe_allow_html=True)`n            with m4: st.markdown(f"<div
  class="metric-card"><div class="metric-label">P/OE (Value)</div><div
  class="metric-value">{results["P/OE"]:.2f}</div></div>", unsafe_allow_html=True)`n
        st.markdown("---")`n            st.table(pd.DataFrame([results]))`n
  except Exception as e: st.error(f"Analysis Error: {e}")`nelif not ticker_input and
  analyze_btn: st.warning("Please enter a ticker symbol.")
