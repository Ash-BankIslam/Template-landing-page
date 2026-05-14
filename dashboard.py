import streamlit as st

def show_dashboard(role, username):
    st.title("Dashboard")
    st.write(f"Welcome {username} ({role})")

    # Define what each role can see
    role_pages = {
        "admin": ["Overview", "User Management", "Reports", "Settings"],
        "modeller": ["Overview", "Model Builder", "Data Upload", "Reports", "Simulation", "Settings"],
        "analyst": ["Overview", "Reports", "Data Explorer", "Settings"],
        "operation": ["Overview", "Reports", "Settings"]
    }

    allowed_tabs = role_pages.get(role, ["Overview"])
    selected_tab = st.sidebar.radio("Navigation", allowed_tabs)

    # Render content based on selected tab
    if selected_tab == "Overview":
        st.subheader("Overview")
        st.write("General overview content here.")

    elif selected_tab == "User Management" and role == "admin":
        st.subheader("User Management")
        st.write("Admin-only: manage users here.")

    elif selected_tab == "Reports":
        st.subheader("Reports")
        st.write("Reports content here.")

    elif selected_tab == "Settings":
        st.subheader("Settings")
        st.write("Settings content here.")

    elif selected_tab == "Model Builder" and role == "modeller":
        st.subheader("Model Builder")
        st.write("Modeller-only: build models here.")

    elif selected_tab == "Data Upload" and role == "modeller":
        st.subheader("Data Upload")
        st.write("Upload datasets for modelling.")

    elif selected_tab == "Simulation" and role == "modeller":
        st.subheader("Simulation")
        st.write("Run simulations here.")

    elif selected_tab == "Data Explorer" and role == "analyst":
        st.subheader("Data Explorer")
        st.write("Analyst-only: explore datasets here.")

    # Logout button
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "login"

