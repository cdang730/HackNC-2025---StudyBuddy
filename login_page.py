import streamlit as st

from userlogin import register_user, login


st.title("Study Buddy Planner - Login")

def main():
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

    # After successful login, offer a button to open the main app page.
    if st.session_state.get("logged_in_user"):
        st.markdown(f"**Logged in as:** {st.session_state['logged_in_user']}")
        # Render the main app directly in the same Streamlit session.
        try:
            import app as app_module
            if hasattr(app_module, "main"):
                app_module.main()
            else:
                st.info("App module imported — implement `main()` in app.py to render the app here.")
        except Exception as e:
            st.error(f"Could not open app: {e}")