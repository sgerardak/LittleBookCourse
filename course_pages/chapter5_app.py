# course_pages/chapter5_app.py
import streamlit as st
import pandas as pd
import fmpsdk
import random
import time

API_KEY = st.secrets["api"]["fmp_key"]

# -----------------------------
# Cache helper (match your style)
# -----------------------------
try:
    cache_data = st.cache_data
except Exception:
    def cache_data(*args, **kwargs):
        def deco(f): return f
        return deco


# -----------------------------
# Generic retry wrapper (match your Chapter 1 style)
# -----------------------------
def _with_retries(fn, tries=4, label="call"):
    for attempt in range(1, tries + 1):
        try:
            return fn()
        except Exception as e:
            sleep_s = min(8, 0.5 * (2 ** (attempt - 1))) + random.random() * 0.2
            print(f"[RETRY {attempt}/{tries}] {label}: {e} | sleeping {sleep_s:.2f}s")
            time.sleep(sleep_s)
    return None


# -----------------------------
# FMP fetchers (cached)
# -----------------------------
@cache_data
def _fetch_cashflow(symbol: str, period: str, limit: int, api_key: str) -> pd.DataFrame:
    """
    period: 'annual' or 'quarter'
    """
    raw = fmpsdk.cash_flow_statement(apikey=api_key, symbol=symbol, period=period)
    if not raw:
        raise RuntimeError("cash_flow_statement empty")

    df = pd.DataFrame(raw)

    # FMP returns more rows than needed; keep the latest `limit`
    # The API typically returns newest first, but we'll be defensive and just take head(limit).
    df = df.head(limit).copy()
    return df


@cache_data
def _fetch_quote(symbol: str, api_key: str) -> pd.DataFrame:
    raw = fmpsdk.quote(apikey=api_key, symbol=symbol)
    if not raw:
        raise RuntimeError("quote empty")
    return pd.DataFrame(raw)


@cache_data
def _fetch_income(symbol: str, period: str, limit: int, api_key: str) -> pd.DataFrame:
    raw = fmpsdk.income_statement(apikey=api_key, symbol=symbol, period=period)
    if not raw:
        raise RuntimeError("income_statement empty")
    df = pd.DataFrame(raw).head(limit).copy()
    return df


# -----------------------------
# DCF mechanics
# -----------------------------
def _safe_float(x):
    try:
        return float(x)
    except Exception:
        return None


def _compute_fcf_from_cashflow_row(row: dict) -> float | None:
    """
    Prefer 'freeCashFlow' if present.
    Else compute: operatingCashFlow - abs(capitalExpenditure)
    """
    fcf = _safe_float(row.get("freeCashFlow"))
    if fcf is not None:
        return fcf

    cfo = _safe_float(row.get("operatingCashFlow"))
    capex = _safe_float(row.get("capitalExpenditure"))

    if cfo is None or capex is None:
        return None

    return cfo - abs(capex)


def _run_dcf(
    fcf_year1: float,
    growth: float,
    discount_rate: float,
    terminal_growth: float = 0.03,
    years: int = 10,
) -> dict:
    """
    Year t forecast:
      FCF_t = FCF_1 * (1+growth)^(t-1)

    PV:
      PV_t = FCF_t / (1+r)^t

    Terminal:
      TV = FCF_10*(1+g)/(r-g)
      PV_TV = TV/(1+r)^10
    """
    rows = []
    pv_10y = 0.0

    for t in range(1, years + 1):
        fcf_t = fcf_year1 * ((1 + growth) ** (t - 1))
        disc = 1.0 / ((1 + discount_rate) ** t)
        pv_t = fcf_t * disc
        pv_10y += pv_t
        rows.append(
            {
                "Year": t,
                "Forecast FCF": fcf_t,
                "Discount Factor": disc,
                "Present Value": pv_t,
            }
        )

    fcf_10 = rows[-1]["Forecast FCF"]
    terminal_value = (fcf_10 * (1 + terminal_growth)) / (discount_rate - terminal_growth)
    pv_terminal = terminal_value / ((1 + discount_rate) ** years)
    intrinsic_value = pv_10y + pv_terminal

    return {
        "forecast_df": pd.DataFrame(rows),
        "pv_10y": pv_10y,
        "terminal_value": terminal_value,
        "pv_terminal": pv_terminal,
        "intrinsic_value": intrinsic_value,
    }


# -----------------------------
# Public function used by chapter5.py
# -----------------------------
def display_intrinsic_value_analysis():
    st.subheader("📌 Chapter 5 App — Intrinsic Value (DCF)")

    symbol = st.text_input("Stock ticker", value="AAPL").upper().strip()

    # --- Fetch data with retries (match your approach)
    cashflow_annual_df = _with_retries(
        lambda: _fetch_cashflow(symbol, period="annual", limit=5, api_key=API_KEY),
        label=f"{symbol} cashflow annual",
    )
    cashflow_quarter_df = _with_retries(
        lambda: _fetch_cashflow(symbol, period="quarter", limit=4, api_key=API_KEY),
        label=f"{symbol} cashflow quarter",
    )
    quote_df = _with_retries(
        lambda: _fetch_quote(symbol, api_key=API_KEY),
        label=f"{symbol} quote",
    )

    if cashflow_annual_df is None or cashflow_quarter_df is None or quote_df is None:
        st.error("Could not fetch the required data after retries. Try again or try another ticker.")
        return

    # --- Display raw data tables (as you requested)
    st.markdown("### 1) Cash Flow (Last 5 years)")
    annual_cols_pref = ["date", "calendarYear", "period", "operatingCashFlow", "capitalExpenditure", "freeCashFlow"]
    annual_cols = [c for c in annual_cols_pref if c in cashflow_annual_df.columns]
    st.dataframe(
        cashflow_annual_df[annual_cols] if annual_cols else cashflow_annual_df,
        use_container_width=True
    )

    st.markdown("### 2) Cash Flow (Last 4 quarters)")
    quarter_cols_pref = ["date", "calendarYear", "period", "operatingCashFlow", "capitalExpenditure", "freeCashFlow"]
    quarter_cols = [c for c in quarter_cols_pref if c in cashflow_quarter_df.columns]

    # Build a display df (copy) and append a "TTM / Sum" row for numeric columns
    q_display = cashflow_quarter_df[quarter_cols].copy() if quarter_cols else cashflow_quarter_df.copy()

    # Identify numeric columns we want to sum
    numeric_sum_cols = [c for c in ["operatingCashFlow", "capitalExpenditure", "freeCashFlow"] if c in q_display.columns]

    sum_row = {}
    for c in q_display.columns:
        if c in numeric_sum_cols:
            sum_row[c] = pd.to_numeric(q_display[c], errors="coerce").iloc[:4].sum()
        elif c == "date":
            sum_row[c] = "TTM (sum)"
        elif c == "calendarYear":
            sum_row[c] = ""
        elif c == "period":
            sum_row[c] = ""
        else:
            sum_row[c] = ""

    q_display = pd.concat([q_display.iloc[:4], pd.DataFrame([sum_row])], ignore_index=True)

    st.dataframe(q_display, use_container_width=True)


    # --- Helpful defaults for "starting cash flow"
    last_annual_fcf = None
    if not cashflow_annual_df.empty:
        last_annual_fcf = _compute_fcf_from_cashflow_row(cashflow_annual_df.iloc[0].to_dict())

    ttm_fcf = None
    if len(cashflow_quarter_df) >= 4:
        fcfs = []
        for _, r in cashflow_quarter_df.iterrows():
            v = _compute_fcf_from_cashflow_row(r.to_dict())
            if v is not None:
                fcfs.append(v)
        if len(fcfs) == 4:
            ttm_fcf = sum(fcfs)

    # --- Inputs (your 4 inputs)
    st.markdown("---")
    st.markdown("## Choose your 4 inputs")

    st.markdown("### ✅ Input 1 — Next year cash flow (starting point)")
    hint = None
    if ttm_fcf is not None:
        st.caption("Suggestion: using **TTM FCF** computed from the last 4 quarters.")
        hint = ttm_fcf
    elif last_annual_fcf is not None:
        st.caption("Suggestion: using the **most recent annual FCF**.")
        hint = last_annual_fcf

    fcf_year1 = st.number_input(
        "Estimated FCF for NEXT year (FCF₁)",
        value=float(hint) if hint is not None else 1_000.0,
        step=100.0,
        format="%.2f",
    )

    st.markdown("### ✅ Input 2 — Growth assumption (Years 1–10)")

    growth_pct = st.number_input(
        "Annual growth rate (%)",
        value=5.0,
        min_value=-20.0,
        max_value=30.0,
        step=0.5,
        format="%.2f",
    )

    growth = float(growth_pct) / 100.0


    st.markdown("### ✅ Input 3 — Risk bucket (Discount rate)")
    risk_choice = st.selectbox("How risky is the company?", ["Low risk (9%)", "Mid risk (12%)", "High risk (15%)"], index=1)
    if risk_choice.startswith("Low"):
        discount_rate = 0.09
    elif risk_choice.startswith("Mid"):
        discount_rate = 0.12
    else:
        discount_rate = 0.15

    st.markdown("### ✅ Input 4 — Terminal growth (Conservative default)")
    terminal_growth = 0.03
    st.write(f"Terminal growth rate (g) = **{terminal_growth*100:.0f}%**")

    if terminal_growth >= discount_rate:
        st.error("Terminal growth must be lower than discount rate (r > g).")
        return

    # --- Run DCF
    st.markdown("---")
    st.markdown("## 3) DCF Results")

    result = _run_dcf(
        fcf_year1=fcf_year1,
        growth=growth,
        discount_rate=discount_rate,
        terminal_growth=terminal_growth,
        years=10,
    )

    forecast_df = result["forecast_df"].copy()
    forecast_df["Forecast FCF"] = pd.to_numeric(forecast_df["Forecast FCF"], errors="coerce").round(2)
    forecast_df["Discount Factor"] = pd.to_numeric(forecast_df["Discount Factor"], errors="coerce").round(6)
    forecast_df["Present Value"] = pd.to_numeric(forecast_df["Present Value"], errors="coerce").round(2)

    st.subheader("📋 10-year forecast table")
    st.dataframe(forecast_df, use_container_width=True)

    st.markdown(
        f"""
**PV of Years 1–10** = **{result["pv_10y"]:,.2f}**  
**Terminal Value (at Year 10)** = **{result["terminal_value"]:,.2f}**  
**PV of Terminal Value** = **{result["pv_terminal"]:,.2f}**
"""
    )
    st.success(f"✅ Intrinsic value (DCF) = **{result['intrinsic_value']:,.2f}**")

    # --- Shares + fair value per share (same style as your earlier work)
    st.markdown("---")
    st.markdown("## 4) Fair value per share")

    shares_outstanding = None
    try:
        shares_outstanding = pd.to_numeric(quote_df.get("sharesOutstanding"), errors="coerce").iloc[0]
        if pd.isna(shares_outstanding) or shares_outstanding <= 0:
            shares_outstanding = None
    except Exception:
        shares_outstanding = None

    if shares_outstanding is None:
        st.error("Could not retrieve shares outstanding from the API (quote -> sharesOutstanding).")
        return

    st.write(f"**Shares outstanding (from API):** {shares_outstanding:,.0f}")

    fair_value = result["intrinsic_value"] / float(shares_outstanding)
    st.metric("Fair value per share", f"{fair_value:,.2f}")

    st.markdown(f"""
    Now that we have the intrinsic value of the entire business, we can translate that into a **fair value per stock**.

    - If the company had **100 shares**, each share would represent **1/100** of the business.
    - So each share should be worth: **Intrinsic Value ÷ Shares Outstanding**

    In our case:

    **{result['intrinsic_value']:,.2f} ÷ {shares_outstanding:,.0f} = {fair_value:,.2f} per share**
    """)


    # --- Margin of safety (automatic, no user input)
    st.markdown("---")
    st.markdown("## 5) Margin of safety")

    market_price = None
    try:
        market_price = pd.to_numeric(quote_df.get("price"), errors="coerce").iloc[0]
        if pd.isna(market_price) or market_price <= 0:
            market_price = None
    except Exception:
        market_price = None

    if market_price is None:
        st.warning("Could not retrieve current market price from the API.")
        return

    st.write(f"**Current market price (from API):** ${market_price:,.2f}")

    margin_of_safety = (fair_value / market_price) - 1

    st.metric("Margin of safety", f"{margin_of_safety * 100:,.1f}%")

    # Explanation
    st.markdown("""
    ### What does this mean?

    The **margin of safety** compares what you think a business is worth
    to what the market is currently charging you.

    - A **positive margin of safety** means the stock is trading **below** your estimated fair value  
    - A **negative margin of safety** means the stock is trading **above** your estimated fair value  

    In practical terms:
    """)

    if margin_of_safety >= 0.30:
        st.success("""
    🟢 **Large margin of safety**

    The market price is far below your estimated intrinsic value.
    This gives you room for error if your assumptions turn out to be too optimistic.
    """)
    elif margin_of_safety >= 0.10:
        st.info("""
    🟡 **Moderate margin of safety**

    There is some discount, but not a huge one.
    Your assumptions need to be reasonably accurate for this investment to work.
    """)
    elif margin_of_safety >= 0:
        st.warning("""
    🟠 **Thin margin of safety**

    The stock is only slightly below your fair value estimate.
    There is little room for error.
    """)
    else:
        st.error("""
    🔴 **No margin of safety**

    The stock is trading above your estimated intrinsic value.
    Either the market is optimistic — or your assumptions are conservative.
    """)

