import streamlit as st
import pandas as pd
import plotly.express as px
from utils.auth import init_users, login_user, register_user, logout_user
from utils.character import CHARACTER_CLASSES, update_character_exp
from utils.workout import init_workouts, EXERCISE_IMAGES, log_workout, get_user_workouts
from utils.achievements import ACHIEVEMENTS, check_achievements

# Initialize the application
init_users()
init_workouts()

# Apply custom CSS
with open('styles/custom.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Session state initialization
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

def main():
    st.title("🎮 Fitness Quest RPG")
    
    if not st.session_state['logged_in']:
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            st.header("Login")
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            if st.button("Login"):
                if login_user(username, password):
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials!")
        
        with tab2:
            st.header("Register")
            username = st.text_input("Username", key="reg_username")
            password = st.text_input("Password", type="password", key="reg_password")
            
            st.subheader("Choose Your Character Class")
            cols = st.columns(4)
            selected_class = None
            
            for i, (class_name, class_info) in enumerate(CHARACTER_CLASSES.items()):
                with cols[i]:
                    st.image(class_info["image"], caption=class_name)
                    st.write(class_info["description"])
                    if st.button(f"Select {class_name}", key=f"select_{class_name}"):
                        selected_class = class_name
            
            if selected_class and st.button("Register"):
                if register_user(username, password, selected_class):
                    st.success("Registration successful! Please login.")
                else:
                    st.error("Username already exists!")
    
    else:
        # Sidebar with character info
        with st.sidebar:
            st.image(CHARACTER_CLASSES[st.session_state['character_class']]["image"],
                    caption=f"Class: {st.session_state['character_class']}")
            st.header(f"Level {st.session_state['level']}")
            exp_to_next = 1000 - (st.session_state['exp'] % 1000)
            st.progress(1 - (exp_to_next / 1000), f"EXP to next level: {exp_to_next}")
            if st.button("Logout"):
                logout_user()
                st.rerun()
        
        tab1, tab2, tab3 = st.tabs(["Workout", "Progress", "Achievements"])
        
        with tab1:
            st.header("Log Workout")
            exercise = st.selectbox("Choose Exercise", list(EXERCISE_IMAGES.keys()))
            st.image(EXERCISE_IMAGES[exercise], caption=exercise)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                sets = st.number_input("Sets", min_value=1, max_value=10)
            with col2:
                reps = st.number_input("Reps", min_value=1, max_value=100)
            with col3:
                weight = st.number_input("Weight (lbs)", min_value=0, max_value=1000)
            
            if st.button("Log Workout"):
                exp_gained = log_workout(st.session_state['username'], exercise, sets, reps, weight)
                update_character_exp(st.session_state['username'], exp_gained)
                st.success(f"Workout logged! Gained {exp_gained} EXP!")
                st.rerun()
        
        with tab2:
            st.header("Progress Tracking")
            user_workouts = get_user_workouts(st.session_state['username'])
            
            if not user_workouts.empty:
                # Exercise distribution
                fig1 = px.pie(user_workouts, names='exercise', title='Exercise Distribution')
                st.plotly_chart(fig1)
                
                # Progress over time
                fig2 = px.line(user_workouts, x='date', y='weight', color='exercise',
                              title='Weight Progress Over Time')
                st.plotly_chart(fig2)
                
                # Total volume per exercise
                volume = user_workouts.copy()
                volume['total_volume'] = volume['sets'] * volume['reps'] * volume['weight']
                fig3 = px.bar(volume, x='exercise', y='total_volume',
                             title='Total Volume by Exercise')
                st.plotly_chart(fig3)
            else:
                st.info("Start logging workouts to see your progress!")
        
        with tab3:
            st.header("Achievements")
            achieved = check_achievements(st.session_state['username'])
            
            for achievement, details in ACHIEVEMENTS.items():
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.image(details['image'], width=100)
                with col2:
                    if achievement in achieved:
                        st.markdown(f"""
                        <div class="achievement-card">
                            <h3>🏆 {achievement}</h3>
                            <p>{details['description']}</p>
                            <p><strong>Reward: {details['exp_reward']} EXP</strong></p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style="opacity: 0.5">
                            <h3>🔒 {achievement}</h3>
                            <p>{details['description']}</p>
                            <p><strong>Reward: {details['exp_reward']} EXP</strong></p>
                        </div>
                        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
