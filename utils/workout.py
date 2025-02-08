import streamlit as st
from models import add_workout, get_user_workouts
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

EXERCISE_IMAGES = {
    "Bench Press": "https://images.unsplash.com/photo-1616994051378-8e3a64147f56",
    "Squats": "https://images.unsplash.com/photo-1518611012118-696072aa579a",
    "Deadlift": "https://images.unsplash.com/photo-1541534741688-6078c6bfb5c5",
    "Pull-ups": "https://images.unsplash.com/photo-1518459031867-a89b944bffe4",
    "Push-ups": "https://images.unsplash.com/photo-1486739985386-d4fae04ca6f7",
    "Running": "https://images.unsplash.com/photo-1483721310020-03333e577078",
    "Rowing": "https://images.unsplash.com/photo-1476480862126-209bfaa8edc8",
    "Planks": "https://images.unsplash.com/photo-1517130038641-a774d04afb3c"
}

def init_workouts():
    pass

def log_workout(username: str, exercise: str, sets: int, reps: int, weight: float) -> int:
    try:
        exp_gained = calculate_exp(sets, reps, weight)
        add_workout(username, exercise, sets, reps, weight, exp_gained)
        logger.info(f"Logged workout for user {username}: {exercise}, {sets}x{reps} at {weight}lbs")
        return exp_gained
    except Exception as e:
        logger.error(f"Error logging workout: {str(e)}")
        raise

def calculate_exp(sets: int, reps: int, weight: float) -> int:
    return int((sets * reps * weight) / 10)

def get_workouts(username: str):
    try:
        workouts = get_user_workouts(username)
        if workouts.empty: # Assuming get_user_workouts returns an object with an empty property
            logger.info(f"No workouts found for user {username}")
            return []
        logger.info(f"Retrieved {len(workouts)} workouts for user {username}")
        return workouts
    except Exception as e:
        logger.error(f"Error retrieving workouts: {str(e)}")
        return []