import streamlit as st
from models import get_db, User
from sqlalchemy.orm import Session

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
            return True
        return False
    finally:
        db.close()

def register_user(username: str, password: str, character_class: str) -> bool:
    db = next(get_db())
    try:
        if db.query(User).filter(User.username == username).first():
            return False

        new_user = User(
            username=username,
            password=password,  # In production, use proper password hashing
            character_class=character_class,
            level=1,
            exp=0
        )
        db.add(new_user)
        db.commit()
        return True
    except:
        db.rollback()
        return False
    finally:
        db.close()

def logout_user():
    for key in st.session_state.keys():
        del st.session_state[key]