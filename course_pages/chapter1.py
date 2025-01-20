import streamlit as st

def app():
    import streamlit as st

    st.title("Chapter 1: Understanding the Basics")

    st.write("""
    By the end of this chapter, you’ll be able to answer these questions and see why they’re important for understanding a business:

    What is the net income of the company?

    How many shares does the company have?

    What are the earnings per share (EPS)?

    What is the earnings yield?

    Answering these questions is a great starting point, and we’ll build from there. Let’s dive into an example to make things simple and fun.
    """)

    st.header("Johnny's Lemon Business")

    st.write("""
    Imagine your best friend Johnny runs a business selling lemons. Johnny buys each lemon for 50 cents and sells it for $1. He’s great at selling lemons and manages to sell 200 lemons every single day.

    Here’s how the numbers add up:

    Daily Revenue: $1 per lemon × 200 lemons = $200

    Daily Cost: $0.50 per lemon × 200 lemons = $100

    Daily Profit: $200 – $100 = $100

    Now let’s see how much Johnny makes in a month. Assuming he keeps up this pace for 30 days:

    Monthly Profit (Net Income): $100 per day × 30 days = $3,000

    Annual Profit (Net Income): $3,000 × 12 = $36,000

    So, Johnny’s business earns him $3,000 every month after covering all the costs of buying lemons. Not bad, right?
    """)

    st.header("Johnny Offers You a Deal")

    st.write("""
    Well, now the interesting part comes. Johnny (since he’s your best friend) wants to sell you part of his profitable business. To do this, he divides his business into 100,000 shares and offers to sell you as many shares as you want.

    What would be a good price? Let’s imagine Johnny sets the price at $72 per share. That means buying 100 shares would cost you:

    Total Investment: $72 × 100 shares = $7,200

    What does this mean? Since you now own 1% of the business (100 shares out of 100,000), then 1% profit is yours too. At the end of the year, you’d receive:

    Your Share of Annual Profit: $36,000 × 0.01 = $360

    Is this a good deal? Well as you can see you're getting only 5% of return for your investment at the end of the year ($360/$7,200). Well, in this case wouldn't it be better to get a 6% bond (or even higher these days) and just have your money secured? Well in this case the answer is yes.
    """)

    st.header("The Crazy Market")

    st.write("""
    Well, Johnny's deal doesn’t seem great right now, so you decide to pass. The good news is, you know Johnny, and frankly, he’s a little crazy—he offers different deals every day (very much like the market). One day, Johnny offers a share for $100. Another day, it’s $60, then $50, $40, $30. Hmm… now it’s starting to get interesting. Finally, one day Johnny offers a share for $15 each. That’s when you decide to jump in.

    Let’s examine the deal you took. Suppose you bought 100 shares:

    Total Investment: $15 × 100 shares = $1,500

    Your Share of Annual Profit (This doesn’t change since you still own 1%): $36,000 × 0.01 = $360

    Now you’re getting $360 at the end of the year for the $1,500 you spent. That’s a 24% return! Suddenly, Johnny seems like a great friend.

    As you may have guessed, Johnny’s behavior and the market have a lot in common. The market, just like Johnny, is full of opportunities if you wait for the right moment!
    """)

    st.header("Key Market Terms")

    st.write("""
    With Johnny's example, we learned some terms that are very commonly used in the market:

    Net Income: $36,000

    Outstanding Shares: 100,000

    Earnings Per Share (EPS): Net Income / Outstanding Shares = $36,000 / 100,000 = $3.6

    Earnings Yield: EPS / Share Price = $3.6 / $15 = 24%
    """)

    st.header("Getting it Real!")

    st.write("""
    This is all really nice and pretty, but real businesses are not as simple as Johnny’s business. They have more costs, more expenses, taxes, and so on. This is true, and you can find all the details in the income statement of each company. But at the end of the day, every business will have a part where they tell you:

    The Net Adjusted Income

    The Outstanding Shares

    The Earnings Per Share (EPS)

    The Earnings Yield

    The Stock Price

    And if it feels like too much of a hassle to dig through income statements, here’s some good news: there’s a tool you can use to explore your favorite companies. Start looking at these metrics and find out which companies could be attractive for you!
    """)

