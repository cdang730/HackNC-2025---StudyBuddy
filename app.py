import streamlit as st
from backend import save_user, find_match
from pathlib import Path

# Load and apply custom CSS if present
css_path = Path(__file__).with_name('style.css')
if css_path.exists():
    st.markdown('<style>' + css_path.read_text(encoding='utf-8') + '</style>', unsafe_allow_html=True)

# Simple session-based navigation keys
st.session_state.setdefault("view", "home")  # views: home, login, delete, app

# Navigation bar at top
col_left, col_right = st.columns([3, 1])
with col_left:
    st.title("Study Buddy Planner")
with col_right:
    if st.session_state.get("logged_in_user"):
        if st.button("Logout"):
            st.session_state.pop("logged_in_user", None)
            st.experimental_rerun()
    else:
        if st.button("Login"):
            st.session_state["view"] = "login"
            st.experimental_rerun()


# If user selected login view, show the login page
if st.session_state.get("view") == "login":
    import login_page
    login_page.main()
    # If login was successful, switch to 'app' view
    if st.session_state.get("logged_in_user"):
        st.session_state["view"] = "app"
        st.experimental_rerun()

    # offer a back button
    if st.button("Back to home"):
        st.session_state["view"] = "home"
        st.experimental_rerun()

# If user selected delete view, show the delete page
elif st.session_state.get("view") == "delete":
    import delete_info_page
    delete_info_page.main()
    if st.button("Back to home"):
        st.session_state["view"] = "home"
        st.experimental_rerun()

else:
    # Home / main app view
    if not st.session_state.get("logged_in_user"):
        st.markdown("### Welcome — please login to continue")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Login with Google"):
                st.info("Google login not implemented yet — use Password login.")
        with c2:
            if st.button("Login with Password"):
                st.session_state["view"] = "login"
                st.experimental_rerun()

        # allow access to delete page (for users who want to manage saved entries)
        if st.button("Manage my saved entries (Delete)"):
            st.session_state["view"] = "delete"
            st.experimental_rerun()

        st.stop()

    # Logged-in user sees the app UI
    st.markdown(f"**Logged in as:** {st.session_state.get('logged_in_user')}")
    col1, col2 = st.columns(2)
    with col1:
        subject = st.selectbox("Subject:", ["Math", "English", "History", "Science", "CS"])
    with col2:
        mode = st.radio("Mode:", ["Virtual", "In-person"]) 

    col3, col4, col5 = st.columns(3)
    with col3:
        time = st.selectbox("Study Time:", ["Morning", "Afternoon", "Evening"])
    with col4:
        name = st.text_input("Enter your name:")
    with col5:
        privacy = st.selectbox("Do you want others to find you?", ["Yes", "No"]) 

    contact = st.text_input("Contact information:")

    button = st.button("Find Match")
    if button:
        if privacy == "Yes":
            new_user = {"name": name, "subject": subject, "time": time, "mode": mode, "contact": contact}
            save_user(new_user)
        matches = find_match(subject, mode, time, name, contact)
        if matches:
            st.write("You have matches!")
            for m in matches:
                st.write(m["name"], "wants to study", m["subject"], "in the", m["time"].lower(), "(", m["mode"], "), Contact:", m["contact"])
        else:
            st.write("Sorry, no matches yet. Come back later!")

