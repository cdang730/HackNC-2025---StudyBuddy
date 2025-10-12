import streamlit as st
from backend import save_user, find_match, get_user_info_with_index, delete_info_by_index
from userlogin import register_user, login


# ----------------------
# INITIAL SETUP
# ----------------------
if "page" not in st.session_state:
    st.session_state.page = "Login"

if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None


def is_logged_in():
    """True if logged in via password or Google."""
    return bool(st.session_state.logged_in_user or (hasattr(st, "user") and st.user.is_logged_in))


def current_user_name():
    """Return the display name of the current user."""
    if hasattr(st, "user") and st.user.is_logged_in:
        return st.user.name
    return st.session_state.logged_in_user


def switch_page(new_page):
    """Allow navigation only if logged in."""
    if is_logged_in():
        st.session_state.page = new_page
        # no need to st.rerun() — Streamlit auto-refreshes after a button press
    else:
        st.warning("⚠️ Please log in first to access this page.")



# ----------------------
# SIDEBAR NAVIGATION
# ----------------------
st.sidebar.title("Navigation")
st.sidebar.button("🏠 Login", on_click=lambda: switch_page("Login"))
st.sidebar.button("🔍 Find Buddy", on_click=lambda: switch_page("Find Buddy"))
st.sidebar.button("🗑️ Delete Info", on_click=lambda: switch_page("Delete Info"))


# ----------------------
# PAGE: LOGIN (Both Options)
# ----------------------
if st.session_state.page == "Login":
    st.title("🔐 Study Buddy Planner Login")

    # Create two login sections: Google and Password
    st.subheader("Choose your login method")

    col1, col2 = st.columns(2)

    # --- Google Login ---
    with col1:
        st.markdown("### 🌐 Google Sign-In")
        if hasattr(st, "user") and not st.user.is_logged_in:
            if st.button("Login with Google"):
                st.login()
            st.info("Sign in using your Google account.")
        elif hasattr(st, "user") and st.user.is_logged_in:
            st.success(f"✅ Logged in as {st.user.name}")
            if st.button("Log out"):
                st.logout()
                st.experimental_rerun()

    # --- Username/Password Login ---
    with col2:
        st.markdown("### 🔑 Password Login")

        username = st.text_input("Username:")
        password = st.text_input("Password:", type="password")

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Login"):
                if login(username.strip(), password.strip()):
                    st.session_state.logged_in_user = username.strip()
                    st.success(f"✅ Welcome, {username.strip()}!")
                else:
                    st.error("❌ Invalid username or password.")
        with col_b:
            if st.button("Sign up"):
                register_user(username.strip(), password.strip())
                st.success("🎉 Account created! You can now log in.")

    # --- Info after login ---
    if is_logged_in():
        st.markdown(f"**Logged in as:** {current_user_name()}")
        st.info("You can now use the sidebar to find buddies or delete info.")


# ----------------------
# PAGE: FIND BUDDY
# ----------------------
elif st.session_state.page == "Find Buddy":
    if is_logged_in():
        st.markdown('<style>' + open('style.css').read() + '</style>', unsafe_allow_html=True)
        st.title("🧑‍🤝‍🧑 Find Your Study Buddy")

        st.markdown(f"Welcome, **{current_user_name()}**!")

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
                st.info("No matches yet. Check back later!")
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

        if st.button("Show my entries") and username.strip():
            # Fetch entries from Supabase for this username
            response = supabase.table("study_buddy").select("*").eq("username", username.strip()).execute()
            entries = response.data  # Extract only the list of rows

            if not entries:
                st.info("No entries found for that username.")
            else:
                st.write(f"Found {len(entries)} entries for {username.strip()}:")
                for idx, row in enumerate(entries):
                    cols = st.columns([6, 1])
                    with cols[0]:
                        st.write(
                            f"Subject: {row.get('subject')} | Mode: {row.get('mode')} | "
                            f"Time: {row.get('time')} | Contact: {row.get('contact')}"
                        )
                    with cols[1]:
                        if st.button(f"Delete {idx}", key=f"delete_{idx}"):
                            # Delete entry from Supabase using its unique id
                            delete_response = supabase.table("study_buddy").delete().eq("id", row["id"]).execute()

                            if delete_response.data:
                                st.success("✅ Deleted entry.")
                                st.stop()  # Stop and re-render cleanly instead of st.rerun()
                            else:
                                st.error("❌ Failed to delete entry. It may have already been removed.")

else:
    st.session_state.page = "Login"
    st.warning("⚠️ Please log in first to access this page.")
    st.rerun()
