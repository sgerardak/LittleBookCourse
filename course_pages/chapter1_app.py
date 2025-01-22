import streamlit as st
import pandas as pd
import fmpsdk

# API key for FMP SDK
API_KEY = st.secrets["api"]["fmp_key"]

# User Input
st.title("📊 Stock Analysis Tool")
st.write("Analyze your favorite company's financial metrics in seconds.")

# Stock Symbol Input
stock_symbol = st.text_input(
    "Enter Stock Symbol",
    value="AAPL",
    help="Example: AAPL for Apple, MSFT for Microsoft.",
    placeholder="Enter a stock ticker",
)

if stock_symbol:
    try:
        # Fetch data using FMP SDK
        income_statement = pd.DataFrame(
            fmpsdk.income_statement(apikey=API_KEY, symbol=stock_symbol, period="quarter")
        )
        balance_sheet = pd.DataFrame(
            fmpsdk.balance_sheet_statement(apikey=API_KEY, symbol=stock_symbol, period="quarter")
        )
        stock_price = fmpsdk.quote_short(apikey=API_KEY, symbol=stock_symbol)[0]["price"]
        income_statement_reported = pd.DataFrame(
            fmpsdk.income_statement_as_reported(apikey=API_KEY, symbol=stock_symbol, period="quarter")
        )
        # Calculate Key Metrics
        net_income = income_statement["netIncome"][0:4].sum()
        stocks = income_statement_reported["weightedaveragenumberofdilutedsharesoutstanding"][0]
        eps = net_income/stocks
        earnings_yield = eps / stock_price

        # Display Metrics with Columns
        st.subheader(f"📈 Financial Metrics for {stock_symbol.upper()} (last 4 semesters)")

        # Abbreviate large numbers and format them for readability
        net_income_display = f"${net_income:,.0f}"  # Format as integer with commas
        stocks_display = f"{stocks/1e6:.2f}M"       # Convert to millions (e.g., 83.28M)
        eps_display = f"${eps:.2f}"                 # Format EPS to 2 decimal places
        stock_price_display = f"${stock_price:.2f}" # Format price to 2 decimal places

        # Display each metric in its own line
        st.write(f"**Net Income:** ${net_income:,.0f}")
        st.write(f"**Outstanding Shares:** {stocks:,.0f}")
        st.write(f"**EPS (Earnings Per Share):** ${eps:.2f}")
        st.write(f"**Stock Price:** ${stock_price:.2f}")
        st.write(f"**Earnings Yield:** {earnings_yield * 100:.2f}%")



        # Expanders for DataFrames
        with st.expander("📜 View Income Statement (Last 4 Quarters)"):
            st.dataframe(income_statement)

        with st.expander("📊 View Balance Sheet (Last 4 Quarters)"):
            st.dataframe(balance_sheet)


    except Exception as e:
        st.error(f"⚠️ An error occurred: {e}")
else:
    st.info("Enter a stock ticker symbol to get started.")
