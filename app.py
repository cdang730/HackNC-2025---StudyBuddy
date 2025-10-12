import streamlit as st
from backend import save_user, find_match
from pathlib import Path

# Load and apply custom CSS from the same directory as this file.
st.markdown('<style>' + open('style.css').read() + '</style>', unsafe_allow_html=True)

if not st.user.is_logged_in:
    if st.button("Login with Google"):
        st.login()
    st.stop()

if st.button("Log out"):
    st.logout()
st.markdown(f"Welcome! Your name: {st.user.name}")

# Initialize page state
if "current_page" not in st.session_state:
    st.session_state.current_page = "main"

# Navigation buttons
col_welcome, col_manage = st.columns([3, 1])
with col_manage:
    if st.button("📝 Manage Sessions"):
        st.session_state.current_page = "manage"
        st.rerun()

# Show content based on current page
if st.session_state.current_page == "manage":
    # Import and show delete info page content
    from backend import get_user_info_with_index, delete_info_by_index
    
    st.title("Delete Your Study Sessions")
    
    user_name = st.user.name
    st.write(f"Logged in as: **{user_name}**")
    
    if user_name:
        try:
            user_sessions = get_user_info_with_index(user_name)
            
            if user_sessions:
                st.success(f"Found {len(user_sessions)} study session(s) for **{user_name}**")
                
                st.subheader("Your Study Sessions:")
                
                for i, session in enumerate(user_sessions):
                    with st.container():
                        col1, col2, col3 = st.columns([3, 2, 1])
                        
                        with col1:
                            st.write(f"**{session['subject']}** - {session['mode']}")
                            st.write(f"📅 {session['time']} | 📧 {session['contact']}")
                            if 'created_at' in session:
                                st.caption(f"Created: {session['created_at'][:19]}")
                        
                        with col2:
                            st.write(f"ID: {session['id']}")
                        
                        with col3:
                            if st.button(f"🗑️ Delete", key=f"delete_{session['id']}"):
                                try:
                                    success = delete_info_by_index(session['id'])
                                    if success:
                                        st.success(f"Deleted session: {session['subject']} - {session['mode']}")
                                        st.rerun()
                                    else:
                                        st.error("Failed to delete session")
                                except Exception as e:
                                    st.error(f"Error deleting session: {str(e)}")
                        
                        st.divider()
                
                # Bulk delete option
                st.subheader("Bulk Actions")
                if st.button("🗑️ Delete All My Sessions", type="secondary"):
                    if st.session_state.get("confirm_delete_all", False):
                        deleted_count = 0
                        for session in user_sessions:
                            try:
                                if delete_info_by_index(session['id']):
                                    deleted_count += 1
                            except Exception as e:
                                st.error(f"Error deleting session {session['id']}: {str(e)}")
                        
                        st.success(f"Deleted {deleted_count} session(s)")
                        st.session_state["confirm_delete_all"] = False
                        st.rerun()
                    else:
                        st.session_state["confirm_delete_all"] = True
                        st.warning("⚠️ Click 'Delete All My Sessions' again to confirm deletion of ALL your study sessions.")
                
                if st.session_state.get("confirm_delete_all", False):
                    if st.button("Cancel", key="cancel_delete_all"):
                        st.session_state["confirm_delete_all"] = False
                        st.rerun()
            
            else:
                st.info(f"No study sessions found for **{user_name}**")
                st.write("You haven't created any study sessions yet. Go to the main page to create one!")
        
        except Exception as e:
            st.error(f"Error loading your study sessions: {str(e)}")
    
    # Back button
    if st.button("← Back to Main App"):
        st.session_state.current_page = "main"
        st.rerun()

else:
    # Main app content
    st.title("Studdy Buddy Planner")
    col1, col2 = st.columns(2)
    with col1: subject = st.selectbox("Subject: ", ["Math", "English", "History", "Science", "CS"])
    with col2: mode = st.radio("Mode: ", ["Virtual", "In-Person"])

    col3, col4, col5 = st.columns(3)
    with col3: time = st.selectbox("Study Time: ", ["Morning", "Afternoon", "Evening"])
    with col4: name = st.text_input("Enter your name: ")
    correct_name: bool = True
    if name != st.user.name:
        correct_name = False
    with col5: privacy = st.selectbox("Do you want others to find you? ", ["Yes", "No"])

    contact = st.text_input("Contact information: ")


    button = st.button("Find Match")
    if button and correct_name:
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
    elif button and not correct_name:
        st.write("Please input your name.")