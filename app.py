import streamlit as st

st.title("Hello, Streamlit!")
st.write("this is my first Streamlit app in VS code")

name = st.text_input("Enter your name: ")
if name:
    st.success(f"hello, {name}!")