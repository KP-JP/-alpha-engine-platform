import streamlit as st
  import pandas as pd
  import yfinance as yf

  # --- SECURE PROPRIETARY MODULES ---
  def get_forensic_metrics(ticker):
      try:
          s = yf.Ticker(ticker)
          cf = s.cashflow
          bs = s.balance_sheet

          if cf.empty or bs.empty:
              return {"Error": "Data not found"}

          # CFO Extraction
          cl = cf.loc['Operating Cash Flow'].iloc[0] if 'Operating Cash Flow' in cf.index else 0
          co = cf.loc['Operating Cash Flow'].iloc[1] if 'Operating Cash Flow' in cf.index and
  len(cf.loc['Operating Cash Flow']) > 1 else 0

          # Operating Capital Extraction
          ol = bs.loc['Net PPE'].iloc[0] if 'Net PPE' in bs.index else 0
          oo = bs.loc['Net PPE'].iloc[1] if 'Net PPE' in bs.index and len(bs.loc['Net PPE']) > 1 else 0

          ioer = (cl - co) / (ol - oo) if (ol - oo) != 0 else 0

          # Owner Earnings & SGA (The Bloat Filter)
          capex = abs(cf.loc['Capital Expenditure'].iloc[0]) if 'Capital Expenditure' in cf.index else 0
          owner_earnings = cl - capex

          sga_labels = ['Selling General and Administrative', 'Operating Expenses', 'General and
  Administrative']
          sga = 0
          for l in sga_labels:
              if l in cf.index:
                  sga = abs(cf.loc[l].iloc[0])
                  break

          oer = owner_earnings / sga if sga != 0 else 0

          return {"IOER": ioer, "OER": oer, "OE": owner_earnings, "OpCap": ol}
      except Exception as e:
          return {"Error": str(e)}

  def classify(ioer, oer):
      if ioer > 1.0 and oer > 1.0: return "💎 PERFECT ALPHA", "green"
      if ioer > 1.0: return "🚀 ASSET ALPHA", "lightgreen"
      if oer > 1.0: return "⚙️ OPS ALPHA", "yellow"
      if ioer < 0.1 and oer < 0.5: return "❌ DOUBLE DANGER", "red"
      return "⚖️ NEUTRAL", "gray"

  # --- STREAMLIT UI ---
  st.set_page_config(page_title="Alpha Engine", layout="wide")
  st.title("⚡ ALPHA ENGINE: Forensic Valuation")

  st.sidebar.header("Control Panel")
  ticker = st.sidebar.text_input("Enter Ticker (e.g., NVDA, ITC.NS)", "NVDA")
  run = st.sidebar.button("Run Forensic Scan")

  if run:
      with st.spinner('Analyzing...'):
          res = get_forensic_metrics(ticker)
          if "Error" in res:
              st.error(res["Error"])
          else:
              verdict, color = classify(res['IOER'], res['OER'])
              c1, c2, c3 = st.columns(3)
              c1.metric("IOER", f"{res['IOER']:.2f}")
              c2.metric("OER", f"{res['OER']:.2f}")
              c3.markdown(f"**Verdict:** <h2 style='color:{color};'>{verdict}</h2>",
  unsafe_allow_html=True)
              st.divider()
              st.write(f"Analysis: Owner Earnings ${res['OE']:,.0f} | OpCap ${res['OpCap']:,.0f}")

  st.info("Legal Disclaimer: Not financial advice. Proprietary Alpha Engine Logic.")
