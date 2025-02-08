import pandas as pd

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
    workouts = pd.read_csv('data/workouts.csv')
    user_workouts = workouts[workouts['username'] == username]
    users = pd.read_csv('data/users.csv')
    user = users[users['username'] == username].iloc[0]
    
    achieved = []
    
    # Check each achievement condition
    if len(user_workouts) >= 1:
        achieved.append("Novice Lifter")
    
    if len(user_workouts) >= 50:
        achieved.append("Workout Warrior")
    
    if user['level'] >= 10:
        achieved.append("Level Master")
    
    if (user_workouts['weight'] >= 200).any():
        achieved.append("Weight Master")
    
    if (user_workouts['sets'] * user_workouts['reps']).max() >= 100:
        achieved.append("Endurance Champion")
    
    # Check for consecutive days
    if not user_workouts.empty:
        dates = pd.to_datetime(user_workouts['date']).sort_values()
        max_consecutive = 1
        current_consecutive = 1
        for i in range(1, len(dates)):
            if (dates.iloc[i] - dates.iloc[i-1]).days == 1:
                current_consecutive += 1
                max_consecutive = max(max_consecutive, current_consecutive)
            else:
                current_consecutive = 1
        
        if max_consecutive >= 7:
            achieved.append("Consistency King")
    
    return achieved
