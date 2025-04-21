import streamlit as st
from course_pages.chapter3_app import display_acquirers_multiple

def app():
    # Title and Introduction
    st.title("Chapter 3: The Acquirer's Multiple – A Deep Value Lens")

    st.markdown("""
    Now that we’ve laid a foundation of understanding — what it means to own a share, and what makes a great business — it’s time to explore another powerful investing concept, one that zooms in on how to buy businesses at a bargain. This concept, popularized by Tobias Carlisle, is known as the **Acquirer's Multiple**.

    ### Understanding Enterprise Value

    Before diving into the multiple itself, we need to understand **Enterprise Value (EV)**. While most investors focus on **Market Capitalization** — the stock price multiplied by the number of shares — EV gives a more complete picture of what it would actually cost to buy the entire company.

    **Enterprise Value = Market Capitalization + Total Debt - Cash and Cash Equivalents**

    Why is this important? Because when you acquire a business, you don’t just buy its equity — you also take on its debt and gain access to its cash. EV accounts for everything:

    - **Debt:** If a company has a lot of debt, it’s a burden that the buyer must handle.
    - **Cash:** On the other hand, a cash-rich company can help offset its purchase cost.

    By focusing on EV, we’re thinking like a true buyer — whether a private equity firm or a corporate acquirer — and not just a stock market trader.

    ### Understanding Operating Earnings

    Next, let’s look at the company’s ability to generate profits through its core operations. For this, we use **Operating Earnings**, also known as **EBIT (Earnings Before Interest and Taxes)**.

    EBIT tells us how profitable the company is before financial and tax decisions come into play. It's a clean view of business performance — free from the effects of capital structure (debt vs. equity) and tax strategy.

    This metric is useful because it:

    - Focuses strictly on **core business performance**, ignoring interest and taxes that may vary significantly across companies or jurisdictions.
    - Is **less susceptible to accounting manipulation** than net income.
    - Provides a **standardized way to compare companies** across industries.

    Warren Buffett has often emphasized that the value of a business is based on its ability to produce cash flows into the future. EBIT gives us a consistent, apples-to-apples way to estimate a company’s core profit engine — what really drives its long-term value.

    ### Putting It Together: The Acquirer's Multiple

    Now that we understand both components, the Acquirer's Multiple is simply:

    **Acquirer's Multiple = Enterprise Value / Operating Earnings (EBIT)**

    This ratio tells us how much we’re paying for each dollar of operating earnings. A **lower multiple** suggests the company is **cheaper** relative to its ability to generate profit.

    Carlisle's insight was to use this multiple as a pure value measure — ignoring quality metrics for a moment and simply asking, *"How cheap is this business if I had to buy the whole thing?"*

    This approach favors unloved, overlooked, or misunderstood companies — the kinds that value investors have long believed can outperform over time.

    ### Example: Calculating the Acquirer's Multiple

    Let’s look at a simple example:

    Imagine we are evaluating Company ABC:

    - Market Capitalization: $500 million
    - Total Debt: $200 million
    - Cash and Cash Equivalents: $50 million
    - EBIT (Operating Earnings): $100 million

    **Step 1: Calculate Enterprise Value**

    EV = \$500M (Market Cap) + \$200M (Debt) - \$50M (Cash) = **\$650M**

    **Step 2: Divide by Operating Earnings**

    Acquirer's Multiple = \$650M / \$100M = **6.5**

    This tells us we’re paying 6.5 times the company’s operating earnings to buy the whole business. 


    """)

    # Important Note
    st.info("**Note:** The Acquirer's Multiple is especially useful when comparing companies within the **same industry**. Since different sectors have different capital structures and profit patterns, this ratio is most powerful when used to evaluate competitors side by side.")


    st.divider()
    st.header("🔍 Try It Yourself: Compare Two Companies")
    display_acquirers_multiple()
    st.divider()

    st.header("Next Steps")
    st.write("You now have a new lens to view businesses — one favored by corporate acquirers and deep value investors. This tool helps you assess a company’s value in a new way, especially when comparing businesses within the same industry.")
    st.markdown("""
    - **Find Real Opportunities**: Start discovering attractive businesses using the Acquirer’s Multiple.
    """)
