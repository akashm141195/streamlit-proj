import pandas as pd
from models import get_db, User, Workout
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ACHIEVEMENTS = {
    "Novice Lifter": {
        "description": "Complete your first workout",
        "image": "https://images.unsplash.com/photo-1548126466-4470dfd3a209",
        "exp_reward": 100
    },
    "Consistency King": {
        "description": "Log workouts for 7 consecutive days",
        "image": "https://images.unsplash.com/photo-1571008840902-28bf8f9cd71a",
        "exp_reward": 500
    },
    "Weight Master": {
        "description": "Lift over 200lbs in any exercise",
        "image": "https://images.unsplash.com/photo-1571008592377-e362723e8998",
        "exp_reward": 300
    },
    "Endurance Champion": {
        "description": "Complete 100 total reps in one workout",
        "image": "https://images.unsplash.com/photo-1552035509-b247fe8e5078",
        "exp_reward": 400
    },
    "Workout Warrior": {
        "description": "Complete 50 workouts",
        "image": "https://images.unsplash.com/photo-1548051718-3acad2d13740",
        "exp_reward": 1000
    },
    "Level Master": {
        "description": "Reach level 10",
        "image": "https://images.unsplash.com/photo-1536682984-f6086a5e8004",
        "exp_reward": 2000
    }
}

def check_achievements(username):
    db = next(get_db())
    try:
        # Get user and their workouts from database
        user = db.query(User).filter(User.username == username).first()
        if not user:
            logger.warning(f"User {username} not found")
            return []

        workouts = db.query(Workout).filter(Workout.user_id == user.id).all()
        achieved = []

        # Check each achievement condition
        if workouts:
            achieved.append("Novice Lifter")

        if len(workouts) >= 50:
            achieved.append("Workout Warrior")

        if user.level >= 10:
            achieved.append("Level Master")

        # Check for weight achievement
        if any(workout.weight >= 200 for workout in workouts):
            achieved.append("Weight Master")

        # Check for endurance achievement
        if any((workout.sets * workout.reps) >= 100 for workout in workouts):
            achieved.append("Endurance Champion")

        # Check for consecutive days
        if workouts:
            dates = sorted([workout.date for workout in workouts])
            max_consecutive = 1
            current_consecutive = 1

            for i in range(1, len(dates)):
                if (dates[i] - dates[i-1]).days == 1:
                    current_consecutive += 1
                    max_consecutive = max(max_consecutive, current_consecutive)
                else:
                    current_consecutive = 1

            if max_consecutive >= 7:
                achieved.append("Consistency King")

        logger.info(f"Checked achievements for user {username}. Achieved: {achieved}")
        return achieved

    except Exception as e:
        logger.error(f"Error checking achievements: {str(e)}")
        return []
    finally:
        db.close()