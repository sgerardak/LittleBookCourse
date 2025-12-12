# course_pages/chapter1_app.py
import streamlit as st
import pandas as pd
import fmpsdk
from course_pages.functions.stock_utils import fetch_stock_list, fetch_symbol_to_name

# API key
API_KEY = st.secrets["api"]["fmp_key"]


def _filter_morningstar_universe(stock_list: pd.DataFrame) -> pd.DataFrame:
    df = stock_list.copy()

    if "exchangeShortName" in df.columns:
        df = df[df["exchangeShortName"].isin(["NYSE", "NASDAQ", "AMEX"])]

    if "type" in df.columns:
        df["type"] = df["type"].astype(str).str.lower()
        df = df[df["type"] == "stock"]

    def is_common_symbol(sym: str) -> bool:
        if not isinstance(sym, str):
            return False
        if "-" in sym:
            return False
        if "-P" in sym:
            return False
        if sym.endswith(("W", "Z", "U", "WS")):
            return False
        bad_suffixes = ("NOTE", "NTS")
        if any(sym.endswith(suf) for suf in bad_suffixes):
            return False
        return True

    if "symbol" in df.columns:
        df = df[df["symbol"].apply(is_common_symbol)]

    df = df.drop_duplicates(subset=["symbol"]).sort_values("symbol")
    return df


def _get_earnings_yield_for_symbol(symbol: str, api_key: str) -> dict | None:
    """
    Helper used both in this chapter screen and in the Appendix scanner.

    Returns a dict with:
      - symbol
      - price
      - net_income_ttm
      - shares_outstanding
      - eps_ttm
      - earnings_yield

    or None if anything is missing/invalid.
    """
    try:
        # === Quote ===
        quote_raw = fmpsdk.quote(apikey=api_key, symbol=symbol)
        if not isinstance(quote_raw, list) or len(quote_raw) == 0:
            return None
        stock_quote = pd.DataFrame(quote_raw)

        # === Income Statement (quarterly) ===
        income_raw = fmpsdk.income_statement(
            apikey=api_key,
            symbol=symbol,
            period="quarter"
        )
        if not isinstance(income_raw, list) or len(income_raw) == 0:
            return None
        income_statement = pd.DataFrame(income_raw)

        # Basic fields
        stock_price = float(stock_quote["price"].iloc[0])
        shares_outstanding = float(stock_quote["sharesOutstanding"].iloc[0])

        # Be safe in case of weird values
        if stock_price <= 0 or shares_outstanding <= 0:
            return None

        # TTM = sum of last 4 quarters
        net_income = (
            pd.to_numeric(income_statement["netIncome"], errors="coerce")
            .iloc[:4]
            .sum()
        )

        eps = net_income / shares_outstanding
        earnings_yield = eps / stock_price

        return {
            "symbol": symbol,
            "price": stock_price,
            "net_income_ttm": net_income,
            "shares_outstanding": shares_outstanding,
            "eps_ttm": eps,
            "earnings_yield": earnings_yield,
        }
    except Exception:
        # You could log the exception here if you want
        return None


def display_stock_analysis():
    st.title("📊 Stock Analysis Tool")
    st.write("Analyze your favorite company's financial metrics in seconds.")

    # Stock list and dropdown
    stock_list_names = fetch_stock_list(API_KEY)
    stock_list_names = _filter_morningstar_universe(stock_list_names)

    symbol_to_name = fetch_symbol_to_name(stock_list_names)

    default_index = (
        stock_list_names[stock_list_names['symbol'] == "AAPL"].index[0]
        if "AAPL" in stock_list_names['symbol'].values
        else 0
    )

    stock_symbol = st.selectbox(
        "Select a Stock",
        options=stock_list_names['symbol'].tolist(),
        index=int(default_index),
        format_func=lambda x: f"{x} - {symbol_to_name.get(x, x)}",
        help="Choose a stock by its ticker and name."
    )

    st.write(f"Selected Stock Symbol: {stock_symbol}")

    if not stock_symbol:
        st.info("Enter a stock ticker symbol to get started.")
        return

    st.divider()
    try:
        row = _get_earnings_yield_for_symbol(stock_symbol, API_KEY)
        if row is None:
            st.error("⚠️ Could not compute earnings yield (missing data).")
            return

        # === Display Metrics ===
        st.subheader(f"📈 Financial Metrics for {stock_symbol.upper()}")
        st.write(f"**Net Income (TTM):** ${row['net_income_ttm']:,.0f}")
        st.write(f"**Outstanding Shares:** {row['shares_outstanding']:,.0f}")
        st.write(f"**EPS (TTM):** ${row['eps_ttm']:.2f}")
        st.write(f"**Stock Price:** ${row['price']:.2f}")
        st.write(f"**Earnings Yield:** {row['earnings_yield'] * 100:.2f}%")

        # If you still want detailed tables:
        # re-fetch full statements to show in expanders
        income_raw = fmpsdk.income_statement(
            apikey=API_KEY, symbol=stock_symbol, period="quarter"
        )
        balance_raw = fmpsdk.balance_sheet_statement(
            apikey=API_KEY, symbol=stock_symbol, period="quarter"
        )

        if isinstance(income_raw, list) and len(income_raw) > 0:
            income_statement = pd.DataFrame(income_raw)
            with st.expander("📜 View Income Statement (Last 4 Quarters)"):
                st.dataframe(income_statement)

        if isinstance(balance_raw, list) and len(balance_raw) > 0:
            balance_sheet = pd.DataFrame(balance_raw)
            with st.expander("📊 View Balance Sheet (Last 4 Quarters)"):
                st.dataframe(balance_sheet)

    except Exception as e:
        st.error(f"⚠️ An error occurred: {e}")
