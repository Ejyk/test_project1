import streamlit as st

ADMINS = {"admin": "XrU2rXe^z"}  # move to st.secrets in production

def admin_login_required():
    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False

    if not st.session_state.admin_logged_in:
        st.subheader("Admin Login")

        with st.form("admin_login"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login = st.form_submit_button("Login")

        if login:
            if ADMINS.get(username) == password:
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("Invalid credentials")

        st.stop()
