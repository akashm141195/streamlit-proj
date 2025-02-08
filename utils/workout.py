import streamlit as st
import pandas as pd
import os
from datetime import datetime

def init_workouts():
    if not os.path.exists('data'):
        os.makedirs('data')
    if not os.path.exists('data/workouts.csv'):
        df = pd.DataFrame(columns=['username', 'date', 'exercise', 'sets', 'reps', 'weight', 'exp_gained'])
        df.to_csv('data/workouts.csv', index=False)

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

def log_workout(username, exercise, sets, reps, weight):
    workouts = pd.read_csv('data/workouts.csv')
    exp_gained = calculate_exp(sets, reps, weight)
    
    new_workout = pd.DataFrame({
        'username': [username],
        'date': [datetime.now().strftime('%Y-%m-%d')],
        'exercise': [exercise],
        'sets': [sets],
        'reps': [reps],
        'weight': [weight],
        'exp_gained': [exp_gained]
    })
    
    workouts = pd.concat([workouts, new_workout], ignore_index=True)
    workouts.to_csv('data/workouts.csv', index=False)
    return exp_gained

def calculate_exp(sets, reps, weight):
    return int((sets * reps * weight) / 10)

def get_user_workouts(username):
    workouts = pd.read_csv('data/workouts.csv')
    return workouts[workouts['username'] == username]
