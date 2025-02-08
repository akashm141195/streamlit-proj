import pandas as pd
from datetime import datetime
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# File paths
USERS_FILE = "data/users.csv"
WORKOUTS_FILE = "data/workouts.csv"

def read_users():
    try:
        if os.path.exists(USERS_FILE):
            return pd.read_csv(USERS_FILE)
        return pd.DataFrame(columns=['username', 'password', 'character_class', 'level', 'exp'])
    except Exception as e:
        logger.error(f"Error reading users file: {str(e)}")
        return pd.DataFrame(columns=['username', 'password', 'character_class', 'level', 'exp'])

def read_workouts():
    try:
        if os.path.exists(WORKOUTS_FILE):
            return pd.read_csv(WORKOUTS_FILE)
        return pd.DataFrame(columns=['username', 'date', 'exercise', 'sets', 'reps', 'weight', 'exp_gained'])
    except Exception as e:
        logger.error(f"Error reading workouts file: {str(e)}")
        return pd.DataFrame(columns=['username', 'date', 'exercise', 'sets', 'reps', 'weight', 'exp_gained'])

def save_users(df):
    try:
        df.to_csv(USERS_FILE, index=False)
        logger.info("Successfully saved users data")
    except Exception as e:
        logger.error(f"Error saving users file: {str(e)}")

def save_workouts(df):
    try:
        df.to_csv(WORKOUTS_FILE, index=False)
        logger.info("Successfully saved workouts data")
    except Exception as e:
        logger.error(f"Error saving workouts file: {str(e)}")

def get_user(username):
    users = read_users()
    return users[users['username'] == username].iloc[0] if not users[users['username'] == username].empty else None

def add_user(username, password, character_class):
    users = read_users()
    if username in users['username'].values:
        return False
    new_user = pd.DataFrame({
        'username': [username],
        'password': [password],
        'character_class': [character_class],
        'level': [1],
        'exp': [0]
    })
    users = pd.concat([users, new_user], ignore_index=True)
    save_users(users)
    return True

def update_user_exp(username, exp_gain):
    users = read_users()
    user_idx = users.index[users['username'] == username].tolist()[0]
    users.loc[user_idx, 'exp'] += exp_gain
    users.loc[user_idx, 'level'] = 1 + (users.loc[user_idx, 'exp'] // 1000)
    save_users(users)
    return users.loc[user_idx, 'exp'], users.loc[user_idx, 'level']

def add_workout(username, exercise, sets, reps, weight, exp_gained):
    workouts = read_workouts()
    new_workout = pd.DataFrame({
        'username': [username],
        'date': [datetime.now().date()],
        'exercise': [exercise],
        'sets': [sets],
        'reps': [reps],
        'weight': [weight],
        'exp_gained': [exp_gained]
    })
    workouts = pd.concat([workouts, new_workout], ignore_index=True)
    save_workouts(workouts)

def get_user_workouts(username):
    workouts = read_workouts()
    return workouts[workouts['username'] == username]