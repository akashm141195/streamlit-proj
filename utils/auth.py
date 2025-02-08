import streamlit as st
from models import get_db, User
from sqlalchemy.orm import Session
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_users():
    # Database tables are automatically created by SQLAlchemy
    pass

def login_user(username: str, password: str) -> bool:
    db = next(get_db())
    try:
        user = db.query(User).filter(User.username == username).first()
        if user and user.password == password:  # In production, use proper password hashing
            st.session_state['logged_in'] = True
            st.session_state['user_id'] = user.id
            st.session_state['username'] = username
            st.session_state['character_class'] = user.character_class
            st.session_state['level'] = user.level
            st.session_state['exp'] = user.exp
            logger.info(f"User {username} logged in successfully")
            return True
        logger.warning(f"Failed login attempt for user {username}")
        return False
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        return False
    finally:
        db.close()

def register_user(username: str, password: str, character_class: str) -> bool:
    db = next(get_db())
    try:
        # Check if username already exists
        if db.query(User).filter(User.username == username).first():
            logger.warning(f"Registration failed: Username {username} already exists")
            return False

        # Create new user
        new_user = User(
            username=username,
            password=password,  # In production, use proper password hashing
            character_class=character_class,
            level=1,
            exp=0
        )
        db.add(new_user)
        db.commit()
        logger.info(f"Successfully registered new user: {username}")
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Error during registration: {str(e)}")
        return False
    finally:
        db.close()

def logout_user():
    try:
        username = st.session_state.get('username', 'Unknown')
        for key in st.session_state.keys():
            del st.session_state[key]
        logger.info(f"User {username} logged out successfully")
    except Exception as e:
        logger.error(f"Error during logout: {str(e)}")