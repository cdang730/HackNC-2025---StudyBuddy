import streamlit as st

if not st.user.is_logged_in:
    if st.button("Login with Google"):
        st.login()
    st.stop()


if st.button("Log out"):
    st.logout()
st.markdown(f"Welcome! {st.user.name}")