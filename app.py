import streamlit as st
from user_manager import register_user, verify_user, reset_password
import dashboard

# --- Session state setup ---
if "page" not in st.session_state:
    st.session_state.page = "login"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None

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
            st.session_state.page = "dashboard"   # <-- route to dashboard
            st.experimental_rerun()
        else:
            st.error("Invalid credentials")
    if st.button("Sign Up"):
        st.session_state.page = "signup"
        st.experimental_rerun()
    if st.button("Forgot Password"):
        st.session_state.page = "forgot"
        st.experimental_rerun()

def signup_page():
    st.title("Sign Up")
    new_user = st.text_input("Choose User ID")
    new_pass = st.text_input("Choose Password", type="password")
    role = st.selectbox("Role", ["admin", "analyst", "modeller", "operation"])
    if st.button("Register"):
        register_user(new_user, new_pass, role)
        st.success(f"User {new_user} registered as {role}")
        st.session_state.page = "login"
        st.experimental_rerun()
    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.experimental_rerun()

def forgot_page():
    st.title("Forgot Password")
    user = st.text_input("User ID")
    new_pass = st.text_input("New Password", type="password")
    if st.button("Reset"):
        reset_password(user, new_pass)
        st.success("Password reset successfully")
        st.session_state.page = "login"
        st.experimental_rerun()
    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.experimental_rerun()

def dashboard_page():
    dashboard.show_dashboard(st.session_state.role, st.session_state.username)

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
