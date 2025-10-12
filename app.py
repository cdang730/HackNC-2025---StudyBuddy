import streamlit as st
from backend import save_user, find_match
from pathlib import Path

# Load and apply custom CSS from the same directory as this file.
st.markdown('<style>' + open('style.css').read() + '</style>', unsafe_allow_html=True)

if not st.user.is_logged_in:
    if st.button("Login with Google"):
        st.login()
    elif st.button("Login with Password"):
        st.markdown("---")
        import userlogin
    st.stop()


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

