import json, bcrypt

USER_FILE = "users.json"

def load_users():
    try:
        with open(USER_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

def register_user(username, password, role):
    users = load_users()
    if username in users:
        return False, "User already exists"
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    users[username] = {"password": hashed, "role": role}
    save_users(users)
    return True, f"User {username} registered as {role}"

def verify_user(username, password):
    users = load_users()
    if username in users:
        stored_hash = users[username]["password"].encode()
        if bcrypt.checkpw(password.encode(), stored_hash):
            return True, users[username]["role"]
    return False, None

def change_password(username, old_pass, new_pass):
    users = load_users()
    if username not in users:
        return False, "User not found"
    stored_hash = users[username]["password"].encode()
    if bcrypt.checkpw(old_pass.encode(), stored_hash):
        new_hash = bcrypt.hashpw(new_pass.encode(), bcrypt.gensalt()).decode()
        users[username]["password"] = new_hash
        save_users(users)
        return True, "Password updated"
    return False, "Old password incorrect"
