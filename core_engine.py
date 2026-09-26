import yfinance as yf
import pandas as pd
import numpy as np


class QuantumEngine:
    def __init__(self, ticker_symbol):
        self.ticker_symbol = ticker_symbol
        try:
            self.ticker = yf.Ticker(ticker_symbol)
            self.financials = self.ticker.financials
            self.balance_sheet = self.ticker.balance_sheet
            self.cashflow = self.ticker.cashflow
        except Exception:
            self.financials = pd.DataFrame()
            self.balance_sheet = pd.DataFrame()
            self.cashflow = pd.DataFrame()

    def _get_safe_value(self, dataframe, possible_labels, year_index=0):
        if dataframe is None or dataframe.empty:
            return 0.0
        try:
            column = dataframe.columns[year_index]
            # 1. Try exact match first
            for label in possible_labels:
                if label in dataframe.index:
                    val = dataframe.loc[label, column]
                    return float(val) if pd.notnull(val) else 0.0

            # 2. DEEP SEARCH: Look for keywords in any index label
            for index_label in dataframe.index:
                index_str = str(index_label).lower()
                # Search for SG&A keywords
                if any(kw in index_str for kw in ['selling', 'administrative', 'sga', 'general']):
                    val = dataframe.loc[index_label, column]
                    return float(val) if pd.notnull(val) else 0.0
        except Exception:
            return 0.0
        return 0.0

    def compute_quantum_metrics(self):
        # 1. Basic Extractions
        net_income = self._get_safe_value(
            self.financials,
            ['Net Income', 'Net Income Common Stockholders']
        )
        depreciation = self._get_safe_value(
            self.cashflow,
            ['Depreciation & Amortization', 'Depreciation']
        )
        changes_in_working_cap = self._get_safe_value(
            self.cashflow,
            ['Change in Working Capital', 'Working Capital Change']
        )
        capex = abs(self._get_safe_value(
            self.cashflow,
            ['Capital Expenditure', 'Capital Expenditures']
        ))

        # Deep search for SG&A
        sga = self._get_safe_value(
            self.financials,
            ['Selling General Administrative', 'SG&A', 'General & Administrative']
        )

        # Operating Capital
        net_ppe = self._get_safe_value(
            self.balance_sheet,
            ['Net PPE', 'Net Block', 'Total PPE', 'Property Plant Equipment']
        )
        current_assets = self._get_safe_value(
            self.balance_sheet,
            ['Total Current Assets', 'Current Assets']
        )
        current_liabs = self._get_safe_value(
            self.balance_sheet,
            ['Total Current Liabilities', 'Current Liabilities']
        )

        op_capital = net_ppe + (current_assets - current_liabs)
        owner_earnings = net_income + depreciation - capex - changes_in_working_cap

        # Ratios
        ioer = (owner_earnings / op_capital) if op_capital != 0 else 0
        oer = (owner_earnings / sga) if sga != 0 else 0
        sga_to_oe = (sga / owner_earnings) if owner_earnings != 0 else 0
        sga_to_cap = (sga / op_capital) if op_capital != 0 else 0

        try:
            price = self.ticker.fast_info.last_price
            shares = self.ticker.fast_info.shares
            market_cap = price * shares
        except Exception:
            market_cap = 0

        poe = (market_cap / owner_earnings) if owner_earnings != 0 else 0
        score = (min(ioer * 100, 33.3) + min(oer * 10, 33.3) + (100 - min(poe, 33.3)))

        return {
            "Ticker": self.ticker_symbol.upper(),
            "Owner Earnings": owner_earnings,
            "Op Capital": op_capital,
            "IOER": ioer,
            "OER": oer,
            "SGA/OE": sga_to_oe,
            "SGA/Cap": sga_to_cap,
            "P/OE": poe,
            "Quantum Score": round(score, 2),
            "Verdict": "ANALYZED"
        }
