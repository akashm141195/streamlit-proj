import streamlit as st
from models import get_user, add_user
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_users():
    pass

def login_user(username: str, password: str) -> bool:
    try:
        user = get_user(username)
        if user is not None and user['password'] == password:  # In production, use proper password hashing
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.session_state['character_class'] = user['character_class']
            st.session_state['level'] = user['level']
            st.session_state['exp'] = user['exp']
            logger.info(f"User {username} logged in successfully")
            return True
        logger.warning(f"Failed login attempt for user {username}")
        return False
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        return False

def register_user(username: str, password: str, character_class: str) -> bool:
    try:
        if add_user(username, password, character_class):
            logger.info(f"Successfully registered new user: {username}")
            return True
        logger.warning(f"Registration failed: Username {username} already exists")
        return False
    except Exception as e:
        logger.error(f"Error during registration: {str(e)}")
        return False

def logout_user():
    try:
        username = st.session_state.get('username', 'Unknown')
        for key in st.session_state.keys():
            del st.session_state[key]
        logger.info(f"User {username} logged out successfully")
    except Exception as e:
        logger.error(f"Error during logout: {str(e)}")