import streamlit as st
import pandas as pd
from course_pages.chapter5_app import display_intrinsic_value_analysis


def app():
    # Title and inspiration
    st.title("📘 Chapter 5: Valuation & Intrinsic Value")

    st.caption("""
    Inspired by *The Five Rules for Successful Stock Investing* by Pat Dorsey.
    This chapter adapts the Morningstar-style intrinsic value framework for educational purposes.
    """)

    st.markdown("""
    So far in this course, we’ve been asking **really good questions**:

    - Is this company profitable?
    - Is it financially stable?
    - Does it look cheap compared to others?

    Those questions already put you ahead of most investors.

    But there’s still one **big question** we haven’t fully answered yet 👇
    """)

    st.subheader("💡 What is this business actually worth?")

    st.markdown("""
    Financial ratios are incredibly useful — they help us understand **how** a company is doing.

    But ratios have a limitation:
    **they don’t tell us what a company is worth in absolute terms.**

    When we buy individual stocks, we want something more concrete than relative comparisons.
    We want a reference point that allows us to judge whether a stock is truly attractive.

    That’s where **intrinsic value** comes in.
    """)

    st.markdown("""
    Valuation gives us:
    - 🎯 A target value  
    - 🧭 A clear decision anchor  
    - 🛡️ A buffer against being wrong  

    It doesn’t eliminate uncertainty — but it helps us manage it.
    """)

    st.header("1️⃣ The Core Idea: Discounted Cash Flow (DCF)")

    st.markdown("""
    Most serious valuation methods are built on one simple idea:

    > A business is worth the cash it will generate **in the future**.

    This is known as **Discounted Cash Flow (DCF)**.

    But future money is not the same as money today.
    """)

    st.subheader("Why do we discount future cash flows?")
    st.markdown("""
    There are two reasons:

    1️⃣ **Time** — You’d rather receive money now than later  
    2️⃣ **Risk** — Future cash flows are uncertain, especially for businesses  

    Even when something feels “safe,” waiting still has a cost.
    """)

    st.markdown("""
    Quick thought experiment 🧠

    - Option A: Get \$100 today  
    - Option B: Get \$1,000 in one year (100% guaranteed)

    Easy choice.

    Now try this:

    - Option A: Get \$100 today  
    - Option B: Get \$101 in one year

    Suddenly, waiting doesn’t feel worth it anymore.

    That difference is **discounting** in real life.
    """)

    st.header("2️⃣ How Discounting Works (No Scary Math)")

    st.markdown(r"""
    The math behind discounting looks intimidating, but the logic is simple.

    **Present Value = Future Cash Flow ÷ (1 + Discount Rate)ⁿ**

    Where:
    - **Discount rate** is the return you demand
    - **n** is how many years you have to wait
    """)

    st.markdown("""
    The most important takeaway isn’t the formula — it’s the intuition:

    👉 **The further away a cash flow is, the less it’s worth today.**

    That’s why:
    - Near-term cash flows are extremely valuable
    - Distant promises matter much less
    """)

    st.header("3️⃣ Cash Flows Beyond Year 10: Perpetuity")

    st.markdown("""
    Here’s a practical limitation we have to accept:

    ❌ We can’t realistically forecast cash flows forever.

    Instead, valuation models usually work in two stages:
    - Forecast cash flows explicitly for a finite period (commonly **10 years**)
    - Estimate the value of all cash flows beyond that point using a **terminal value**
    """)

    st.markdown(r"""
    The most common terminal value approach is the **perpetuity formula**:

    **Terminal Value = (Final Year Cash Flow × (1 + g)) ÷ (r − g)**

    This represents the value of *all future cash flows after year 10*, expressed as a value
    at the end of the forecast period.
    """)

    st.markdown("""
    A few important rules:
    - The long-term growth rate (**g**) must be **lower** than the discount rate (**r**)
    - Terminal value often represents a large portion of intrinsic value
    - Small changes here can have a big impact → stay conservative
    """)

    st.header("4️⃣ Choosing a Discount Rate (Reality > Precision)")

    st.markdown("""
    Choosing the “correct” discount rate is one of the hardest parts of valuation.

    Rather than chasing false precision, we focus on **directional logic**.

    Your discount rate should generally increase when:
    - Interest rates increase
    - Business risk increases
    """)

    st.markdown("""
    Why interest rates?

    Because if you can earn an attractive return from a **low-risk bond**, a risky stock
    needs to offer a meaningfully higher expected return to be worth owning.
    """)

    st.header("5️⃣ Risk: Think Business, Not Stock Price")

    st.markdown("""
    Many finance textbooks define risk as **stock price volatility**.

    For long-term investors, a more useful definition is:
    > *How confident are we that the business will actually deliver the cash flows we’re modeling?*
    """)

    st.subheader("What increases business risk?")
    st.markdown("""
    - **Company size:**  
      Smaller companies tend to be more volatile. They usually have fewer resources,
      less diversification, and are more vulnerable to competition or economic shocks.

    - **Economic moat:**  
      Companies without a strong moat face constant competitive pressure,
      which makes future profits less predictable.

    - **Management quality:**  
      Poor capital allocation, excessive risk-taking, or weak governance
      can destroy value even in a good business.

    - **Cyclicality:**  
      Businesses tied to economic or seasonal cycles experience unstable cash flows,
      which increases uncertainty.

    - **Debt levels:**  
      Higher debt means fixed obligations. During downturns, interest payments
      can quickly become a serious problem.

    - **Business complexity:**  
      If a business is hard to understand, it’s harder to model reliably —
      and uncertainty increases risk.
    """)

    st.subheader("A simple, consistent risk framework")
    st.markdown("""
    Instead of pretending we can calculate risk precisely, we group companies into buckets:

    | Risk Level | Discount Rate |
    |---|---:|
    | Low-risk | 9% |
    | Mid-risk | 12% |
    | High-risk | 15% |

    This approach isn’t perfect — but it’s disciplined, conservative, and repeatable.
    """)

    # ------------------------------------------------------------
    # HARD-CODED JOHNNY EXAMPLE (illustrative, step-by-step)
    # ------------------------------------------------------------
    st.header("6️⃣ Worked Example: Johnny’s Lemon Stand 🍋 (Hard-coded)")

    st.markdown("""
    Let’s put everything together with **easy numbers**, step by step.

    We’ll assume Johnny’s Lemon Stand is **mid-risk** (cyclical demand), so we use **12%** as the discount rate.
    """)

    # Easy assumptions
    r = 0.12               # discount rate (mid-risk)
    g_terminal = 0.03      # terminal growth

    st.markdown("""
    ### ✅ Assumptions
    - Discount rate (mid-risk): **12%**
    - Terminal growth (**g**): **3%**
    - Forecast horizon: **10 years**
    """)

    st.markdown("---")
    st.subheader("Step 1 — Assume we forecasted the next 10 years of cash flows")

    st.markdown("""
    In real life, forecasting is its own skill — it involves understanding the business, its moat,
    competition, margins, reinvestment needs, and so on.

    For this example, let’s keep it simple:

    👉 **Assume we did our homework** and we believe Johnny’s free cash flow for the next 10 years
    will look like this:
    """)

    # Easy, hand-picked cash flows (gently increasing, easy to follow)
    forecast_fcfs = [100, 105, 110, 115, 120, 125, 130, 135, 140, 145]

    rows = []
    pv_10y = 0.0
    for year, fcf in enumerate(forecast_fcfs, start=1):
        discount_factor = 1 / ((1 + r) ** year)
        pv = fcf * discount_factor
        pv_10y += pv
        rows.append({
            "Year": year,
            "Forecast FCF": fcf,
            "Discount Factor (12%)": round(discount_factor, 4),
            "Present Value": round(pv, 2),
        })

    df_forecast = pd.DataFrame(rows)

    st.dataframe(df_forecast, use_container_width=True)
    st.success(f"✅ Present Value of Years 1–10 cash flows = **{pv_10y:,.2f}**")

    st.markdown("---")
    st.subheader("Step 2 — Calculate terminal value (perpetuity) at year 10")

    fcf_10 = forecast_fcfs[-1]

    st.markdown(r"""
    After year 10, we stop forecasting year-by-year and use the perpetuity formula:

    **Terminal Value (at Year 10) = (FCF₁₀ × (1 + g)) ÷ (r − g)**
    """)

    terminal_value = (fcf_10 * (1 + g_terminal)) / (r - g_terminal)

    st.markdown(f"""
    Plugging in the numbers:
    - FCF₁₀ = **{fcf_10}**
    - g = **3%**
    - r = **12%**

    **TV = ({fcf_10} × 1.03) ÷ (0.12 − 0.03) = {terminal_value:,.2f}**
    """)

    st.markdown("---")
    st.subheader("Step 3 — Discount the terminal value back to today")

    st.markdown(r"""
    The terminal value is a value **at the end of year 10**, so we discount it:

    **PV(TV) = TV ÷ (1 + r)¹⁰**
    """)

    pv_terminal = terminal_value / ((1 + r) ** 10)

    st.markdown(f"""
    **PV(TV) = {terminal_value:,.2f} ÷ (1.12¹⁰) = {pv_terminal:,.2f}**
    """)

    st.success(f"✅ Present Value of Terminal Value = **{pv_terminal:,.2f}**")

    st.markdown("---")
    st.subheader("Step 4 — Add everything to estimate intrinsic value")

    intrinsic_value = pv_10y + pv_terminal

    st.markdown(f"""
    **Intrinsic Value = PV(Years 1–10) + PV(Terminal Value)**

    **Intrinsic Value = {pv_10y:,.2f} + {pv_terminal:,.2f} = {intrinsic_value:,.2f}**
    """)

    st.markdown("---")
    st.subheader("Step 5 — From intrinsic value to fair value per stock")

    st.markdown("""
    Now that we have an estimate of the **intrinsic value of the entire business**, we can translate
    that into a **fair value per stock**.

    The logic is simple:

    - Intrinsic value tells us what the **whole business** is worth
    - To get the value of **one stock**, we divide by the number of shares
    """)

    # Easy illustrative assumption
    shares_outstanding = 100

    fair_value_per_share = intrinsic_value / shares_outstanding

    st.markdown(f"""
    ### 📊 Fair Value Calculation (Illustrative)

    - Estimated intrinsic value of the business: **{intrinsic_value:,.2f}**
    - Number of shares outstanding: **{shares_outstanding}**

    **Fair value per stock = {intrinsic_value:,.2f} ÷ {shares_outstanding} = {fair_value_per_share:,.2f}**
    """)

    st.info("""
    This is how intrinsic value becomes actionable.

    Once you know the fair value per stock, you can compare it to the market price:
    - If the stock trades well **below** this value → potential margin of safety
    - If it trades **around** this value → fairly priced
    - If it trades well **above** this value → higher risk of overpaying

    In real companies, the only difference is scale — instead of 100 shares,
    you’ll use the actual number of shares outstanding.
    """)


    # ------------------------------------------------------------
    # OPTIONAL: keep your interactive / real-stock section
    # ------------------------------------------------------------
    st.markdown("---")
    st.header("7️⃣ Now try it on a real stock (interactive)")

    st.subheader("Example")
    display_intrinsic_value_analysis()

    st.subheader("🧠 Final Takeaways")
    st.markdown("""
    - Valuation gives you a concrete reference point
    - DCF forces you to think about **cash, time, and risk**
    - Business risk matters more than stock price volatility
    - Terminal value plays a major role — conservative assumptions matter
    - Intrinsic value isn’t exact, but it’s an extremely powerful decision tool

    If you can value Johnny’s Lemon Stand,
    you can value real companies using the exact same logic.
    """)