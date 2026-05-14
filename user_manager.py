import bcrypt
from supabase import create_client
import streamlit as st

# --- Supabase connection ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# --- User management functions ---
def register_user(username: str, password: str, role: str):
    """Register a new user with hashed password and role."""
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    supabase.table("users").insert({
        "username": username,
        "password": hashed,
        "role": role
    }).execute()

def verify_user(username: str, password: str):
    """Verify login credentials. Returns (True, role) if valid, else (False, None)."""
    result = supabase.table("users").select("*").eq("username", username).execute()
    if result.data:
        stored_hash = result.data[0]["password"].encode()
        if bcrypt.checkpw(password.encode(), stored_hash):
            return True, result.data[0]["role"]
    return False, None

def reset_password(username: str, new_pass: str):
    """Reset a user's password by updating the hash in Supabase."""
    new_hash = bcrypt.hashpw(new_pass.encode(), bcrypt.gensalt()).decode()
    supabase.table("users").update({"password": new_hash}).eq("username", username).execute()

def get_all_users():
    """Optional: Fetch all users (for admin dashboard)."""
    return supabase.table("users").select("id, username, role, created_at").execute().data
