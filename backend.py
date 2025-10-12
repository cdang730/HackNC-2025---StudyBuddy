"""data handeling and mathcin gunctions"""

import csv
import os


def save_user(data, filename = "users.csv"):
    """save user imput data into the user file"""
    from pathlib import Path
    import csv as _csv

    # Always write next to this file (robust against changing CWD in Streamlit)
    path = (Path(__file__).parent / filename).resolve()

    # Write header if file doesn't exist or is empty
    need_header = (not path.exists()) or (path.stat().st_size == 0)

    fieldnames = ["name", "subject", "mode", "time", "contact"]
    row = {k: (data.get(k, "") if isinstance(data, dict) else "") for k in fieldnames}

    with path.open("a", newline="", encoding="utf-8") as file:
        writer = _csv.DictWriter(file, fieldnames=fieldnames)
        if need_header:
            writer.writeheader()
        writer.writerow(row)
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
    # Use a set to track already-seen users (by name+contact) so we only return unique matches.
    seen = set()
    for user in users:
        # Use .get to avoid KeyError if some rows don't include optional fields like 'contact'
        if (user.get("subject") == subject and
            user.get("mode") == mode and
            user.get("time") == time and
            user.get("name") != name and
            user.get("contact") != contact):

            key = (user.get("name"), user.get("contact"))
            if key not in seen:
                seen.add(key)
                matches.append(user)

    return matches

def get_user_info(name, filename = "users.csv"):
    """Return all entires for a certain name."""
    past_info = []
    if os.path.exists(filename):
        with open(filename, newline = '', encoding = 'utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["name"].lower() == name.lower():
                    past_info.append(row)

    return past_info


def delete_info_by_index(index: int, filename: str = "users.csv") -> bool:
    """Delete a row by its zero-based index (order in the CSV file, excluding header).

    Returns True if deletion succeeded, False otherwise.
    """
    if not os.path.exists(filename):
        return False

    users = load_users(filename)
    if index < 0 or index >= len(users):
        return False

    # Remove the row at the given index
    users.pop(index)

    # Write back preserving contact field
    with open(filename, "w", newline='', encoding='utf-8') as file:
        fieldnames = ["name", "subject", "mode", "time", "contact"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(users)

    return True


def get_user_info_with_index(name, filename = "users.csv"):
    """Return a list of (index, row) tuples for entries that match `name` (case-insensitive)."""
    results = []
    users = load_users(filename)
    for i, row in enumerate(users):
        if row.get("name", "").lower() == name.lower():
            results.append((i, row))
    return results





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