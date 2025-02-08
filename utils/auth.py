import streamlit as st
import pandas as pd
import os
from pathlib import Path

def init_users():
    if not os.path.exists('data'):
        os.makedirs('data')
    if not os.path.exists('data/users.csv'):
        df = pd.DataFrame(columns=['username', 'password', 'character_class', 'level', 'exp'])
        df.to_csv('data/users.csv', index=False)

def login_user(username, password):
    users = pd.read_csv('data/users.csv')
    user = users[users['username'] == username]
    if not user.empty and user.iloc[0]['password'] == password:
        st.session_state['logged_in'] = True
        st.session_state['username'] = username
        st.session_state['character_class'] = user.iloc[0]['character_class']
        st.session_state['level'] = user.iloc[0]['level']
        st.session_state['exp'] = user.iloc[0]['exp']
        return True
    return False

def register_user(username, password, character_class):
    users = pd.read_csv('data/users.csv')
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
    users.to_csv('data/users.csv', index=False)
    return True

def logout_user():
    for key in st.session_state.keys():
        del st.session_state[key]
