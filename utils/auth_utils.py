import streamlit as st
import json
import os
from datetime import datetime, timedelta

USERS_FILE = "data/users.json"

def _load_users():
    """Loads user data from the JSON file."""
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists(USERS_FILE) or os.stat(USERS_FILE).st_size == 0:
        # Create a dummy users.json if it doesn't exist
        dummy_users = [
            {"username": "teacher1", "password": "password123", "role": "teacher"},
            {"username": "parent1", "password": "password123", "role": "parent"},
            {"username": "admin", "password": "adminpassword", "role": "admin"}
        ]
        with open(USERS_FILE, 'w') as f:
            json.dump(dummy_users, f, indent=2)
        return dummy_users
    
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        st.error("Error: users.json is corrupt. Please check the file.")
        return []
    except Exception as e:
        st.error(f"Error loading user data: {e}")
        return []

def authenticate_user(username, password):
    """Authenticates a user based on username and password."""
    users = _load_users()
    for user in users:
        if user["username"] == username and user["password"] == password:
            st.session_state["authenticated"] = True
            st.session_state["username"] = user["username"]
            st.session_state["role"] = user["role"]
            return True
    st.session_state["authenticated"] = False
    return False

def logout_user():
    """Logs out the current user."""
    st.session_state["authenticated"] = False
    st.session_state["username"] = None
    st.session_state["role"] = None
    st.success("You have been logged out.")
    st.switch_page("app.py") # Redirect to login page after logout

def is_authenticated():
    """Checks if a user is currently authenticated."""
    return st.session_state.get("authenticated", False)

def get_user_role():
    """Returns the role of the authenticated user."""
    return st.session_state.get("role")

def render_login_page():
    """Renders the login form."""
    # Wrap the entire login content in a div with a specific class for styling
    st.markdown(
        """
        <div class="login-container">
        """,
        unsafe_allow_html=True
    )
    
    st.title("EduScan Login")
    st.markdown("Please log in to access the application.")

    with st.form("login_form"):
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        submitted = st.form_submit_button("Login")

        if submitted:
            if authenticate_user(username, password):
                st.success(f"Welcome, {st.session_state['username']} ({st.session_state['role'].capitalize()})!")
                st.switch_page("app.py") # Use st.switch_page for full redirect
            else:
                st.error("Invalid username or password.")
                
    st.markdown("---")
    st.markdown("### Demo Accounts:")
    st.markdown("- **Teacher:** `teacher1` / `password123`")
    st.markdown("- **Parent:** `parent1` / `password123`")
    st.markdown("- **Admin:** `admin` / `adminpassword`")

    st.markdown(
        """
        </div>
        """,
        unsafe_allow_html=True
    )