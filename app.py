import streamlit as st

# Load users from storage (JSON/DB)
# For demo, using dictionary
users = {
    "admin": {"password": "admin123", "role": "admin"},
    "bob": {"password": "analyst123", "role": "analyst"},
    "carol": {"password": "modeller123", "role": "modeller"},
    "dave": {"password": "ops123", "role": "operation"}
}

# Session state init
if "page" not in st.session_state:
    st.session_state.page = "login"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = None

# Login page
def login_page():
    st.title("Welcome to the App")
    st.subheader("Login")

    username = st.text_input("User ID")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.role = users[username]["role"]
            st.session_state.username = username
            st.success(f"Logged in as {username} ({st.session_state.role})")
        else:
            st.error("Invalid credentials")

    st.markdown("---")
    if st.button("Sign Up"):
        st.session_state.page = "signup"
    if st.button("Forgot Password"):
        st.session_state.page = "forgot"

# Sign up page
def signup_page():
    st.title("Sign Up")
    new_user = st.text_input("Choose a User ID")
    new_pass = st.text_input("Choose a Password", type="password")
    role = st.selectbox("Select Role", ["analyst","modeller","operation"])
    if st.button("Register"):
        if new_user in users:
            st.error("User already exists")
        else:
            users[new_user] = {"password": new_pass, "role": role}
            st.success(f"User {new_user} registered as {role}")
            st.session_state.page = "login"

    if st.button("Back to Login"):
        st.session_state.page = "login"

# Forgot password page
def forgot_page():
    st.title("Forgot Password")
    user = st.text_input("Enter your User ID")
    new_pass = st.text_input("Enter New Password", type="password")
    if st.button("Reset Password"):
        if user in users:
            users[user]["password"] = new_pass
            st.success("Password reset successfully")
            st.session_state.page = "login"
        else:
            st.error("User not found")

    if st.button("Back to Login"):
        st.session_state.page = "login"

# Routing
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
