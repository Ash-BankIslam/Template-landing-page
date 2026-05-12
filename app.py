import streamlit as st
import user_manager as um

if "page" not in st.session_state:
    st.session_state.page = "login"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = None

def login_page():
    st.title("Login")
    username = st.text_input("User ID")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        ok, role = um.verify_user(username, password)
        if ok:
            st.session_state.logged_in = True
            st.session_state.role = role
            st.session_state.username = username
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
    role = st.selectbox("Role", ["analyst","modeller","operation"])
    if st.button("Register"):
        ok, msg = um.register_user(new_user, new_pass, role)
        if ok:
            st.success(msg)
            st.session_state.page = "login"
        else:
            st.error(msg)
    if st.button("Back to Login"):
        st.session_state.page = "login"

def forgot_page():
    st.title("Forgot Password")
    user = st.text_input("User ID")
    new_pass = st.text_input("New Password", type="password")
    if st.button("Reset"):
        users = um.load_users()
        if user in users:
            users[user]["password"] = um.bcrypt.hashpw(new_pass.encode(), um.bcrypt.gensalt()).decode()
            um.save_users(users)
            st.success("Password reset successfully")
            st.session_state.page = "login"
        else:
            st.error("User not found")
    if st.button("Back to Login"):
        st.session_state.page = "login"

if not st.session_state.logged_in:
    if st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "signup":
        signup_page()
    elif st.session_state.page == "forgot":
        forgot_page()
else:
    st.title("Dashboard")
    st.write(f"Welcome {st.session_state.username} ({st.session_state.role})")
