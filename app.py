import streamlit as st
from backend import save_user, find_match
from pathlib import Path
from userlogin import register_user, login

# Load and apply custom CSS from the same directory as this file.
st.markdown('<style>' + open('style.css').read() + '</style>', unsafe_allow_html=True)

if not st.user.is_logged_in:
    if st.button("Login with Google"):
        st.login()
    elif st.button("Login with Password"):
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
    st.stop()

if st.button("Log out"):
    st.logout()
st.markdown(f"Welcome! {st.user.name}")

st.title("Studdy Buddy Planner")
col1, col2 = st.columns(2)
with col1: subject = st.selectbox("Subject: ", ["Math", "English", "History", "Science", "CS"])
with col2: mode = st.radio("Mode: ", ["Virtual", "In-Person"])

if st.button("Log out"):
    st.logout()
st.markdown(f"Welcome! {st.user.name}")

st.title("Studdy Buddy Planner")
col1, col2 = st.columns(2)
with col1: subject = st.selectbox("Subject: ", ["Math", "English", "History", "Science", "CS"])
with col2: mode = st.radio("Mode: ", ["Virtual", "In-Person"])

col3, col4, col5 = st.columns(3)
with col3: time = st.selectbox("Study Time: ", ["Morning", "Afternoon", "Evening"])
with col4: name = st.text_input("Enter your name: ")
with col5: privacy = st.selectbox("Do you want others to find you? ", ["Yes", "No"])

contact = st.text_input("Contact information: ")

col3, col4, col5 = st.columns(3)
with col3: time = st.selectbox("Study Time: ", ["Morning", "Afternoon", "Evening"])
with col4: name = st.text_input("Enter your name: ")
with col5: privacy = st.selectbox("Do you want others to find you? ", ["Yes", "No"])

contact = st.text_input("Contact information: ")


button = st.button("Find Match")
if button:
    if privacy == "Yes":
        new_user = {"name": name, "subject": subject, "time": time, "mode": mode, "contact": contact}
        save_user(new_user)
    matches = find_match(subject, mode, time, name, contact)
    if matches:
        st.write("You have matches!")
        for m in matches:
            st.write(m["name"], "wants to study", m["subject"], "in the ", m["time"].lower(), "(", m["mode"], "), Contact: ", m["contact"])
    elif not matches:
        st.write("Sorry, no matches yet. Come back later!")
button = st.button("Find Match")
if button:
    if privacy == "Yes":
        new_user = {"name": name, "subject": subject, "time": time, "mode": mode, "contact": contact}
        save_user(new_user)
    matches = find_match(subject, mode, time, name, contact)
    if matches:
        st.write("You have matches!")
        for m in matches:
            st.write(m["name"], "wants to study", m["subject"], "in the ", m["time"].lower(), "(", m["mode"], "), Contact: ", m["contact"])
    elif not matches:
        st.write("Sorry, no matches yet. Come back later!")


