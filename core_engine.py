import yfinance as yf`nimport pandas as
  pd`nimport numpy as np`nclass QuantumEngine:`n    def __init__(self, ticker_symbol):`n
        self.ticker_symbol = ticker_symbol`n        self.ticker =
  yf.Ticker(ticker_symbol)`n        self.financials = self.ticker.financials`n
  self.balance_sheet = self.ticker.balance_sheet`n        self.cashflow =
  self.ticker.cashflow`n    def _get_safe_value(self, dataframe, possible_labels,
  year_index=0):`n        if dataframe is None or dataframe.empty: return 0.0`n
  try: column = dataframe.columns[year_index]`n        except IndexError: return 0.0`n
      for label in possible_labels:`n            if label in dataframe.index:`n
        val = dataframe.loc[label, column]`n                return float(val) if
  pd.notnull(val) else 0.0`n        return 0.0`n    def compute_quantum_metrics(self):`n
        net_income = self._get_safe_value(self.financials, ["Net Income"])`n
  depreciation = self._get_safe_value(self.cashflow, ["Depreciation & Amortization"])`n
       changes_in_working_cap = self._get_safe_value(self.cashflow, ["Change in Working
  Capital"])`n        capex = abs(self._get_safe_value(self.cashflow, ["Capital
  Expenditure"]))`n        sga = self._get_safe_value(self.financials, ["Selling General
  Administrative", "SG&A", "General & Administrative"])`n        net_ppe =
  self._get_safe_value(self.balance_sheet, ["Net PPE", "Net Block", "Property Plant
  Equipment Net"])`n        current_assets = self._get_safe_value(self.balance_sheet,
  ["Total Current Assets"])`n        current_liabs =
  self._get_safe_value(self.balance_sheet, ["Total Current Liabilities"])`n
  op_capital = net_ppe + (current_assets - current_liabs)`n        owner_earnings =
  net_income + depreciation - capex - changes_in_working_cap`n        ioer =
  (owner_earnings / op_capital) if op_capital != 0 else 0`n        oer = (owner_earnings
  / sga) if sga != 0 else 0`n        price = self.ticker.fast_info.last_price`n
  shares = self.ticker.fast_info.shares`n        market_cap = price * shares`n        poe
  = (market_cap / owner_earnings) if owner_earnings != 0 else 0`n        score =
  (min(ioer * 100, 33.3) + min(oer * 10, 33.3) + (100 - min(poe, 33.3)))`n        return
  {"Ticker": self.ticker_symbol.upper(), "Owner Earnings": owner_earnings, "Op Capital":
  op_capital, "IOER": ioer, "OER": oer, "P/OE": poe, "Quantum Score": round(score, 2),
  "Verdict": self._generate_verdict(score)}`n    def _generate_verdict(self, score):`n
      if score > 80: return "🚀 STRONG ALPHA"`n        if score > 60: return "📈
  BULLISH"`n        if score > 40: return "⚖️ NEUTRAL"`n        return "⚠️ RISK ALERT"
