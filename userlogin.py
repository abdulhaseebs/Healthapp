import streamlit as st
import hashlib
import pandas as pd
import os

# Constants for step calculation
STEPS_PER_MILE_WALKING = 2000  # Average steps per mile for walking
CALORIES_PER_STEP_WALKING = 0.05  # Calories burned per step for walking
STEPS_PER_MILE_RUNNING = 1500  # Average steps per mile for running
CALORIES_PER_STEP_RUNNING = 0.1  # Calories burned per step for running

# File to store user data
USER_DATA_FILE = 'users.csv'


def calculate_bmr(weight, height, age, gender):
    gender_lower = gender.lower()# Convert to lowercase

    if gender_lower == 'male':
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    elif gender_lower == 'female':
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    else:
        raise ValueError("Invalid gender")

    return bmr


def calculate_tdee(bmr, activity_level):
    activity_factors = {
        'sedentary': 1.2,
        'lightly_active': 1.375,
        'moderately_active': 1.55,
        'very_active': 1.725,
        'extra_active': 1.9
    }
    return bmr * activity_factors[activity_level]


def calculate_calorie_intake(tdee, goal):
    goals = {
        'lose_weight': tdee - 500,
        'maintain_weight': tdee,
        'gain_weight': tdee + 500
    }
    return goals[goal]


def calculate_miles_to_exercise(calories_to_burn, steps_per_mile, calories_per_step):
    steps_per_day = calories_to_burn / calories_per_step
    miles_per_day = steps_per_day / steps_per_mile
    return miles_per_day


def calculate_time_to_goal(calories_to_burn, deficit_calories_per_day):
    days_to_goal = calories_to_burn / deficit_calories_per_day
    return days_to_goal


def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100  # Convert height to meters
    bmi = weight / (height_m ** 2)
    return bmi


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def load_users():
    if os.path.exists(USER_DATA_FILE):
        return pd.read_csv(USER_DATA_FILE)
    else:
        return pd.DataFrame(columns=['username', 'password'])


def save_user(username, password):
    users = load_users()
    hashed_password = hash_password(password)
    new_user = pd.DataFrame([[username, hashed_password]], columns=['username', 'password'])
    users = pd.concat([users, new_user], ignore_index=True)
    users.to_csv(USER_DATA_FILE, index=False)


def user_exists(username):
    users = load_users()
    return not users[users['username'] == username].empty


def validate_user(username, password):
    users = load_users()
    hashed_password = hash_password(password)
    user = users[(users['username'] == username) &
                 (users['password'] == hashed_password)]
    return not user.empty


def registration():
    st.header('Register')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    confirm_password = st.text_input('Confirm Password', type='password')

    if st.button('Register'):
        if password != confirm_password:
            st.error('Passwords do not match')
        elif user_exists(username):
            st.error('Username already exists')
        else:
            save_user(username, password)
            st.success('You have successfully registered! Please log in.')


def login():
    st.header('Login')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    if st.button('Login'):
        if validate_user(username, password):
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.success(f'Welcome {username}!')
            st.experimental_rerun()  # Force a rerun to reflect the login status immediately
        else:
            st.error('Invalid username or password')


def weight_loss_calculator():
    st.title('Weight Loss Goal Calculator')

    weight = st.number_input('Enter your current weight (kg)')
    desired_weight = st.number_input('Enter your desired weight (kg)')
    
    height_unit = st.selectbox('Select height unit', ['Centimeters', 'Inches'])
    if height_unit == 'Centimeters':
        height_cm = st.number_input('Enter your height (cm)')
    else:
        height_inches = st.number_input('Enter your height (inches)')
        height_cm = height_inches * 2.54

    age = st.number_input('Enter your age (years)')
    gender = st.radio('Select your gender', ('Male', 'Female'))
    activity_level = st.selectbox('Select your activity level',
                                  ('Sedentary', 'Lightly Active', 'Moderately Active',
                                   'Very Active', 'Extra Active'))
    goal = st.selectbox('Select your goal',
                        ('Lose Weight', 'Maintain Weight', 'Gain Weight'))
    exercise_type = st.radio('Select exercise type', ('Walking', 'Running'))

    if st.button('Calculate'):
        with st.spinner('Calculating...'):
            try:
                st.write('Calculating your weight loss plan...')

                gender_lower = gender.lower() # Convert to lowercase
                activity_level_lower = activity_level.lower().replace(' ', '_')
                goal_lower = goal.lower().replace(' ', '_')

                
                bmr = calculate_bmr(weight, height_cm, age, gender_lower)
                tdee = calculate_tdee(bmr, activity_level_lower)
                calorie_intake = calculate_calorie_intake(tdee, goal_lower)
                calories_to_burn_per_day = tdee - calorie_intake  # Caloric deficit per day

                if calories_to_burn_per_day <= 0:
                    st.error("Error: Your current goal doesn't involve weight loss. "
                             "Please select 'Lose Weight' goal.")
                    return

                if exercise_type == 'Walking':
                    steps_per_mile = STEPS_PER_MILE_WALKING
                    calories_per_step = CALORIES_PER_STEP_WALKING
                else:
                    steps_per_mile = STEPS_PER_MILE_RUNNING
                    calories_per_step = CALORIES_PER_STEP_RUNNING

                miles_per_day = calculate_miles_to_exercise(calories_to_burn_per_day,
                                                            steps_per_mile, calories_per_step)
                time_to_goal_days = calculate_time_to_goal((weight - desired_weight) * 7700,
                                                           calories_to_burn_per_day)

                st.success('Calculation completed!')
                st.subheader('Weight Loss Plan:')
                st.write(f'Your recommended daily calorie intake: {calorie_intake:.2f} calories')
                st.write(f'Miles to walk/run per day to achieve your goal: {miles_per_day:.2f} miles per day')
                st.write(f'Estimated time to achieve goal: {time_to_goal_days:.1f} days')
                st.write(f'Calories to burn per day: {calories_to_burn_per_day:.2f} calories')

            except ValueError as e:
                st.error(f"Error: {str(e)}")


def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if st.session_state['logged_in']:
        if st.sidebar.button('Logout'):
            st.session_state['logged_in'] = False
            st.experimental_rerun()  # Force a rerun to reflect the logout status immediately
        weight_loss_calculator()
    else:
        option = st.sidebar.selectbox('Menu', ['Login', 'Register'])
        if option == 'Login':
            login()
        elif option == 'Register':
            registration()


if __name__ == '__main__':
    main()
