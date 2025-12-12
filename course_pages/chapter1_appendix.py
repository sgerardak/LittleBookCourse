# course_pages/chapter1_appendix.py
import streamlit as st
import pandas as pd
from course_pages.functions.stock_utils import fetch_stock_list
from course_pages.chapter1_app import (
    _filter_morningstar_universe,
    _get_earnings_yield_for_symbol,
)

API_KEY = st.secrets["api"]["fmp_key"]


def app():
    st.title("📎 Chapter 1 Appendix – Earnings Yield Scanner")
    st.write("""
    This appendix performs the **earnings yield formula** on **every company** in your stock list
    and ranks them from highest to lowest.  
    You can also export the results to CSV.
    """)

    # Load symbol list
    stock_list = fetch_stock_list(API_KEY)
    stock_list = _filter_morningstar_universe(stock_list)

    symbols = stock_list["symbol"].dropna().unique().tolist()

    st.write(f"Found **{len(symbols)}** symbols in your Morningstar-ready universe.")

    max_default = min(50, len(symbols))
    max_to_scan = st.slider(
        "How many tickers do you want to scan?",
        min_value=10,
        max_value=len(symbols),
        value=max_default,
        step=10,
    )

    run = st.button("🚀 Run Earnings Yield Scan")

    if not run:
        st.info("Click the button above to start scanning.")
        return

    results = []
    progress = st.progress(0)
    status = st.empty()

    to_scan = symbols[:max_to_scan]

    for i, symbol in enumerate(to_scan, start=1):
        status.text(f"Processing {symbol} ({i}/{max_to_scan})...")
        row = _get_earnings_yield_for_symbol(symbol, API_KEY)
        if row:
            results.append(row)

        progress.progress(i / max_to_scan)

    progress.empty()
    status.empty()

    if not results:
        st.error("No data retrieved. Check API limits.")
        return

    df = pd.DataFrame(results)
    df.sort_values("earnings_yield", ascending=False, inplace=True)
    df["earnings_yield_%"] = df["earnings_yield"] * 100

    st.subheader("📊 Earnings Yield Ranking")
    st.dataframe(df)

    csv = df.to_csv(index=False)
    st.download_button(
        label="💾 Download as CSV",
        data=csv,
        file_name="earnings_yield_ranking.csv",
        mime="text/csv",
    )


if __name__ == "__main__":
    app()
