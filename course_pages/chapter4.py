import streamlit as st
from course_pages.chapter4_app import display_stock_analysis

def app():
    # Title and Intro
    st.title("📘 Chapter 4: How Financially Stable Is Your Stock? Meet the FS_Score")

    st.markdown("""
    🔍 When analyzing a company, there are many aspects investors tend to value:
    - Is the company selling at a good price?
    - Is it innovative?
    - Is it a leader in its sector?

    All of those matter. But to me — and to any long-term, value-oriented investor — one question always goes around:""")
    
    
    st.subheader("💡 Is this company financially stable?")

    st.markdown("""
    📚 In previous chapters, we explored how to compare companies, evaluate if a stock is fairly priced, and assess the quality of its business model and products. In this chapter, we shift our focus to something equally important: **financial stability**.

    🧱 Financial stability means the company has solid accounting, a resilient structure, and the ability to weather economic shocks. It’s not skating on the edge of bankruptcy, and it isn’t propped up by hope and hype. In other words, it gives us the peace of mind that it won’t disappear overnight and take our money with it.

    🧠 As Warren Buffett once said: _"You only find out who is swimming naked when the tide goes out."_ Financial strength is what keeps your portfolio from being exposed when the market turns.

    ✅ To measure this kind of financial strength, Joseph Piotroski introduced the **F-Score** — a set of nine accounting-based checks designed to spot robust companies and avoid the duds. Later, in the book *Quantitative Value*, Wesley Gray and Tobias Carlisle expanded on this framework and developed an improved, ten-variable version called the **FS_Score**. It’s a systematic, battle-tested way to assess whether a company’s fundamentals are solid.
        """)

    st.header("Let’s break it down, category by category")

    st.subheader("Current Profitability")
    st.markdown("""
    1. **Return on Assets (ROA > 0)**  
    ROA = Net Income / Total Assets  
    A positive ROA means the company is generating profit from its assets.

    2. **Free Cash Flow to Total Assets (FCFTA > 0)**  
    FCFTA = CFO / Total Assets  
    This indicates the company is generating strong cash returns.

    3. **Accruals (CFO / Net Income > 1)**  
    Low accruals = high earnings quality. More cash, fewer gimmicks.
    """)

    st.subheader("Stability")
    st.markdown("""
    4. **Change in Leverage (Δ Leverage < 0)**  
    A drop in leverage shows the company is reducing financial risk.

    5. **Change in Liquidity (Δ Current Ratio > 0)**  
    An improving current ratio means the company is in better shape to meet obligations.

    6. **Net Equity Issuance (NEQISS)**  
    Avoid dilution. If a company isn’t issuing new shares — or better, is buying back — that’s a good sign.
    """)

    st.subheader("Recent Operational Improvements")
    st.markdown("""
    7. **Change in ROA (Δ ROA > 0)**  
    Profitability is heading in the right direction.

    8. **Change in FCFTA (Δ FCFTA > 0)**  
    More cash relative to assets = strong performance.

    9. **Change in Gross Margin (Δ Margin > 0)**  
    Improving margins show pricing power or cost efficiency.

    10. **Change in Asset Turnover (Δ Turnover > 0)**  
    The company is becoming more efficient in using assets to generate revenue.
    """)

    st.subheader("Final Score")
    st.markdown("""
    You get 1 point for each metric a company passes:

    - 8–10 points? 🚀 Financial rockstar.
    - 5–7 points? 🤔 Decent, worth a deeper dive.
    - Below 5? 🚩 High risk. Proceed with caution.
    """)

    st.subheader("Example")
    display_stock_analysis()

    st.subheader("Wrap-Up: Key Takeaways 🧠")
    st.markdown("""
    The FS_Score is a fast, effective way to assess a company’s financial strength using real, hard metrics — not vibes. It screens for profitability, filters out balance-sheet disasters, and rewards operational momentum.

    But don’t forget: **financial stability is just one of many variables** to consider when deciding whether to buy a company. Other factors like price and business quality are crucial for value investors. And if you're a technical investor, momentum, trends, or news may also matter.
    """)
