import streamlit as st
from course_pages import (
    introduction,
    chapter1,
    chapter2,
    chapter3,
    chapter4,
    investment_pro,
    chapter1_appendix
)

def main():
    st.sidebar.title("The Little Book")

    menu = [
        "Introduction",
        "Chapter 1- Understanding the Basics",
        "Chapter 1 Appendix – Earnings Yield Scanner",
        "Chapter 2- Indicators of a Good Business",
        "Chapter 3- Acquirer's Multiple",
        "Chapter 4- Financial Stability (FS-Score)"
    ]

    choice = st.sidebar.radio("Go to", menu)

    # Navigation handler
    if choice == "Introduction":
        introduction.app()

    elif choice == "Chapter 1- Understanding the Basics":
        chapter1.app()

    elif choice == "Chapter 1 Appendix – Earnings Yield Scanner":
        chapter1_appendix.app()

    elif choice == "Chapter 2- Indicators of a Good Business":
        chapter2.app()

    elif choice == "Chapter 3- Acquirer's Multiple":
        chapter3.app()

    elif choice == "Chapter 4- Financial Stability (FS-Score)":
        chapter4.app()

if __name__ == "__main__":
    main()
