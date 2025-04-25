import streamlit as st
import pandas as pd
import fmpsdk
from course_pages.functions.stock_utils import fetch_stock_list, fetch_symbol_to_name

API_KEY = st.secrets["api"]["fmp_key"]

def display_stock_analysis():
    st.title("🏋️‍♀️ FS_Score Analyzer")
    st.write("Evaluate your stock’s financial strength based on the 10-variable FS_Score model.")

    # Fetch symbols and names
    stock_list = fetch_stock_list(API_KEY)
    symbol_to_name = fetch_symbol_to_name(stock_list)
    default_idx = stock_list[stock_list['symbol']=='AAPL'].index[0] if 'AAPL' in stock_list['symbol'].values else 0

    stock_symbol = st.selectbox(
        "Select a Stock",
        options=stock_list['symbol'].tolist(),
        index=int(default_idx),
        format_func=lambda x: f"{x} - {symbol_to_name[x]}",
        help="Choose a stock by its ticker and name."
    )
    st.write(f"Selected Stock Symbol: {stock_symbol}")

    if not stock_symbol:
        st.info("Enter a stock ticker symbol to get started.")
        return

    st.divider()
    try:
        # Load data
        income = pd.DataFrame(fmpsdk.income_statement(apikey=API_KEY, symbol=stock_symbol, period='quarter'))
        balance = pd.DataFrame(fmpsdk.balance_sheet_statement(apikey=API_KEY, symbol=stock_symbol, period='quarter'))
        cashflow = pd.DataFrame(fmpsdk.cash_flow_statement(apikey=API_KEY, symbol=stock_symbol, period='quarter'))

        st.subheader(f"🧮 FS_Score Breakdown for {stock_symbol}")
        score = 0

        # ROA
        net_income = income['netIncome'][0]
        total_assets = balance['totalAssets'][0]
        roa = net_income / total_assets
        passed = roa > 0
        score += int(passed)
        st.write(f"{'✅' if passed else '❌'} **Return on Assets (ROA > 0)**")
        with st.expander("Show ROA details"):
            st.write(f"**Net Income:** ${net_income:,.0f}")
            st.write(f"**Total Assets:** ${total_assets:,.0f}")
            st.write(f"**ROA:** {roa:.2f}")

        # FCFTA
        cfo = cashflow['operatingCashFlow'][0]
        fcfta = cfo / total_assets
        passed = fcfta > 0
        score += int(passed)
        st.write(f"{'✅' if passed else '❌'} **Free Cash Flow to Total Assets (FCFTA > 0)**")
        with st.expander("Show FCFTA details"):
            st.write(f"**CFO:** ${cfo:,.0f}")
            st.write(f"**Total Assets:** ${total_assets:,.0f}")
            st.write(f"**FCFTA:** {fcfta:.4f}")

        # Accruals
        accruals_ratio = cfo / net_income if net_income != 0 else 0
        passed = accruals_ratio > 1
        score += int(passed)
        st.write(f"{'✅' if passed else '❌'} **Accruals (CFO / Net Income > 1)**")
        with st.expander("Show Accruals details"):
            st.write(f"**CFO:** ${cfo:,.0f}")
            st.write(f"**Net Income:** ${net_income:,.0f}")
            st.write(f"**Ratio:** {accruals_ratio:.2f}")

        # Leverage
        ltd_now = balance['longTermDebt'][0]
        assets_prev = balance['totalAssets'][1]
        ltd_prev = balance['longTermDebt'][1]
        leverage_now = ltd_now / total_assets
        leverage_prev = ltd_prev / assets_prev
        passed = leverage_now < leverage_prev
        score += int(passed)
        st.write(f"{'✅' if passed else '❌'} **Change in Leverage (↓)**")
        with st.expander("Show Leverage details"):
            st.write(f"**Debt Now:** ${ltd_now:,.0f}")
            st.write(f"**Assets Now:** ${total_assets:,.0f}")
            st.write(f"**Debt Prev:** ${ltd_prev:,.0f}")
            st.write(f"**Assets Prev:** ${assets_prev:,.0f}")
            st.write(f"**Now Ratio:** {leverage_now:.2f}")
            st.write(f"**Prev Ratio:** {leverage_prev:.2f}")

        # Liquidity
        ca_now = balance['totalCurrentAssets'][0]
        cl_now = balance['totalCurrentLiabilities'][0]
        ca_prev = balance['totalCurrentAssets'][1]
        cl_prev = balance['totalCurrentLiabilities'][1]
        curr_now = ca_now / cl_now
        curr_prev = ca_prev / cl_prev
        passed = curr_now > curr_prev
        score += int(passed)
        st.write(f"{'✅' if passed else '❌'} **Change in Liquidity (↑ Current Ratio)**")
        with st.expander("Show Liquidity details"):
            st.write(f"**Current Assets Now:** ${ca_now:,.0f}")
            st.write(f"**Current Liabilities Now:** ${cl_now:,.0f}")
            st.write(f"**Current Assets Prev:** ${ca_prev:,.0f}")
            st.write(f"**Current Liabilities Prev:** ${cl_prev:,.0f}")
            st.write(f"**Ratio Now:** {curr_now:.2f}")
            st.write(f"**Ratio Prev:** {curr_prev:.2f}")

        # Equity Issuance
        equity_now = balance['totalStockholdersEquity'][0]
        equity_prev = balance['totalStockholdersEquity'][1]
        passed = equity_now <= equity_prev
        score += int(passed)
        st.write(f"{'✅' if passed else '❌'} **Net Equity Issuance (No dilution)**")
        with st.expander("Show Equity details"):
            st.write(f"**Equity Now:** ${equity_now:,.0f}")
            st.write(f"**Equity Prev:** ${equity_prev:,.0f}")

        # ROA Growth
        net_income_prev = income['netIncome'][1]
        roa_prev = net_income_prev / assets_prev
        passed = roa > roa_prev
        score += int(passed)
        st.write(f"{'✅' if passed else '❌'} **Change in ROA (↑)**")
        with st.expander("Show ROA Growth details"):
            st.write(f"**ROA Now:** {roa:.2f}")
            st.write(f"**ROA Prev:** {roa_prev:.2f}")

        # FCFTA Growth
        cfo_prev = cashflow['operatingCashFlow'][1]
        fcfta_prev = cfo_prev / assets_prev
        passed = fcfta > fcfta_prev
        score += int(passed)
        st.write(f"{'✅' if passed else '❌'} **Change in FCFTA (↑)**")
        with st.expander("Show FCFTA Growth details"):
            st.write(f"**FCFTA Now:** {fcfta:.2f}")
            st.write(f"**FCFTA Prev:** {fcfta_prev:.2f}")

        # Gross Margin Growth
        gp_now = income['grossProfit'][0]
        gp_prev = income['grossProfit'][1]
        rev_now = income['revenue'][0]
        rev_prev = income['revenue'][1]
        margin_now = gp_now / rev_now
        margin_prev = gp_prev / rev_prev
        passed = margin_now > margin_prev
        score += int(passed)
        st.write(f"{'✅' if passed else '❌'} **Change in Gross Margin (↑)**")
        with st.expander("Show Margin Growth details"):
            st.write(f"**Margin Now:** {margin_now:.2%}")
            st.write(f"**Margin Prev:** {margin_prev:.2%}")

        # Asset Turnover Growth
        turnover_now = rev_now / total_assets
        turnover_prev = rev_prev / assets_prev
        passed = turnover_now > turnover_prev
        score += int(passed)
        st.write(f"{'✅' if passed else '❌'} **Change in Asset Turnover (↑)**")
        with st.expander("Show Turnover Growth details"):
            st.write(f"**Turnover Now:** {turnover_now:.2f}")
            st.write(f"**Turnover Prev:** {turnover_prev:.2f}")

        # Final Score
        st.markdown(f"### 📊 Final FS_Score: **{score}/10**")
        if score >= 8:
            st.success("This is a financially strong company! 💪")
        elif score >= 5:
            st.info("Decent score. Worth a closer look.")
        else:
            st.warning("Low score — proceed with caution! ⚠️")

        # Raw data expanders
        with st.expander("📜 View Income Statement"):
            st.dataframe(income)
        with st.expander("📊 View Balance Sheet"):
            st.dataframe(balance)
        with st.expander("💸 View Cash Flow Statement"):
            st.dataframe(cashflow)

    except Exception as e:
        st.error(f"⚠️ An error occurred: {e}")

if __name__ == "__main__":
    display_stock_analysis()