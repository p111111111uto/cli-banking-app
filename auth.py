import hashlib
import json
from pathlib import Path

# Path is resolved relative to this file so the app works from any directory
DATA_FILE = Path(__file__).resolve().parent / 'data' / 'users.json'


def load_users():
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as file:
                return json.load(file)
        except json.JSONDecodeError:
            # File exists but is empty or corrupt — treat as no users yet
            return {}
    return {}


def save_users(users):
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(users, file, indent=2)


def register():
    users = load_users()
    name = input('Please enter your name:\n')

    while True:
        # Usernames are lowercased so "Bob" and "bob" are the same account
        username = input('Please create a username:\n').lower()
        if username in users:
            print(f'{username} already exists, please make a new one')
            continue
        break

    password = input('Create a password:\n')
    # SHA-256 hashes the password so the plain-text is never stored on disk
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    users[username] = {'name': name, 'password': hashed_password}
    save_users(users)
    print('Registration complete.')

    return username


def login():
    users = load_users()

    username = input('Enter your username:')
    if username not in users:
        print('Username not found')
        return None

    password = input('Enter your password:')
    # Hash the attempt and compare against the stored hash — never compare plain-text
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if users[username]['password'] == hashed_password:
        return username
    else:
        return None
