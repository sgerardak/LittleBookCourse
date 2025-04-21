import streamlit as st
from course_pages.chapter1_app import display_stock_analysis


def app():
    # Title and Introduction
    st.title("📘 Chapter 1: Understanding the Basics")
    st.write("By the end of this chapter, you’ll be able to answer these questions:")
    st.markdown("""
    - What is the **net income** of the company?
    - How many **shares** does the company have?
    - What are the **earnings per share (EPS)**?
    - What is the **earnings yield**?
    """)
    st.divider()  # Horizontal separator for clarity

    # Section 1: Johnny's Magical Lemon Empire
    st.header("🍋 Johnny and His Magical Lemons")
    st.write("""
    Your best friend Johnny is an unusual guy. Some might even say he’s a little… eccentric. But that’s part of his charm.
    Johnny runs a business selling magical lemons. Yes, you heard that right—**magical lemons**. These lemons are so good 
    that anyone who buys one swears they can run faster, think sharper, and even sing in perfect pitch (but only for a day).
    """)
    st.write("""
    Johnny buys each magical lemon for **\$0.50** and sells it for **\$1.00**. His stand is always buzzing with customers. 
    Why? Because Johnny is not only a great salesman, but he’s also got a flair for theatrics—he wears a magician’s hat 
    and calls himself “The Lemon Whisperer.”
    """)
    st.markdown("""
    - **Daily Revenue**: \$1 × 200 = **\$200**
    - **Daily Cost**: \$0.50 × 200 = **\$100**
    - **Daily Profit**: \$200 - \$100 = **\$100**
    """)
    st.write("""
    Johnny works his magic every day, and after a month, his profits look like this:
    """)
    st.markdown("""
    - **Monthly Profit (Net Income)**: \$100 × 30 days = **\$3,000**
    - **Annual Profit (Net Income)**: \$3,000 × 12 months = **\$36,000**
    """)
    st.divider()

    # Section 2: Johnny Offers You a Slice of the Magic
    st.header("💼 Johnny Offers You a Slice of the Magic")
    st.write("""
    One day, Johnny comes to you with his magician’s hat slightly tilted and says, 
    “Hey, best friend! I’ve got an offer you can’t refuse. I’m dividing my magical lemon business into 
    **100,000 shares**. Want in?”
    """)
    st.write("""
    Being intrigued, you ask how much a share costs. Johnny, with a dramatic wave of his hand, announces, 
    “Only **\$72** per share.”
    """)
    st.write("""
    Now, before going ahead, let’s ponder:
    """)
    st.markdown("""
    - **Is this a good deal?**
    - **Why would it be a good deal?**
    """)
    st.write("""
    It’s magical lemons—surely it should be a good deal, right? They’re magical, after all. 
    But wait… maybe we should do the math first.
    """)
    st.write("""
    Let's imagine that you buy **100 shares**. Since the company is divided into **100,000 shares**, 
    those 100 shares would make you the owner of **1%** of the magical lemon company—much the same way 
    as buying a share makes you a part-owner of a company in the stock market.
    """)
    st.markdown("""
    - **Your Total Investment**: 100 shares × \$72 = **\$7,200**
    """)
    st.write("""
    And since you now own **1%** of the company, that means **1% of the earnings are yours**!
    """)
    st.markdown("""
    - **Your Share of Annual Profit**: \$36,000 × 0.01 = **\$360**
    """)
    st.write("""
    Now, let’s calculate your **return on investment (ROI)**. ROI tells you what percentage of your investment 
    you’re getting back in profit. To calculate ROI, we use the formula:
    """)
    st.markdown("""
    **ROI = (Your Profit ÷ Your Investment) × 100**
    """)
    st.write("""
    In this case:
    """)
    st.markdown("""
    - **ROI = (360 ÷ 7,200) × 100 = 5%**
    """)
    st.write("""
    At this price, your return would be **5%**, which honestly isn’t very magical. You politely decline, 
    thinking you’d rather put your money in a **6% bond** or another investment. Johnny shrugs and says, 
    “Suit yourself. But remember, you’re turning down magic.”
    """)

    st.divider()

    # Section 3: The Crazy Market
    st.header("🤯 The Crazy Market")
    st.write("""
    Johnny’s offers change daily, much like the stock market. One day he offers shares at **\$100**, 
    then **\$60**, **\$50**, **\$40**, and finally **\$15**. You jump in at **\$15** and buy 100 shares.
    """)
    st.write("""
    Here’s the magical part: even though the price per share is lower, you’re still buying **100 shares**, 
    which means you still own **1% of the company**. And owning 1% entitles you to **1% of the company’s earnings**, 
    just like before.
    """)
    st.markdown("""
    - **Your Total Investment**: 100 shares × \$15 = **\$1,500**
    - **Your Share of Annual Profit**: \$36,000 × 0.01 = **\$360**
    """)
    st.write("""
    Now let’s calculate your **return on investment (ROI)** again to see how much better this deal is:
    """)
    st.markdown("""
    **ROI = (Your Profit ÷ Your Investment) × 100**
    """)
    st.write("""
    For this deal:
    """)
    st.markdown("""
    - **ROI = (\$360 ÷ \$1,500) × 100 = 24%**
    """)
    st.write("""
    This time, your ROI is **24%**, which is a fantastic return compared to the earlier offer of 5%. 
    Waiting for the right moment paid off!
    """)
    st.write("""
    Johnny’s pricing behavior reminds us of Benjamin Graham’s famous analogy: **“Mr. Market”**. Graham, 
    one of the greatest investors of all time, described the market as a wildly unpredictable, schizophrenic 
    business partner who offers to buy or sell shares at a different price every day. Your job? To take advantage of him when the price is right—just like you did with Johnny.
    """)
    st.divider()


    # Section 4: Key Market Terms
    st.header("📚 Key Market Terms")
    st.write("""
    Johnny’s example introduces terms commonly used in the market:
    """)
    st.markdown("""
    - **Net Income**: \$36,000
    - **Outstanding Shares**: 100,000
    - **Earnings Per Share (EPS)**: \$36,000 ÷ 100,000 = **\$3.6**
    - **Earnings Yield**: \$3.6 ÷ \$15 = **24%**
    """)
    st.divider()

    # Section 5: Getting it Real
    st.header("🔍 Getting it Real!")
    st.write("""
    Real businesses are more complex than Johnny’s. They have more costs, taxes, and expenses. Still, they publish key metrics:
    """)
    st.markdown("""
    - **Net Income**
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

    # Conclusion Section
    st.header("🎉 Wrapping Up Chapter 1")
    st.write("""
    Well, I hope you’re having fun with the market right now and that you’re starting to grasp some of the key ideas 
    behind identifying good opportunities. We’ve explored how owning part of a company works, how share prices can affect 
    your return on investment, and how the market can behave like a quirky, unpredictable character.

    However, since this is **real money** we’re talking about, I’m sure you want confidence in knowing that the business 
    you’re putting your money into is actually a **good business**. You’d probably want one with steady, reliable income not 
    just a one-year miracle or at the very least, a business that isn’t handled by a *schizophrenic dude* like Johnny.

    Luckily, this is just the **first chapter**! In the next chapters, we’re going to dive deeper into answering these 
    important questions and learning how to spot truly good businesses.
    """)

