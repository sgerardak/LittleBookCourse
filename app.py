import streamlit as st
from course_pages import introduction, chapter1, chapter2, investment_pro  # Import your pages

# Define a sidebar for navigation
def main():
    st.sidebar.title("The Little Book")
    menu = ["Introduction", "Chapter 1", "Chapter 2", "Investment Pro"]
    choice = st.sidebar.radio("Go to", menu)

    # Load the selected page
    if choice == "Introduction":
        introduction.app()
    elif choice == "Chapter 1":
        chapter1.app()
    elif choice == "Chapter 2":
        chapter2.app()
    elif choice == "Investment Pro":
        investment_pro.app()

if __name__ == "__main__":
    main()
