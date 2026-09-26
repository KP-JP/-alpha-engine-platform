import streamlit as st
from core_engine import QuantumEngine
import pandas as pd

st.title("💎 Quantum Cashflow (Safe Mode)")

ticker_input = st.text_input("Enter Tickers (comma separated)").upper()
if st.button("Run Scan"):
    tickers = [t.strip() for t in ticker_input.split(",") if t.strip()]
    results = []
    for t in tickers:
        try:
            engine = QuantumEngine(t)
            results.append(engine.compute_quantum_metrics())
        except Exception as e:
            st.error(f"Error {t}: {e}")
    if results:
        st.table(pd.DataFrame(results))
