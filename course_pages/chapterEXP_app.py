import streamlit as st
import pandas as pd
import fmpsdk
#from course_pages.functions.stock_utils import fetch_stock_list,fetch_symbol_to_name

# API key for FMP SDK
API_KEY = st.secrets["api"]["fmp_key"]

def display_stock_analysis():
    # Title and Description
    st.title("📊 Stock Analysis Tool")
    st.write("Analyze your favorite company's financial metrics in seconds.")
    stock_quotes=pd.read_csv("course_pages/stock_quotes_sorted.csv")[["symbol","name","marketCap"]][:2500]
    key_metrics = pd.DataFrame(fmpsdk.key_metrics(apikey=API_KEY, symbol="AAPL"))
    st.dataframe(key_metrics)
    stock_symbols=stock_quotes["symbol"].tolist()
    # Fetch and preprocess stock list
    ''' income_statement = pd.DataFrame(
                fmpsdk.income_statement(apikey=API_KEY, symbol="AAPL")
            )
    st.dataframe(income_statement)
    st.dataframe(stock_quotes["symbol"].tolist())
    balance_sheet = pd.DataFrame(
                fmpsdk.balance_sheet_statement(apikey=API_KEY, symbol=["AAPL", "CSCO", "QQQQ"])
            )     


    # Calculate Key Metrics
    net_income = income_statement["netIncome"][0:4].sum()
    total_debt = balance_sheet["totalDebt"][0]
    total_equity = balance_sheet["totalStockholdersEquity"][0]
    invested_capital = total_debt + total_equity
    roc=net_income/invested_capital*100'''

    # Initialize an empty DataFrame
    financial_data = pd.DataFrame()

    # Loop through each stock symbol
    for symbol in stock_symbols:
        # Fetch financial key metrics (which includes ROIC & Earnings Yield)
        key_metrics = pd.DataFrame(fmpsdk.key_metrics(apikey=API_KEY, symbol=symbol, limit=1))

        if not key_metrics.empty:
            # Select only necessary columns
            key_metrics = key_metrics[["symbol", "date", "calendarYear", "period", "roic", "earningsYield"]]

            # Append to the master DataFrame
            financial_data = pd.concat([financial_data, key_metrics], ignore_index=True)

    # Display the final DataFrame in Streamlit
    st.dataframe(financial_data)

if __name__ == "__main__":
    display_stock_analysis()