import streamlit as st

st.title("Welcome Kit Order Form")

name = st.text_input("Enter your name")

if st.button("Submit Order"):
    st.write(f"Order submitted for {name}")