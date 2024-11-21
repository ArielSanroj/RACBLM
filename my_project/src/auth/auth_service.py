import streamlit as st

class AuthService:
    def __init__(self):
        if 'users' not in st.session_state:
            st.session_state.users = {}

    def register(self, email: str, password: str, name: str, service: str) -> bool:
        if email in st.session_state.users:
            return False

        st.session_state.users[email] = {
            "password": password,
            "name": name,
            "service": service
        }
        return True

    def login(self, email: str, password: str) -> bool:
        if email in st.session_state.users:
            if st.session_state.users[email]["password"] == password:
                st.session_state.current_user = {
                    "email": email,
                    "name": st.session_state.users[email]["name"],
                    "service": st.session_state.users[email]["service"]
                }
                return True
        return False