import streamlit as st
from course_pages.chapter1_app import display_stock_analysis

def app():
    # Title and Introduction
    st.title("Chapter 2: Indicators of a Good Business")
    st.write("By the end of this chapter, you'll be able to answer these questions:")
    st.write("- **What is an indicator of a good business?**")
    st.write("- **What is return on capital?**")
    st.write("- **How to put it all together.**")

    # Section 1: Digging Deeper into Johnny's Lemon Empire
    st.header("Digging Deeper into Johnny's Lemon Empire")
    st.write(
        "As you already know, Johnny is a tremendous businessman, and luckily for him, "
        "his business is still thriving. Johnny’s success has allowed him to expand his empire by "
        "opening new lemon stores across the country. Now, Johnny owns over 10 stores. 🍋"
    )
    st.write("**The Numbers Behind Johnny’s Success:**")
    st.write("- On average, Johnny spends **\$100,000** to open a new lemon store.")
    st.write("- Each store generates **\$15,000 yearly in profit.** 💸")

    # Section 2: Introducing Diego's Padelmania
    st.header("Introducing Diego's Padelmania")
    st.write(
        "Diego is also a businessman (it seems that entrepreneurial spirit runs in the family!). "
        "However, Diego’s business is very different from Johnny’s. Diego is capitalizing on a "
        "rapidly growing sport called **padel** by building courts and renting them out to customers. 🎾"
    )
    st.write("**The Numbers Behind Diego’s Venture:**")
    st.write("- Each padel court costs Diego **\$160,000** to build.")
    st.write("- On average, each court generates **\$40,000 yearly in profit.** 🌟")

    # Section 3: Comparing Johnny's Empire vs. Diego's Courts
    st.header("Comparing Johnny’s Empire vs. Diego’s Courts")
    st.write(
        "Good news! You’re also a businessman. Johnny's business is generating \$15,000 "
        "profit per store per year while Diego's court generates \$40,000. But it's way cheaper "
        "to open a lemon store. 🤔"
    )
    st.write(
        "What if we compare **2 lemon stores** with **1 of Diego's courts**? Or analyze what "
        "happens if profits drop by 30%? Let’s break it down! ✌️"
    )

    # Subsection: Johnny's 2 Stores vs Diego's Court
    st.subheader("Johnny's 2 Stores vs Diego's Court")
    st.write("**Diego’s Court:**")
    st.write("  - Total investment: \$160,000")
    st.write("  - Total yearly profit: \$40,000")
    st.write("**Johnny’s 2 Stores:**")
    st.write("  - Total investment: \$200,000")
    st.write("  - Total yearly profit:\$30,000")
    st.success("✅ With less investment, Diego's court is generating more profit!")

    # Subsection: Both businesses experience a 30% drop in profits
    st.subheader("What Happens if Profits Drop by 30%?")
    st.write("**Johnny’s Lemon Empire:**")
    st.write("  - New profit per store: $10,500")
    st.write("  - Return on capital per store: 10.5% 🤔")
    st.write("**Diego’s Padelmania:**")
    st.write("  - New profit per court: $28,000")
    st.write("  - Return on capital per court: 17.5%")

    st.write(
        "### What Does This Mean? 🌟\n"
        "1. Diego's business generates more money with less investment. His product is rarer and more valued.\n"
        "2. Johnny's business is less resilient when profits decline, but Diego's business remains profitable.\n"
    )

    # Section 4: Return on Capital (ROC)
    st.header("Return on Capital (ROC): A Key Indicator")
    st.write(
        "**What is return on capital?**\n"
        "Return on capital (ROC) measures how effectively a business uses its money to generate profits. "
        "It’s calculated as:\n"
    )
    st.latex(r"Return\ on\ Capital = \frac{Profit}{Debt+Equity} \times 100")

    # Section 5: Which Business Would You Invest In?
    st.header("Which Business Would You Invest In?")
    st.markdown(
        """
        - **A.** A business that has higher earnings yield (from Chapter 1).  
        - **B.** A business with a high return on capital.  
        - **C.** Both A and B.  
        """
    )
    st.success("Guessed it? Yes, the answer is **C**.")

     # Section 5: Getting it Real
    st.header("🔍 Getting it Real!")
    st.write("""
    It's fun to play with imaginary businnes like Johnny's Lemon Empire and Diego's Padelmania but isn't more fun to look at real business let's get down to it!
    Explored metrics:
    """)
    st.markdown("""
    - **Return on capital**
    - **Outstanding Shares**
    - **EPS (Earnings Per Share)**
    - **Earnings Yield**
    - **Stock Price**
    """)
    st.write("""
    If digging through financial reports feels overwhelming, don’t worry. Use the stock analysis tool below to explore your favorite companies and find the magic in the market.
    """)
    st.divider()

    # Stock Analysis Tool
    display_stock_analysis()
    st.divider()


    # Recap Section
    st.header("Recap: What You’ve Learned 🔄")
    st.write("- **Good businesses generate high returns on capital (ROC).**")
    st.write("- Johnny’s Lemon Empire has a slightly lower ROC compared to Diego’s Padelmania.")
    st.write("- Diego’s Padelmania scales better and is more resilient in declining markets.")
    st.write("- Balancing profitability, scalability, and risk is key to making smart investment decisions. 📚")
