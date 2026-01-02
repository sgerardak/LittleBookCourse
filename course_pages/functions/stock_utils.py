import streamlit as st
import pandas as pd
import fmpsdk

try:
    import streamlit as st
    cache_data = st.cache_data
except Exception:
    def cache_data(*args, **kwargs):
        def deco(f): return f
        return deco


@cache_data
def fetch_stock_list(api_key: str) -> pd.DataFrame:
    """
    Fetch the list of stocks and preprocess it.
    Returns a filtered DataFrame with 'symbol' and 'name' columns.
    """
    stock_list = pd.DataFrame(fmpsdk.symbols_list(apikey=api_key))

    # ---- Debug (optional: keep while diagnosing, remove later) ----
    # print("COLUMNS:", list(stock_list.columns))
    # print("SAMPLE:", stock_list.head(1).to_dict())

    # ---- Filter by exchange (prefer exchangeShortName) ----
    if "exchangeShortName" in stock_list.columns:
        stock_list = stock_list[stock_list["exchangeShortName"].isin(["NASDAQ", "NYSE"])]
    elif "exchange" in stock_list.columns:
        stock_list = stock_list[stock_list["exchange"].isin(["NASDAQ", "NYSE"])]
    else:
        # If the API payload changes, don't crash the whole app/scan
        # You can tighten this later once you confirm the schema.
        pass

    # ---- Keep only common stocks (exclude ETFs, mutual funds, etc.) ----
    if "type" in stock_list.columns:
        stock_list["type"] = stock_list["type"].astype(str).str.lower()
        stock_list = stock_list[stock_list["type"] == "stock"]

    # Ensure needed columns exist
    if "symbol" not in stock_list.columns:
        raise ValueError(f"FMP symbols_list payload missing 'symbol'. Columns: {list(stock_list.columns)}")
    if "name" not in stock_list.columns:
        # fallback if name isn't present
        stock_list["name"] = ""

    stock_list = stock_list[["symbol", "name"]].copy()
    stock_list["symbol"] = stock_list["symbol"].astype(str)

    # ---- Symbol filtering ----
    # Keep BRK-B, remove BRK-A, remove preferred/warrants/units patterns.
    # If you want different rules, we can tune this.
    def keep_symbol(sym: str) -> bool:
        if not sym:
            return False

        # Keep -B explicitly (e.g., BRK-B)
        if sym.endswith("-B"):
            return True

        # Remove -A explicitly (e.g., BRK-A)
        if sym.endswith("-A"):
            return False

        # Remove anything else with '-' (preferreds, special classes, etc.)
        if "-" in sym:
            return False

        # Remove common warrant/unit suffixes
        if sym.endswith(("W", "WS", "WT", "U", "Z")):
            return False

        # Remove some debt/note-like suffixes
        if sym.endswith(("NOTE", "NTS")):
            return False

        return True

    stock_list = stock_list[stock_list["symbol"].apply(keep_symbol)]

    # Deduplicate and tidy
    stock_list = (
        stock_list.drop_duplicates(subset=["symbol"])
                  .sort_values("symbol")
                  .reset_index(drop=True)
    )
    return stock_list


@cache_data
def fetch_symbol_to_name(dataframe: pd.DataFrame) -> dict:
    """
    Create a dictionary mapping stock symbols to names for faster lookup.
    """
    # Safer than dataframe['symbol'] if columns ever missing
    if "symbol" not in dataframe.columns:
        return {}
    if "name" not in dataframe.columns:
        return dict(zip(dataframe["symbol"], [""] * len(dataframe)))
    return dict(zip(dataframe["symbol"], dataframe["name"]))
