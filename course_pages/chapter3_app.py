import streamlit as st
import pandas as pd
import fmpsdk

# API key from Streamlit secrets
API_KEY = st.secrets["api"]["fmp_key"]

# Function to calculate the Acquirer's Multiple
def calculate_acquirers_multiple(market_cap, total_debt, cash_and_equiv, ebit):
    enterprise_value = market_cap + total_debt - cash_and_equiv
    if ebit == 0:
        return None  # Avoid division by zero
    return round(enterprise_value / ebit, 2)

# Function to fetch and return financial data for a given symbol
def fetch_financials(symbol, stock_quotes):
    income_statement = pd.DataFrame(fmpsdk.income_statement(apikey=API_KEY, symbol=symbol, limit=1))
    st.write(income_statement)
    ebit = income_statement["operatingIncome"].iloc[0] if not income_statement.empty else None

    balance_sheet = pd.DataFrame(fmpsdk.balance_sheet_statement(apikey=API_KEY, symbol=symbol, limit=1))
    total_debt = balance_sheet["totalDebt"].iloc[0] if not balance_sheet.empty else None
    cash = balance_sheet["cashAndCashEquivalents"].iloc[0] if not balance_sheet.empty else None

    market_cap = stock_quotes[stock_quotes.symbol == symbol]["marketCap"].values[0]

    if None in (ebit, total_debt, cash, market_cap):
        return None

    multiple = calculate_acquirers_multiple(market_cap, total_debt, cash, ebit)
    ev = market_cap + total_debt - cash

    return {
        "symbol": symbol,
        "enterprise_value": ev,
        "ebit": ebit,
        "multiple": multiple
    }

# Display Function for Streamlit App
def display_acquirers_multiple():
    st.title("🏷️ The Acquirer's Multiple")
    st.write("Explore a deep value metric popularized by Tobias Carlisle: The Acquirer's Multiple.")

    # Load a list of stock symbols and names
    stock_quotes = pd.read_csv("course_pages/stock_quotes_sorted.csv")[["symbol", "name", "marketCap"]][:2500]
    stock_symbols = stock_quotes["symbol"].tolist()

    col1, col2 = st.columns(2)

    with col1:
        symbol1 = st.selectbox("Choose the first company:", stock_symbols, key="symbol1")
    with col2:
        symbol2 = st.selectbox("Choose the second company:", stock_symbols, key="symbol2")

    if symbol1 and symbol2:
        col1, col2 = st.columns(2)

        with col1:
            data1 = fetch_financials(symbol1, stock_quotes)
            st.subheader(f"📊 {symbol1} Analysis")
            if data1:
                st.metric("Enterprise Value", f"${data1['enterprise_value']:,.0f}")
                st.metric("Operating Income (EBIT)", f"${data1['ebit']:,.0f}")
                st.metric("Acquirer's Multiple", data1['multiple'])
            else:
                st.warning("Incomplete data for the first company.")

        with col2:
            data2 = fetch_financials(symbol2, stock_quotes)
            st.subheader(f"📊 {symbol2} Analysis")
            if data2:
                st.metric("Enterprise Value", f"${data2['enterprise_value']:,.0f}")
                st.metric("Operating Income (EBIT)", f"${data2['ebit']:,.0f}")
                st.metric("Acquirer's Multiple", data2['multiple'])
            else:
                st.warning("Incomplete data for the second company.")

        st.caption("Compare the Acquirer's Multiples side by side to identify which company is potentially a better value buy.")

# For standalone testing
if __name__ == "__main__":
    display_acquirers_multiple()
