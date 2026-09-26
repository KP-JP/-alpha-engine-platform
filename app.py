import streamlit as st
from core_engine import QuantumEngine
import pandas as pd

  # --- PAGE CONFIG ---
  st.set_page_config(page_title="Quantum Cashflow Terminal", page_icon="💎", layout="wide")

  # --- GLASSMORPHISM CUSTOM CSS ---
  st.markdown("""
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

      /* Metric Card Styling */
      .metric-card {
          background: rgba(255, 255, 255, 0.05);
          backdrop-filter: blur(10px);
          border: 1px solid rgba(255, 255, 255, 0.1);
          border-radius: 15px;
          padding: 20px;
          text-align: center;
          transition: transform 0.3s ease;
      }
      .metric-card:hover {
          transform: translateY(-5px);
          border: 1px solid #00ffcc;
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
      .verdict-text {
          font-size: 3rem;
          font-weight: 800;
          text-align: center;
          margin: 20px 0;
          text-shadow: 0 0 20px rgba(0, 255, 204, 0.5);
      }
      </style>
      """, unsafe_allow_html=True)

  # --- UI LAYOUT ---
  st.markdown('<h1 style="text-align: center; color: #00ffcc;">💎 QUANTUM CASHFLOW</h1>',
  unsafe_allow_html=True)
  st.markdown('<p style="text-align: center; color: #888;">Institutional Forensic Alpha Detection
  Terminal</p>', unsafe_allow_html=True)

  # Input Section
  col1, col2, col3 = st.columns([1, 2, 1])
  with col2:
      ticker_input = st.text_input("ENTER TICKER SYMBOL", placeholder="e.g. NVDA, AAPL,
  RELIANCE.NS").upper()
      analyze_btn = st.button("RUN FORENSIC ANALYSIS", use_container_width=True)

  if analyze_btn and ticker_input:
      with st.spinner("⚡ Accessing SEC Edgar & Computing Quantum Ratios..."):
          try:
              engine = QuantumEngine(ticker_input)
              results = engine.compute_quantum_metrics()

              # Display Verdict
              st.markdown(f'<div class="verdict-text">{results["Verdict"]}</div>',
  unsafe_allow_html=True)

              # Display Metrics in Glassmorphism Cards
              m1, m2, m3, m4 = st.columns(4)

              with m1:
                  st.markdown(f'''<div class="metric-card">
                      <div class="metric-label">Quantum Score</div>
                      <div class="metric-value">{results["Quantum Score"]}</div>
                  </div>''', unsafe_allow_html=True)

              with m2:
                  st.markdown(f'''<div class="metric-card">
                      <div class="metric-label">IOER (Alpha)</div>
                      <div class="metric-value">{results["IOER"]:.2%}</div>
                  </div>''', unsafe_allow_html=True)

              with m3:
                  st.markdown(f'''<div class="metric-card">
                      <div class="metric-label">OER (Efficiency)</div>
                      <div class="metric-value">{results["OER"]:.2f}</div>
                  </div>''', unsafe_allow_html=True)

              with m4:
                  st.markdown(f'''<div class="metric-card">
                      <div class="metric-label">P/OE (Value)</div>
                      <div class="metric-value">{results["P/OE"]:.2f}</div>
                  </div>''', unsafe_allow_html=True)

              # Detailed Data Table
              st.markdown("---")
              st.markdown("<h3 style='color: #888;'>Forensic Breakdown</h3>", unsafe_allow_html=True)
              df = pd.DataFrame([results])
              st.table(df)

          except Exception as e:
              st.error(f"Analysis Error: {e}. Please ensure the ticker is correct (e.g., use .NS for
  Indian stocks).")

  elif not ticker_input and analyze_btn:
      st.warning("Please enter a ticker symbol.")
