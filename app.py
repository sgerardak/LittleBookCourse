import streamlit as st
from course_pages import chapter3, introduction, chapter1, chapter2,investment_pro  # Import your pages

# Define a sidebar for navigation
def main():
    st.sidebar.title("The Little Book")
    menu = ["Introduction", "Chapter 1- Understanding the Basics", "Chapter 2- Indicators of a Good Business","Chapter 3- Acquirer's Multiple"]
    choice = st.sidebar.radio("Go to", menu)

    # Load the selected page
    if choice == "Introduction":
        introduction.app()
    elif choice == menu[1]:
        chapter1.app()
    elif choice == menu[2]:
        chapter2.app()
    elif choice == menu[3]:
        chapter3.app()
    ###elif choice == "Investment Pro":
    ###    investment_pro.app()'''

if __name__ == "__main__":
    main()
