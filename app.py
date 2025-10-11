import streamlit as st
from backend import save_user
from backend import find_match

st.title("Studdy Buddy Planner")
col1, col2 = st.columns(2)
with col1: subject = st.multiselect("Subject: ", ["Math", "English", "History", "Science", "CS"])
with col2: mode = st.radio("Mode: ", ["Virtual", "In-Person"])

col3, col4 = st.columns(2)
with col3: time = st.selectbox("Study Time: ", ["Morning", "Afternoon", "Evening"])
with col4: name = st.text_input("Enter your name: ")


button = st.button("Find Match")
if button:
    new_user = {"name": name, "subject": subject, "time": time, "mode": mode}
    save_user(new_user)
    matches = find_match(subject, mode, time)
    if matches:
        st.write("You have matches!")
    else:
        st.write("Sorry, no matches yet. Come back later!")
