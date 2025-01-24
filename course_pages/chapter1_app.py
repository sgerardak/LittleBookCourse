import streamlit as st
import pandas as pd
import fmpsdk

# API key for FMP SDK
API_KEY = st.secrets["api"]["fmp_key"]

@st.cache_data
def fetch_stock_list(api_key):
    """
    Fetch the list of stocks and preprocess it.
    Returns a filtered DataFrame with 'symbol' and 'name' columns.
    """
    stock_list = pd.DataFrame(fmpsdk.symbols_list(apikey=api_key))
    stock_list_names = stock_list[stock_list["exchangeShortName"].isin(["NASDAQ", "NYSE"])]
    stock_list_names = stock_list_names[stock_list_names["type"] == "stock"][["symbol", "name"]]
    ###st.dataframe(stock_list)
    stock_list_names = stock_list_names.reset_index(drop=True)
    return stock_list_names

@st.cache_data
def fetch_symbol_to_name(dataframe):
    """
    Create a dictionary mapping stock symbols to names for faster lookup.
    """
    return dict(zip(dataframe['symbol'], dataframe['name']))

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
            stock_quote = pd.DataFrame(
                fmpsdk.quote(apikey=API_KEY, symbol=stock_symbol)
            )            

            # Calculate Key Metrics
            stock_price=stock_quote["price"][0]
            net_income = income_statement["netIncome"][0:4].sum()
            stocks = stock_quote["sharesOutstanding"][0]
            eps = net_income / stocks
            earnings_yield = eps / stock_price

            # Display Key Metrics
            st.subheader(f"📈 Financial Metrics for {stock_symbol.upper()}")
            st.write(f"**Net Income:** ${net_income:,.0f}")
            st.write(f"**Outstanding Shares:** {stocks:,.0f}")
            st.write(f"**EPS (Earnings Per Share):** ${eps:.2f}")
            st.write(f"**Stock Price:** ${stock_price:.2f}")
            st.write(f"**Earnings Yield:** {earnings_yield * 100:.2f}%")

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
