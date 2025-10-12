import streamlit as st
from backend import get_user_info_with_index, delete_info_by_index

st.title("Delete Your Study Sessions")

# Get user name from session or input
if hasattr(st, 'user') and getattr(st.user, 'is_logged_in', False):
    user_name = st.user.name
    st.write(f"Logged in as: **{user_name}**")
elif st.session_state.get("logged_in", False):
    user_name = st.session_state.get("user_name", "")
    st.write(f"Logged in as: **{user_name}**")
else:
    st.error("Please log in to manage your study sessions.")
    st.stop()

# Allow manual name override for testing
with st.expander("Override name (for testing)"):
    override_name = st.text_input("Enter name to search:", value=user_name)
    if override_name:
        user_name = override_name

if user_name:
    # Get user's study sessions from Supabase
    try:
        user_sessions = get_user_info_with_index(user_name)
        
        if user_sessions:
            st.success(f"Found {len(user_sessions)} study session(s) for **{user_name}**")
            
            # Display sessions in a table format
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
                        # Delete button for each session
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
                    # Confirmed - delete all
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
                    # Ask for confirmation
                    st.session_state["confirm_delete_all"] = True
                    st.warning("⚠️ Click 'Delete All My Sessions' again to confirm deletion of ALL your study sessions.")
            
            # Reset confirmation if user doesn't follow through
            if st.session_state.get("confirm_delete_all", False):
                if st.button("Cancel", key="cancel_delete_all"):
                    st.session_state["confirm_delete_all"] = False
                    st.rerun()
        
        else:
            st.info(f"No study sessions found for **{user_name}**")
            st.write("You haven't created any study sessions yet. Go to the main page to create one!")
    
    except Exception as e:
        st.error(f"Error loading your study sessions: {str(e)}")
        st.write("This might be due to:")
        st.write("- Supabase connection issues")
        st.write("- Missing credentials")
        st.write("- Database table not found")

else:
    st.warning("Please enter your name to view your study sessions.")

# Navigation
st.markdown("---")
if st.button("← Back to Main App"):
    st.switch_page("app.py")