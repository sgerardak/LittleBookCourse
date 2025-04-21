import streamlit as st
import pandas as pd
import fmpsdk
@st.cache_data
def fetch_stock_list(api_key):
    """
    Fetch the list of stocks and preprocess it.
    Returns a filtered DataFrame with 'symbol' and 'name' columns.
    """
    stock_list = pd.DataFrame(fmpsdk.symbols_list(apikey=api_key))

    # Filter by NASDAQ and NYSE
    stock_list = stock_list[stock_list["exchangeShortName"].isin(["NASDAQ", "NYSE"])]

    # Keep only common stocks (exclude ETFs, mutual funds, etc.)
    stock_list = stock_list[stock_list["type"] == "stock"][["symbol", "name"]]

    # Ensure filtering of unwanted stock symbols while keeping -B stocks
    stock_list = stock_list[
        ~stock_list["symbol"].str.endswith('-A') &  # Removes "-A" stocks like "BRK-A"
        ~stock_list["symbol"].str.contains(r'-(P|PR|WS|WT|PC|PD|PL|PW|[C-Z])$', regex=True) |  # Removes preferred stocks
        stock_list["symbol"].str.endswith('-B')  # Keeps "-B" stocks like "BRK-B"
    ]

    stock_list = stock_list.reset_index(drop=True)

    return stock_list

@st.cache_data
def fetch_symbol_to_name(dataframe):
    """
    Create a dictionary mapping stock symbols to names for faster lookup.
    """
    return dict(zip(dataframe['symbol'], dataframe['name']))

