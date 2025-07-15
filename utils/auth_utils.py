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
    """Renders the enhanced professional login form."""
    # Enhanced login page with better styling and professional layout
    st.markdown(
        """
        <div class="login-page-container">
            <div class="login-form-card">
                <div class="login-header-section">
                    <div class="login-brand-logo">
                        <span class="material-symbols-outlined">school</span>
                    </div>
                    <h1 class="login-title">Welcome to EduScan</h1>
                    <p class="login-subtitle">Advanced Learning Assessment Platform</p>
                    <div class="login-divider"></div>
                </div>
        """,
        unsafe_allow_html=True
    )
    
    # Login form section
    with st.form("login_form", clear_on_submit=False):
        st.markdown(
            '''
            <style>
                .login-form-section {
                    max-width: 200px;
                    margin: 0 auto;
                }
            </style>
            <div class="login-form-section">
            ''',
            unsafe_allow_html=True
        )
        
        username = st.text_input(
            "Username", 
            key="login_username",
            placeholder="Enter your username",
            help="Use your assigned EduScan username"
        )
        password = st.text_input(
            "Password", 
            type="password", 
            key="login_password",
            placeholder="Enter your password",
            help="Enter your secure password"
        )
        
        # Add some spacing before the button
        st.markdown('<div style="margin: 1.5rem 0;"></div>', unsafe_allow_html=True)
        
        submitted = st.form_submit_button(
            "🔐 Sign In to EduScan", 
            use_container_width=True,
            type="primary"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)

        if submitted:
            if username and password:  # Basic validation
                if authenticate_user(username, password):
                    st.success(f"✅ Welcome back, {st.session_state['username']}!")
                    st.balloons()  # Add a nice touch
                    st.switch_page("app.py")
                else:
                    st.error("❌ Invalid credentials. Please check your username and password.")
            else:
                st.warning("⚠️ Please enter both username and password.")
    
    # Demo accounts section with expander and left alignment
    st.markdown("""
        <div class="demo-accounts-section" style="text-align: left;">
            <div class="demo-accounts-header" style="justify-content: flex-start; margin-bottom: 0;">
                <span class="material-symbols-outlined" style="margin-right: 8px;">account_circle</span>
                <h3 style="margin-bottom: 0;">Quick Demo Access</h3>
            </div>
    """, unsafe_allow_html=True)

    with st.expander("Show Demo Login Details"):
        st.markdown("""
            <p style="font-size: 0.9em; color: var(--gray-600); margin-top: 10px; text-align: left;">
                You can use these demo accounts to explore the platform:
                <br><b>Teacher:</b> teacher1 / password123
                <br><b>Parent:</b> parent1 / password123
                <br><b>Admin:</b> admin / adminpassword
            </p>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        </div>
    """, unsafe_allow_html=True)

    # Footer section
    st.markdown("""
        <div class="login-footer">
            <p>
                <span class="material-symbols-outlined">security</span>
                Your data is secure and protected
            </p>
        </div>
        </div> </div> """, unsafe_allow_html=True)