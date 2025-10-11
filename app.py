import streamlit as st
from backend import save_user, find_match

st.title("Studdy Buddy Planner")
col1, col2 = st.columns(2)
with col1: subject = st.selectbox("Subject: ", ["Math", "English", "History", "Science", "CS"])
with col2: mode = st.radio("Mode: ", ["Virtual", "In-Person"])

col3, col4, col5 = st.columns(3)
with col3: time = st.selectbox("Study Time: ", ["Morning", "Afternoon", "Evening"])
with col4: name = st.text_input("Enter your name: ")
with col5: privacy = st.selectbox("Do you want others to find you? ", ["Yes", "No"])


button = st.button("Find Match")
if button:
    if privacy == "Yes":
        new_user = {"name": name, "subject": subject, "time": time, "mode": mode}
        save_user(new_user)
    matches = find_match(subject, mode, time, name)
    if matches:
        st.write("You have matches!")
        for m in matches:
            st.write(m["name"], "wants to study", m["subject"], "in the ", m["time"].lower(), "(", m["mode"], ")")
    elif not matches:
        st.write("Sorry, no matches yet. Come back later!")
