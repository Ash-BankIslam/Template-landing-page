import streamlit as st
import bcrypt
from supabase import create_client

# --- Supabase connection ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# --- Session state setup ---
if "page" not in st.session_state:
    st.session_state.page = "login"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None

# --- User management functions ---
def register_user(username, password, role):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    supabase.table("users").insert({
        "username": username,
        "password": hashed,
        "role": role
    }).execute()

def verify_user(username, password):
    result = supabase.table("users").select("*").eq("username", username).execute()
    if result.data:
        stored_hash = result.data[0]["password"].encode()
        if bcrypt.checkpw(password.encode(), stored_hash):
            return True, result.data[0]["role"]
    return False, None

def reset_password(username, new_pass):
    new_hash = bcrypt.hashpw(new_pass.encode(), bcrypt.gensalt()).decode()
    supabase.table("users").update({"password": new_hash}).eq("username", username).execute()

# --- Page functions ---
def login_page():
    st.title("Login")
    username = st.text_input("User ID")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        ok, role = verify_user(username, password)
        if ok:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = role
            st.success(f"Logged in as {username} ({role})")
        else:
            st.error("Invalid credentials")
    if st.button("Sign Up"):
        st.session_state.page = "signup"
    if st.button("Forgot Password"):
        st.session_state.page = "forgot"

def signup_page():
    st.title("Sign Up")
    new_user = st.text_input("Choose User ID")
    new_pass = st.text_input("Choose Password", type="password")
    role = st.selectbox("Role", ["admin", "analyst", "modeller", "operation"])
    if st.button("Register"):
        register_user(new_user, new_pass, role)
        st.success(f"User {new_user} registered as {role}")
        st.session_state.page = "login"
    if st.button("Back to Login"):
        st.session_state.page = "login"

def forgot_page():
    st.title("Forgot Password")
    user = st.text_input("User ID")
    new_pass = st.text_input("New Password", type="password")
    if st.button("Reset"):
        reset_password(user, new_pass)
        st.success("Password reset successfully")
        st.session_state.page = "login"
    if st.button("Back to Login"):
        st.session_state.page = "login"

def dashboard_page():
    st.title("Dashboard")
    st.write(f"Welcome {st.session_state.username} ({st.session_state.role})")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "login"

# --- Routing ---
if not st.session_state.logged_in:
    if st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "signup":
        signup_page()
    elif st.session_state.page == "forgot":
        forgot_page()
else:
    dashboard_page()
