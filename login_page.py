import streamlit as st
from userlogin import register_user, login


def main():
    """Render the login/sign-up UI. Call this from app.py when the user requests password login."""
    st.title("Study Buddy Planner - Login")

    # Simple, linear layout works best for small forms. Use columns for buttons.
    username = st.text_input("Enter your username:")
    password = st.text_input("Enter your password:", type="password")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login"):
            if login(username.strip(), password.strip()):
                st.success("Login successful!")
                st.session_state["logged_in_user"] = username.strip()
            else:
                st.error("Invalid username or password. Please try again.")

    with col2:
        if st.button("Sign up"):
            register_user(username.strip(), password.strip())
            st.success("Registered. You can now log in.")

    # After successful login, display a confirmation and return to caller (app.py can decide what to show next)
    if st.session_state.get("logged_in_user"):
        st.markdown(f"**Logged in as:** {st.session_state['logged_in_user']}")
