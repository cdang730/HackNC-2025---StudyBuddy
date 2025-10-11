"""data handeling and mathcin gunctions"""

import csv
import os


def save_user(data, filename = "users.csv"):
    """save user imput data into the user file"""
    file_exist = os.path.isfile(filename)
    with open(filename, "a", newline = '', encoding = 'utf-8') as file:
        writer = csv.writer(file)

        # check if the file exists
        if not file_exist:
            writer.writerow(["name", "subject", "mode", "time"])

        # write the user data row
        writer.writerow([data["name"], data["subject"], data["mode"], data["time"]])


def load_users(filename = "usrs.csv"):
    """Return a list of all usrs as dictionaries"""
    users = []

    if os.path.exists(filename):
        with open(filename, newline = "", encoding = "utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                users.append(row)
    return users


def find_match(subject, mode, time, name, filename = "users.csv"):
    """Return users who have the same subject mode and time"""
    users = load_users(filename)
    matches = []

    for user in users:
        if (user["subject"] == subject and
            user ["mode"] == mode and
            user ["time"] == time and
            user ["name"] != name):
            matches.append(user)

    return matches


if __name__ == "__main__":
    # add some prefill tutors for student to choose
    save_user({"name": "Tutor1", "subject": "Math", "mode": "Virtual", "time": "Evening"})
    save_user({"name": "Tutor2", "subject": "CS", "mode": "In-person", "time": "Afternoon"})
    save_user({"name": "Tutor3", "subject": "History", "mode": "In-person", "time": "Afternoon"})
    save_user({"name": "Tutor4", "subject": "Science", "mode": "In-person", "time": "Evening"})
    save_user({"name": "Tutor5", "subject": "English", "mode": "Virtual", "time": "Morning"})

    print("All users: ", load_users())

    result = find_match("Math", "Virtual", "Evening", "Dorothy")
    print("Matches for Alice: ", result)