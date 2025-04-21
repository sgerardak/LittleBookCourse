import streamlit as st
import pandas as pd
import fmpsdk
from course_pages.functions.stock_utils import fetch_stock_list,fetch_symbol_to_name

# API key for FMP SDK
API_KEY = st.secrets["api"]["fmp_key"]

def display_stock_analysis():
    # Title and Description
    st.title("📊 Stock Analysis Tool")
    st.write("Analyze your favorite company's financial metrics in seconds.")
    
    # Fetch and preprocess stock list
    stock_list_names = fetch_stock_list(API_KEY)
    symbol_to_name = fetch_symbol_to_name(stock_list_names)

    # Default index for "AAPL"
    default_index = stock_list_names[stock_list_names['symbol'] == "AAPL"].index[0] if "AAPL" in stock_list_names['symbol'].values else 0

    # Dropdown for Stock Symbol Selection
    stock_symbol = st.selectbox(
        "Select a Stock",
        options=stock_list_names['symbol'].tolist(),
        index=int(default_index),
        format_func=lambda x: f"{x} - {symbol_to_name[x]}",
        help="Choose a stock by its ticker and name."
    )
    st.write(f"Selected Stock Symbol: {stock_symbol}")

    if stock_symbol:
        st.divider()  # Add spacing before metrics
        try:
            # Fetch data using FMP SDK
            income_statement = pd.DataFrame(
                fmpsdk.income_statement(apikey=API_KEY, symbol=stock_symbol, period="quarter")
            )
            balance_sheet = pd.DataFrame(
                fmpsdk.balance_sheet_statement(apikey=API_KEY, symbol=stock_symbol, period="quarter")
            )     


            # Calculate Key Metrics
            net_income = income_statement["netIncome"][0:4].sum()
            total_debt = balance_sheet["totalDebt"][0]
            total_equity = balance_sheet["totalStockholdersEquity"][0]
            invested_capital = total_debt + total_equity
            roc=net_income/invested_capital*100


            # Display Key Metrics
            st.subheader(f"📈 Financial Metrics for {stock_symbol.upper()}")
            st.write(f"**Net Income:** ${net_income:,.0f}")
            st.write(f"**Total Debt:** ${total_debt:,.0f}")
            st.write(f"**Equity:** ${total_equity:,.0f}")
            st.write(f"**Invested Capital:** ${invested_capital:,.0f}")
            st.write(f"**Return on Capital (ROC):** {roc:,.2f}%")

            # Expanders for Detailed Statements
            with st.expander("📜 View Income Statement (Last 4 Quarters)"):
                st.dataframe(income_statement)

            with st.expander("📊 View Balance Sheet (Last 4 Quarters)"):
                st.dataframe(balance_sheet)

        except Exception as e:
            st.error(f"⚠️ An error occurred: {e}")
    else:
        st.info("Enter a stock ticker symbol to get started.")

if __name__ == "__main__":
    display_stock_analysis()
