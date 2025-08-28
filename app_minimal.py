# app_minimal.py
import streamlit as st

st.title("Simple Phishing Detector")
st.write("This is a basic working app. We'll add functionality step by step.")

url = st.text_input("Enter a URL to analyze")

if url:
    st.write(f"You entered: {url}")
    st.write("This is where the analysis would happen.")