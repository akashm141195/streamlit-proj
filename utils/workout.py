import streamlit as st
from models import get_db, Workout
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
    db = next(get_db())
    try:
        exp_gained = calculate_exp(sets, reps, weight)
        new_workout = Workout(
            user_id=st.session_state['user_id'],
            exercise=exercise,
            sets=sets,
            reps=reps,
            weight=weight,
            exp_gained=exp_gained
        )
        db.add(new_workout)
        db.commit()
        logger.info(f"Logged workout for user {username}: {exercise}, {sets}x{reps} at {weight}lbs")
        return exp_gained
    except Exception as e:
        logger.error(f"Error logging workout: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

def calculate_exp(sets: int, reps: int, weight: float) -> int:
    return int((sets * reps * weight) / 10)

def get_user_workouts(username: str) -> list:
    db = next(get_db())
    try:
        workouts = db.query(Workout).filter(
            Workout.user_id == st.session_state['user_id']
        ).all()

        if not workouts:
            logger.info(f"No workouts found for user {username}")
            return []

        workout_list = []
        for w in workouts:
            workout_list.append({
                'date': w.date,
                'exercise': w.exercise,
                'sets': w.sets,
                'reps': w.reps,
                'weight': w.weight,
                'exp_gained': w.exp_gained
            })

        logger.info(f"Retrieved {len(workout_list)} workouts for user {username}")
        return workout_list
    except Exception as e:
        logger.error(f"Error retrieving workouts: {str(e)}")
        return []
    finally:
        db.close()