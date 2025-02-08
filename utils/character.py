import streamlit as st
from models import get_db, User
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CHARACTER_CLASSES = {
    "Warrior": {
        "image": "https://images.unsplash.com/photo-1524373050940-8f19e9b858a9",
        "description": "Specializes in strength training and heavy lifting"
    },
    "Rogue": {
        "image": "https://images.unsplash.com/photo-1548445929-4f60a497f851",
        "description": "Focuses on agility and cardio exercises"
    },
    "Mage": {
        "image": "https://images.unsplash.com/photo-1432958576632-8a39f6b97dc7",
        "description": "Masters of flexibility and mind-body connection"
    },
    "Paladin": {
        "image": "https://images.unsplash.com/photo-1514539079130-25950c84af65",
        "description": "Balanced training with focus on endurance"
    }
}

def calculate_level(exp):
    return 1 + (exp // 1000)

def update_character_exp(username, exp_gain):
    db = next(get_db())
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            logger.error(f"User {username} not found")
            return

        new_exp = user.exp + exp_gain
        user.exp = new_exp
        user.level = calculate_level(new_exp)
        db.commit()

        # Update session state
        st.session_state['exp'] = new_exp
        st.session_state['level'] = calculate_level(new_exp)
        logger.info(f"Updated experience for user {username}: +{exp_gain} EXP, Level {user.level}")
    except Exception as e:
        logger.error(f"Error updating character experience: {str(e)}")
        db.rollback()
    finally:
        db.close()