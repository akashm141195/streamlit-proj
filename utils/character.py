import streamlit as st
import pandas as pd

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
    users = pd.read_csv('data/users.csv')
    user_idx = users[users['username'] == username].index[0]
    current_exp = users.loc[user_idx, 'exp']
    new_exp = current_exp + exp_gain
    users.loc[user_idx, 'exp'] = new_exp
    users.loc[user_idx, 'level'] = calculate_level(new_exp)
    users.to_csv('data/users.csv', index=False)
    st.session_state['exp'] = new_exp
    st.session_state['level'] = calculate_level(new_exp)
