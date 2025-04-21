import streamlit as st
from course_pages.chapterEXP_app import display_stock_analysis

def app():
    st.title("Welcome to the Course!")
    st.write("This is the introduction to the interactive course based on *The Little Book That Still Beats the Market*.")
    display_stock_analysis()
