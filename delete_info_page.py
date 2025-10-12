import streamlit as st
from backend import get_user_info_with_index, delete_info_by_index

st.title("Delete Your Saved Entries")

username = st.text_input("Enter your username to list your entries:")

if st.button("Show my entries") and username.strip():
    entries = get_user_info_with_index(username.strip())
    if not entries:
        st.info("No entries found for that username.")
    else:
        st.write(f"Found {len(entries)} entries for {username.strip()}:")
        for idx, row in entries:
            cols = st.columns([6, 1])
            with cols[0]:
                st.write(f"Subject: {row.get('subject')} | Mode: {row.get('mode')} | Time: {row.get('time')} | Contact: {row.get('contact')}")
            with cols[1]:
                if st.button(f"Delete {idx}"):
                    if delete_info_by_index(idx):
                        st.success("Deleted entry.")
                        st.experimental_rerun()
                    else:
                        st.error("Failed to delete entry. It may have already been removed.")


st.markdown("---")
st.write("Tip: When you delete an entry, the CSV is rewritten. If multiple people are using the app concurrently, consider adding locking or moving to a small database.")