# course_pages/chapter1_app.py
import streamlit as st
import pandas as pd
import fmpsdk
import random
import time

API_KEY = st.secrets["api"]["fmp_key"]


def get_row_with_retries(sym, api_key, tries=4, min_market_cap=1_000_000_000, excluded_sectors=None):
    for attempt in range(1, tries + 1):
        try:
            return _get_earnings_yield_for_symbol(
                sym,
                api_key,
                min_market_cap=min_market_cap,
                excluded_sectors=excluded_sectors,
            )
        except Exception as e:
            sleep_s = min(8, 0.5 * (2 ** (attempt - 1))) + random.random() * 0.2
            print(f"[RETRY {attempt}/{tries}] {sym}: {e} | sleeping {sleep_s:.2f}s")
            time.sleep(sleep_s)
    return None


def _get_earnings_yield_for_symbol(
    symbol: str,
    api_key: str,
    min_market_cap: int = 1_000_000_000,
    excluded_sectors=None,
) -> dict | None:
    excluded_sectors = set(excluded_sectors) if excluded_sectors else set()

    # --- Quote (price, shares, market cap) ---
    quote_raw = fmpsdk.quote(apikey=api_key, symbol=symbol)
    if not quote_raw:
        raise RuntimeError("quote empty")

    stock_quote = pd.DataFrame(quote_raw)

    price = pd.to_numeric(stock_quote.get("price"), errors="coerce").iloc[0]
    shares_outstanding = pd.to_numeric(stock_quote.get("sharesOutstanding"), errors="coerce").iloc[0]
    market_cap = pd.to_numeric(stock_quote.get("marketCap"), errors="coerce").iloc[0]  # ✅ back to your working way

    if pd.isna(price) or pd.isna(shares_outstanding) or price <= 0 or shares_outstanding <= 0:
        return None

    if pd.isna(market_cap) or market_cap < min_market_cap:
        return None

    # --- Profile (sector) ---
    sector = None
    if excluded_sectors:
        profile_raw = fmpsdk.company_profile(apikey=api_key, symbol=symbol)
        if not profile_raw:
            raise RuntimeError("profile empty")
        sector = profile_raw[0].get("sector")

        if sector in excluded_sectors:
            return None

    # --- Income statement (TTM net income) ---
    income_raw = fmpsdk.income_statement(apikey=api_key, symbol=symbol, period="quarter")
    if not income_raw or len(income_raw) < 4:
        raise RuntimeError("income empty/<4q")

    income_df = pd.DataFrame(income_raw)
    net_income_ttm = pd.to_numeric(income_df["netIncome"], errors="coerce").iloc[:4].sum()
    if pd.isna(net_income_ttm):
        return None

    eps_ttm = float(net_income_ttm) / float(shares_outstanding)
    earnings_yield = eps_ttm / float(price)

    # --- Balance sheet (ROC) ---
    balance_raw = fmpsdk.balance_sheet_statement(apikey=api_key, symbol=symbol, period="quarter")
    if not balance_raw:
        raise RuntimeError("balance empty")

    balance = balance_raw[0]
    total_debt = float(balance.get("totalDebt", 0) or 0)
    equity = balance.get("totalStockholdersEquity")

    roc = None
    if equity is not None:
        equity = float(equity)
        invested_capital = total_debt + equity
        roc = (float(net_income_ttm) / invested_capital) if invested_capital > 0 else None

    return {
        "symbol": symbol,
        "sector": sector,
        "market_cap": float(market_cap),
        "price": float(price),
        "net_income_ttm": float(net_income_ttm),
        "shares_outstanding": float(shares_outstanding),
        "eps_ttm": float(eps_ttm),
        "earnings_yield": float(earnings_yield),
        "roc": (float(roc) if roc is not None else None),
    }


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

    return df.drop_duplicates(subset=["symbol"]).sort_values("symbol")
