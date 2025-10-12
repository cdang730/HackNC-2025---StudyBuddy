import streamlit as st
from backend import save_user, find_match, get_user_info_with_index, delete_info_by_index
from userlogin import register_user, login


# ----------------------
# INITIAL SETUP
# ----------------------
if "page" not in st.session_state:
    st.session_state.page = "Login"

# Track password-based login separately
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None


def is_logged_in():
    """Return True if user logged in via either Google or password."""
    return bool(st.session_state.logged_in_user or (hasattr(st, "user") and st.user.is_logged_in))


def current_user_name():
    """Return current user's display name (Google name or username)."""
    if hasattr(st, "user") and st.user.is_logged_in:
        return st.user.name
    return st.session_state.logged_in_user


def switch_page(new_page):
    """Switch only if logged in."""
    if is_logged_in():
        st.session_state.page = new_page
        st.rerun()
    else:
        st.warning("⚠️ Please log in first to access this page.")


# ----------------------
# SIDEBAR NAVIGATION
# ----------------------
st.sidebar.title("Navigation")
st.sidebar.button("🏠 Login", on_click=lambda: switch_page("Login"))
st.sidebar.button("🔍 Find Buddy", on_click=lambda: switch_page("Find Buddy"))
st.sidebar.button("🗑️ Delete Info", on_click=lambda: switch_page("Delete Info"))

correct_user: bool = True
# ----------------------
# PAGE: LOGIN
# ----------------------
if st.session_state.page == "Login":
    st.title("Study Buddy Planner - Login")

    # --- Google Sign-in Section (works on Streamlit Cloud) ---
    if hasattr(st, "user") and not st.user.is_logged_in:
        st.subheader("🔐 Sign in with Google")
        if st.button("Login with Google"):
            st.login()
        st.stop()

    # --- Password Login Section ---
    st.subheader("Or use your account credentials")

    username = st.text_input("Enter your username:")
    password = st.text_input("Enter your password:", type="password")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login"):
            if login(username.strip(), password.strip()):
                st.session_state.logged_in_user = username.strip()
                st.success("✅ Login successful!")
            else:
                st.error("❌ Invalid username or password. Please try again.")
    with col2:
        if st.button("Sign up"):
            register_user(username.strip(), password.strip())
            st.success("🎉 Registered! You can now log in.")

    # --- After login, show user info ---
    if is_logged_in():
        st.markdown(f"**Logged in as:** {current_user_name()}")
        st.info("You can now use the sidebar to find buddies or delete info.")

        if hasattr(st, "user") and st.user.is_logged_in:
            if st.button("Log out"):
                st.logout()
                st.experimental_rerun()


# ----------------------
# PAGE: FIND BUDDY
# ----------------------

elif st.session_state.page == "Find Buddy":
    if is_logged_in():
        st.markdown('<style>' + open('style.css').read() + '</style>', unsafe_allow_html=True)
        st.title("🧑‍🤝‍🧑 Study Buddy Planner")

        if hasattr(st, "user") and st.user.is_logged_in:
            st.markdown(f"Welcome! Your name: **{st.user.name}**")
            if st.button("Log out"):
                st.logout()
                st.experimental_rerun()
        else:
            st.markdown(f"Welcome! Your name: **{st.session_state.logged_in_user}**")

        col1, col2 = st.columns(2)
        with col1:
            subject = st.selectbox("Subject: ", ["Math", "English", "History", "Science", "CS"])
        with col2:
            mode = st.radio("Mode: ", ["Virtual", "In-Person"])

        col3, col4, col5 = st.columns(3)
        with col3:
            time = st.selectbox("Study Time: ", ["Morning", "Afternoon", "Evening"])
        with col4:
            name = st.text_input("Enter your name:")
            if current_user_name != name:
                correct_user = False
        with col5:
            privacy = st.selectbox("Do you want others to find you?", ["Yes", "No"])

        contact = st.text_input("Contact information:")

        if st.button("Find Match"):
            if privacy == "Yes":
                new_user = {"name": name, "subject": subject, "time": time, "mode": mode, "contact": contact}
                save_user(new_user)
            matches = find_match(subject, mode, time, name, contact)
            if matches:
                st.success("🎯 You have matches!")
                for m in matches:
                    st.write(
                        f"{m['name']} wants to study {m['subject']} in the {m['time'].lower()} "
                        f"({m['mode']}), Contact: {m['contact']}"
                    )
            else:
                st.info("No matches yet. Come back later!")
    else:
        st.session_state.page = "Login"
        st.warning("⚠️ Please log in first to access this page.")
        st.rerun()


# ----------------------
# PAGE: DELETE INFO
# ----------------------
elif st.session_state.page == "Delete Info":
    if is_logged_in():
        st.title("🗑️ Delete Your Saved Entries")

        username = st.text_input("Enter your username to list your entries:")
        if st.button("Show my entries") and username.strip() and correct_user:
            entries = get_user_info_with_index(username.strip())
            if not entries:
                st.info("No entries found for that username.")
            else:
                st.write(f"Found {len(entries)} entries for {username.strip()}:")
                for idx, row in entries:
                    cols = st.columns([6, 1])
                    with cols[0]:
                        st.write(
                            f"Subject: {row.get('subject')} | Mode: {row.get('mode')} | "
                            f"Time: {row.get('time')} | Contact: {row.get('contact')}"
                        )
                    with cols[1]:
                        if st.button(f"Delete {idx}"):
                            if delete_info_by_index(idx):
                                st.success("✅ Deleted entry.")
                                st.rerun()
                            else:
                                st.error("❌ Failed to delete entry. It may have already been removed.")
        elif st.button("Show my entries") and username.strip() and not correct_user:
            st.write("Please input your name correctly.")
    else:
        st.session_state.page = "Login"
        st.warning("⚠️ Please log in first to access this page.")
        st.rerun()
