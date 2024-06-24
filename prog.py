import streamlit as st
import time  # Import time module for simulating delay
import matplotlib.pyplot as plt

# Constants for step calculation
STEPS_PER_MILE_WALKING = 2000  # Average steps per mile for walking
CALORIES_PER_STEP_WALKING = 0.05  # Calories burned per step for walking
STEPS_PER_MILE_RUNNING = 1500  # Average steps per mile for running
CALORIES_PER_STEP_RUNNING = 0.1  # Calories burned per step for running

def calculate_bmr(weight, height, age, gender):
    gender_lower = gender.lower()  # Convert to lowercase

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

def main():
    st.title('Weight Loss Goal Calculator')

    weight = st.number_input('Enter your current weight (kg)')
    desired_weight = st.number_input('Enter your desired weight (kg)')
    
    height_unit = st.radio('Select height unit', ('Centimeters', 'Inches'))
    if height_unit == 'Centimeters':
        height_cm = st.number_input('Enter your height (cm)')
        height_inches = height_cm / 2.54
    else:
        height_inches = st.number_input('Enter your height (inches)')
        height_cm = height_inches * 2.54

    age = st.number_input('Enter your age (years)')
    gender = st.radio('Select your gender', ('Male', 'Female'))
    activity_level = st.selectbox('Select your activity level', ('Sedentary', 'Lightly Active', 'Moderately Active', 'Very Active', 'Extra Active'))
    goal = st.selectbox('Select your goal', ('Lose Weight', 'Maintain Weight', 'Gain Weight'))
    exercise_type = st.radio('Select exercise type', ('Walking', 'Running'))

    if st.button('Calculate'):
        with st.spinner('Calculating...'):
            try:
                st.write('Calculating your weight loss plan...')

                gender_lower = gender.lower()  # Convert to lowercase
                activity_level_lower = activity_level.lower().replace(' ', '_')  # Convert to lowercase and replace spaces
                goal_lower = goal.lower().replace(' ', '_')  # Convert to lowercase and replace spaces

                bmr = calculate_bmr(weight, height_cm, age, gender_lower)
                tdee = calculate_tdee(bmr, activity_level_lower)
                calorie_intake = calculate_calorie_intake(tdee, goal_lower)
                calories_to_burn_per_day = tdee - calorie_intake  # Caloric deficit per day

                if calories_to_burn_per_day <= 0:
                    st.error("Error: Your current goal doesn't involve weight loss. Please select 'Lose Weight' goal.")
                    return

                # Calculate miles to walk or run per day
                if exercise_type == 'Walking':
                    steps_per_mile = STEPS_PER_MILE_WALKING
                    calories_per_step = CALORIES_PER_STEP_WALKING
                else:
                    steps_per_mile = STEPS_PER_MILE_RUNNING
                    calories_per_step = CALORIES_PER_STEP_RUNNING

                miles_per_day = calculate_miles_to_exercise(calories_to_burn_per_day, steps_per_mile, calories_per_step)
                time_to_goal_days = calculate_time_to_goal((weight - desired_weight) * 7700, calories_to_burn_per_day)
                bmi = calculate_bmi(weight, height_cm)

                st.success('Calculation completed!')
                st.subheader('Weight Loss Plan:')
                st.write(f'Your recommended daily calorie intake: {calorie_intake:.2f} calories')
                st.write(f'Miles to {goal.replace("_", " ")} weight: {miles_per_day:.2f} miles per day')
                st.write(f'Calories to burn per day: {calories_to_burn_per_day:.2f} calories')
                st.write(f'Estimated time to achieve goal: {time_to_goal_days:.1f} days')
                st.write(f'Your BMI: {bmi:.2f}')

                # Progress Tracker
                st.subheader('Track Your Progress:')
                st.write('Enter your weight at regular intervals to track your progress.')

                if 'weights' not in st.session_state:
                    st.session_state.weights = []
                if 'dates' not in st.session_state:
                    st.session_state.dates = []

                date = st.date_input('Date')
                current_weight = st.number_input('Current weight (kg)', value=weight, step=0.1)

                if st.button('Add Entry'):
                    st.session_state.weights.append(current_weight)
                    st.session_state.dates.append(date)
                    st.success('Entry added!')

                if st.session_state.weights:
                    st.line_chart({
                        'Weight': st.session_state.weights,
                        'Date': st.session_state.dates
                    })

            except ValueError as e:
                st.error(f"Error: {str(e)}")

if __name__ == '__main__':
    main()
