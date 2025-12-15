# course_pages/Magic Formula Screener.py
import streamlit as st
import pandas as pd
from course_pages.functions.stock_utils import fetch_stock_list
from course_pages.chapter1_app import (
    _filter_morningstar_universe,
    _get_earnings_yield_for_symbol,
)

API_KEY = st.secrets["api"]["fmp_key"]


def app():
    st.title("📎 Magic Formula Screener")
    st.write("""
    This screener computes **Earnings Yield** (+ ROC + Market Cap if your helper returns them)
    for a list of tickers and shows results as they come in.
    You can **Stop** at any time and keep what has already been computed.
    """)

    # -------------------------
    # Session state init
    # -------------------------
    if "mf_running" not in st.session_state:
        st.session_state.mf_running = False
    if "mf_stop" not in st.session_state:
        st.session_state.mf_stop = False
    if "mf_results" not in st.session_state:
        st.session_state.mf_results = []   # list of dict rows
    if "mf_i" not in st.session_state:
        st.session_state.mf_i = 0          # how many tickers processed
    if "mf_to_scan" not in st.session_state:
        st.session_state.mf_to_scan = []   # the tickers list for current run

    # -------------------------
    # Load symbol list (universe)
    # -------------------------
    stock_list = fetch_stock_list(API_KEY)
    stock_list = _filter_morningstar_universe(stock_list)
    symbols = stock_list["symbol"].dropna().unique().tolist()

    st.write(f"Found **{len(symbols)}** symbols in your Morningstar-ready universe.")

    # IMPORTANT: your current slider can crash if len(symbols) < 10
    if len(symbols) < 10:
        st.warning("Universe has fewer than 10 symbols. Scanning all of them.")
        max_to_scan = len(symbols)
    else:
        max_default = min(50, len(symbols))
        max_to_scan = st.slider(
            "How many tickers do you want to scan?",
            min_value=10,
            max_value=len(symbols),
            value=max_default,
            step=10,
        )

    # -------------------------
    # Controls
    # -------------------------
    c1, c2, c3 = st.columns(3)
    with c1:
        run = st.button("🚀 Run / Resume", disabled=False)
    with c2:
        stop = st.button("🛑 Stop", disabled=not st.session_state.mf_running)
    with c3:
        reset = st.button("♻️ Reset")

    if reset:
        st.session_state.mf_running = False
        st.session_state.mf_stop = False
        st.session_state.mf_results = []
        st.session_state.mf_i = 0
        st.session_state.mf_to_scan = []
        st.rerun()

    if stop:
        st.session_state.mf_stop = True

    # If user clicks run/resume, set up the run (only once)
    if run:
        # If not currently running, start a fresh run
        if not st.session_state.mf_running:
            st.session_state.mf_results = []
            st.session_state.mf_i = 0
            st.session_state.mf_to_scan = symbols[:max_to_scan]
            st.session_state.mf_stop = False
            st.session_state.mf_running = True
            st.rerun()
        else:
            # If already running, just rerun (resume loop)
            st.session_state.mf_stop = False
            st.rerun()

    # -------------------------
    # Live UI placeholders
    # -------------------------
    progress = st.progress(0)
    status = st.empty()
    table_ph = st.empty()

    # Always show whatever results we already have
    if st.session_state.mf_results:
        df_live = pd.DataFrame(st.session_state.mf_results)
        table_ph.dataframe(df_live)

    # -------------------------
    # Run loop (only if running)
    # -------------------------
    if not st.session_state.mf_running:
        st.info("Click **Run / Resume** to start scanning.")
        return

    to_scan = st.session_state.mf_to_scan
    total = len(to_scan)

    # If somehow total is 0
    if total == 0:
        st.warning("No tickers to scan.")
        st.session_state.mf_running = False
        return

    # Continue where we left off
    for idx in range(st.session_state.mf_i, total):
        if st.session_state.mf_stop:
            status.warning(f"Stopped. Showing {len(st.session_state.mf_results)} results computed so far.")
            st.session_state.mf_running = False
            break

        symbol = to_scan[idx]
        status.text(f"Processing {symbol} ({idx+1}/{total})...")

        row = _get_earnings_yield_for_symbol(symbol, API_KEY)
        if row:
            st.session_state.mf_results.append(row)

        st.session_state.mf_i = idx + 1

        # Update progress + table incrementally
        progress.progress((idx + 1) / total)
        df_live = pd.DataFrame(st.session_state.mf_results)

        # Optional formatting if columns exist
        if "earnings_yield" in df_live.columns:
            df_live["earnings_yield_%"] = (pd.to_numeric(df_live["earnings_yield"], errors="coerce") * 100).round(2)
        if "roc" in df_live.columns:
            df_live["roc_%"] = (pd.to_numeric(df_live["roc"], errors="coerce") * 100).round(2)
        if "market_cap" in df_live.columns:
            df_live["market_cap_b"] = (pd.to_numeric(df_live["market_cap"], errors="coerce") / 1e9).round(2)

        table_ph.dataframe(df_live)

    # Finished naturally (not stopped)
    if st.session_state.mf_running and not st.session_state.mf_stop and st.session_state.mf_i >= total:
        st.session_state.mf_running = False
        status.success(f"Done. Computed {len(st.session_state.mf_results)} rows.")

    # Final dataframe + download (use what we have)
    if not st.session_state.mf_results:
        st.error("No data retrieved. Check API limits.")
        return

    df = pd.DataFrame(st.session_state.mf_results)

    # Sort if present
    if "earnings_yield" in df.columns:
        df.sort_values("earnings_yield", ascending=False, inplace=True)

    # Add formatted cols if present
    if "earnings_yield" in df.columns:
        df["earnings_yield_%"] = (pd.to_numeric(df["earnings_yield"], errors="coerce") * 100).round(2)
    if "roc" in df.columns:
        df["roc_%"] = (pd.to_numeric(df["roc"], errors="coerce") * 100).round(2)
    if "market_cap" in df.columns:
        df["market_cap_b"] = (pd.to_numeric(df["market_cap"], errors="coerce") / 1e9).round(2)

    st.subheader("📊 Screener Results")
    st.dataframe(df)

    csv = df.to_csv(index=False)
    st.download_button(
        label="💾 Download as CSV",
        data=csv,
        file_name="magic_formula_screener.csv",
        mime="text/csv",
    )


if __name__ == "__main__":
    app()
