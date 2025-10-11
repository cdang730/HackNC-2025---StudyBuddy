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
            writer.writerow(["name", "subject", "mode", "time", "contact"])

        # write the user data row
        writer.writerow([data["name"], data["subject"], data["mode"], data["time"], data["contact"]])


def load_users(filename = "users.csv"):
    """Return a list of all users as dictionaries."""
    users = []

    if os.path.exists(filename):
        with open(filename, newline = "", encoding = "utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                users.append(row)
    return users


def find_match(subject, mode, time, name, contact, filename = "users.csv"):
    """Return users who have the same subject mode and time"""
    users = load_users(filename)
    matches = []

    for user in users:
        if (user["subject"] == subject and
            user ["mode"] == mode and
            user ["time"] == time and
            user ["name"] != name and
            user ["contact"] != contact):
            matches.append(user)

    return matches



# No need prefill anymore
"""if __name__ == "__main__":
    filename = "users.csv"

    # Only prefill tutors if the users file doesn't exist or is empty.
    existing_users = load_users(filename)
    if not existing_users:
        # add some prefill tutors for student to choose
        prefill = [
            {"name": "Tutor1", "subject": "Math", "mode": "Virtual", "time": "Evening"},
            {"name": "Tutor2", "subject": "CS", "mode": "In-person", "time": "Afternoon"},
            {"name": "Tutor3", "subject": "History", "mode": "In-person", "time": "Afternoon"},
            {"name": "Tutor4", "subject": "Science", "mode": "In-person", "time": "Evening"},
            {"name": "Tutor5", "subject": "English", "mode": "Virtual", "time": "Morning"},
        ]
        for tutor in prefill:
            save_user(tutor, filename)
        print(f"Prefilled {len(prefill)} tutors into '{filename}'.")
    else:
        print(f"Users file '{filename}' already has {len(existing_users)} entries; skipping prefill.")
"""