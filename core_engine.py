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
        Computes the proprietary IOER, OER, and the new Efficiency Insurance metrics
        """
        # 1. Extract Raw Data with a WIDE search net for labels
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

        # Broad search for SG&A
        sga = self._get_safe_value(
            self.financials,
            [
                'Selling General Administrative',
                'SG&A',
                'General & Administrative',
                'Selling, General & Administrative',
                'Operating Expenses'
            ]
        )

        # Broad search for Operating Capital
        net_ppe = self._get_safe_value(
            self.balance_sheet,
            ['Net PPE', 'Net Block', 'Property Plant Equipment Net', 'Total PPE']
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

        # 2. Proprietary Calculations
        owner_earnings = net_income + depreciation - capex - changes_in_working_cap

        ioer = (owner_earnings / op_capital) if op_capital != 0 else 0
        oer = (owner_earnings / sga) if sga != 0 else 0

        # Insurance Metrics
        sga_to_oe = (sga / owner_earnings) if owner_earnings != 0 else 0
        sga_to_cap = (sga / op_capital) if op_capital != 0 else 0

        # Price to Owner Earnings (P/OE)
        try:
            price = self.ticker.fast_info.last_price
            shares = self.ticker.fast_info.shares
            market_cap = price * shares
        except Exception:
            market_cap = 0

        poe = (market_cap / owner_earnings) if owner_earnings != 0 else 0

        # Quantum Score Synthesis (0-100)
        score = (
            min(ioer * 100, 33.3)
            + min(oer * 10, 33.3)
            + (100 - min(poe, 33.3))
        )

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
            "Verdict": self._generate_verdict(score)
        }

    def _generate_verdict(self, score):
        if score > 80:
            return "🚀 STRONG ALPHA"
        if score > 60:
            return "📈 BULLISH"
        if score > 40:
            return "⚖️ NEUTRAL"
        return "⚠️ RISK ALERT"
