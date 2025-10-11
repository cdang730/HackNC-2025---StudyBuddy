import json
import hashlib
from pathlib import Path


# File paths
USER_DATA_FILE = Path("data/user_data.json")

def register_user(username: str, master_password: str) -> None:
    """Register a new user with a master password."""
    hashed_pw = hashlib.sha256(master_password.encode()).hexdigest()
    # load existing, else empty dict
    if USER_DATA_FILE.exists():
        with open(USER_DATA_FILE, "r") as f:
            users = json.load(f)
    else:
        users = {}

    # save or update user
    if username in users:
        print("Username exists")
        return

    users[username] = hashed_pw

    USER_DATA_FILE.parent.mkdir(exist_ok=True)
    with open(USER_DATA_FILE, "w") as f:
        json.dump(users, f, indent = 4)

    print(f"User -{username}- registered succssfully!")


def login(username: str, master_password: str) -> bool:
    """Check login credentials"""
    if not USER_DATA_FILE.exists():
        print("No users found. Please register.")
        return False
    
    with open(USER_DATA_FILE, "r") as f:
        users = json.load(f)

    hashed_pw = hashlib.sha256(master_password.encode()).hexdigest()

    if username in users and users[username] == hashed_pw:
        print("Login successful!")    
        return True
    else:
        print("Invalid user name or password. Please try again.")
        return False
    


def main() -> None:
    while True:
        action = input("Do you want to (r)egister or (l)ogin?\n").strip().lower()

        if action == "r":
            username = input("Enter new username: ").strip()
            password = input("Enter master password: ").strip()
            register_user(username, password)
        elif action == "l":
            username = input("Enter username: ").strip()
            password = input("Enter master password: ").strip()
            # attempt login and repeat until successful or user cancels
            success = login(username, password)
            if success:
                break
            else:
                # allow retry or go back to register/login prompt
                continue
        else:
            print("Invalid option. Please type r or l")


if __name__ == "__main__":
    main()