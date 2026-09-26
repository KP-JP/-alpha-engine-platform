import yfinance as yf
import pandas as pd
import numpy as np


class QuantumEngine:
    """
    Quantum Cashflow Core Engine v2.1
    Temporal Forensic Accounting with Zero-Floor Guardrails
    """

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
            if year_index >= len(dataframe.columns):
                return 0.0
            column = dataframe.columns[year_index]
            for label in possible_labels:
                if label in dataframe.index:
                    val = dataframe.loc[label, column]
                    return float(val) if pd.notnull(val) else 0.0

            for index_label in dataframe.index:
                index_str = str(index_label).lower()
                if any(kw in index_str for kw in ['selling', 'administrative', 'sga', 'general']):
                    val = dataframe.loc[index_label, column]
                    return float(val) if pd.notnull(val) else 0.0
        except Exception:
            return 0.0
        return 0.0

    def compute_temporal_metrics(self, start_year_idx=0, end_year_idx=None):
        if self.financials.empty:
            return None

        max_years = len(self.financials.columns)
        if end_year_idx is None:
            end_year_idx = max_years

        effective_end = min(end_year_idx, max_years)
        yearly_data = []

        for i in range(start_year_idx, effective_end):
            net_income = self._get_safe_value(
                self.financials,
                ['Net Income', 'Net Income Common Stockholders'],
                i
            )
            depreciation = self._get_safe_value(
                self.cashflow,
                ['Depreciation & Amortization', 'Depreciation'],
                i
            )
            changes_in_working_cap = self._get_safe_value(
                self.cashflow,
                ['Change in Working Capital', 'Working Capital Change'],
                i
            )
            capex = abs(self._get_safe_value(
                self.cashflow,
                ['Capital Expenditure', 'Capital Expenditures'],
                i
            ))
            sga = self._get_safe_value(
                self.financials,
                ['Selling General Administrative', 'SG&A', 'General & Administrative'],
                i
            )

            net_ppe = self._get_safe_value(
                self.balance_sheet,
                ['Net PPE', 'Net Block', 'Total PPE'],
                i
            )
            current_assets = self._get_safe_value(
                self.balance_sheet,
                ['Total Current Assets', 'Current Assets'],
                i
            )
            current_liabs = self._get_safe_value(
                self.balance_sheet,
                ['Total Current Liabilities', 'Current Liabilities'],
                i
            )

            op_capital = net_ppe + (current_assets - current_liabs)
            owner_earnings = net_income + depreciation - capex - changes_in_working_cap

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

            yearly_data.append({
                "Year": self.financials.columns[i],
                "Owner Earnings": owner_earnings,
                "Op Capital": op_capital,
                "IOER": ioer,
                "OER": oer,
                "SGA/OE": sga_to_oe,
                "SGA/Cap": sga_to_cap,
                "P/OE": poe
            })

        if not yearly_data:
            return None

        avg_ioer = float(np.mean([d['IOER'] for d in yearly_data]))
        avg_oer = float(np.mean([d['OER'] for d in yearly_data]))
        avg_poe = float(np.mean([d['P/OE'] for d in yearly_data]))
        avg_sga_oe = float(np.mean([d['SGA/OE'] for d in yearly_data]))
        avg_sga_cap = float(np.mean([d['SGA/Cap'] for d in yearly_data]))

        # GUARDRAILS
        avg_oe = float(np.mean([d['Owner Earnings'] for d in yearly_data]))
        if avg_oe <= 0:
            agg_score = 0.0
        else:
            poe_contribution = (100 - min(avg_poe, 33.3)) if avg_poe > 0 else 0
            agg_score = (
                min(avg_ioer * 100, 33.3)
                + min(avg_oer * 10, 33.3)
                + poe_contribution
            )

        return {
            "Ticker": self.ticker_symbol.upper(),
            "Average_IOER": avg_ioer,
            "Average_OER": avg_oer,
            "Average_SGA_OE": avg_sga_oe,
            "Average_SGA_Cap": avg_sga_cap,
            "Average_P_OE": avg_poe,
            "Quantum Score": round(max(0, agg_score), 2),
            "Temporal_Data": yearly_data,
            "Verdict": self._generate_verdict(agg_score)
        }

    # Backward compatibility for single-year app calls
    def compute_quantum_metrics(self):
        res = self.compute_temporal_metrics(start_year_idx=0, end_year_idx=1)
        if res is None:
            return {
                "Ticker": self.ticker_symbol.upper(),
                "Quantum Score": 0.0,
                "Verdict": "NO DATA"
            }
        latest = res["Temporal_Data"][0] if res["Temporal_Data"] else {}
        return {
            "Ticker": res["Ticker"],
            "Owner Earnings": latest.get("Owner Earnings", 0.0),
            "Op Capital": latest.get("Op Capital", 0.0),
            "IOER": latest.get("IOER", 0.0),
            "OER": latest.get("OER", 0.0),
            "SGA/OE": latest.get("SGA/OE", 0.0),
            "SGA/Cap": latest.get("SGA/Cap", 0.0),
            "P/OE": latest.get("P/OE", 0.0),
            "Quantum Score": res["Quantum Score"],
            "Verdict": res["Verdict"]
        }

    def _generate_verdict(self, score):
        if score > 80:
            return "🚀 STRONG ALPHA"
        if score > 60:
            return "📈 BULLISH"
        if score > 40:
            return "⚖️ NEUTRAL"
        return "⚠️ RISK ALERT"
