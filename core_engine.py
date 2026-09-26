
  import yfinance as yf
  import pandas as pd
  import numpy as np

  class QuantumEngine:
      """
      Quantum Cashflow Core Engine
      Proprietary Forensic Accounting for Alpha Detection
      """
      def __init__(self, ticker_symbol):
          self.ticker_symbol = ticker_symbol
          self.ticker = yf.Ticker(ticker_symbol)
          self.financials = self.ticker.financials
          self.balance_sheet = self.ticker.balance_sheet
          self.cashflow = self.ticker.cashflow

      def _get_safe_value(self, dataframe, possible_labels, year_index=0):
          """Searches multiple possible labels to ensure data continuity across different regions"""
          if dataframe is None or dataframe.empty:
              return 0.0

          # Get the column for the most recent year
          try:
              column = dataframe.columns[year_index]
          except IndexError:
              return 0.0

          for label in possible_labels:
              if label in dataframe.index:
                  val = dataframe.loc[label, column]
                  return float(val) if pd.notnull(val) else 0.0
          return 0.0

      def compute_quantum_metrics(self):
          """
          Computes the proprietary IOER, OER, and Quantum Score
          """
          # 1. Extract Raw Data
          net_income = self._get_safe_value(self.financials, ['Net Income'])
          depreciation = self._get_safe_value(self.cashflow, ['Depreciation & Amortization'])
          changes_in_working_cap = self._get_safe_value(self.cashflow, ['Change in Working Capital'])
          capex = abs(self._get_safe_value(self.cashflow, ['Capital Expenditure']))
          sga = self._get_safe_value(self.financials, ['Selling General Administrative', 'SG&A',
  'General & Administrative'])

          # Total Operating Capital (Tangible)
          net_ppe = self._get_safe_value(self.balance_sheet, ['Net PPE', 'Net Block', 'Property Plant
  Equipment Net'])
          current_assets = self._get_safe_value(self.balance_sheet, ['Total Current Assets'])
          current_liabs = self._get_safe_value(self.balance_sheet, ['Total Current Liabilities'])

          op_capital = net_ppe + (current_assets - current_liabs)

          # 2. Proprietary Calculations
          # Owner Earnings = Net Income + Depr - Capex - Change in WC
          owner_earnings = net_income + depreciation - capex - changes_in_working_cap

          # IOER (Incremental Owner Earnings Ratio)
          # Formula: Owner Earnings / Total Operating Capital
          ioer = (owner_earnings / op_capital) if op_capital != 0 else 0

          # OER (Overhead Efficiency Ratio)
          # Formula: Owner Earnings / SG&A
          oer = (owner_earnings / sga) if sga != 0 else 0

          # Price to Owner Earnings (P/OE)
          price = self.ticker.fast_info.last_price
          shares = self.ticker.fast_info.shares
          market_cap = price * shares
          poe = (market_cap / owner_earnings) if owner_earnings != 0 else 0

          # 3. Quantum Score Synthesis (0-100)
          # Weighted average of the 3 metrics normalized against industry benchmarks
          # This is a simplified synthesis for the prototype
          score = (min(ioer * 100, 33.3) + min(oer * 10, 33.3) + (100 - min(poe, 33.3)))

          return {
              "Ticker": self.ticker_symbol.upper(),
              "Owner Earnings": owner_earnings,
              "Op Capital": op_capital,
              "IOER": ioer,
              "OER": oer,
              "P/OE": poe,
              "Quantum Score": round(score, 2),
              "Verdict": self._generate_verdict(score)
          }

      def _generate_verdict(self, score):
          if score > 80: return "🚀 STRONG ALPHA"
          if score > 60: return "📈 BULLISH"
          if score > 40: return "⚖️ NEUTRAL"
          return "⚠️ RISK ALERT"
