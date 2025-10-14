import streamlit as st
import pandas as pd
from backend import (
    generate_workout,
    generate_diet,
    create_schedule,
    get_motivation,
    get_gemini_motivation,
    weekly_calories,
    get_quote
)

st.set_page_config(
    page_title="Personalized Workout & Diet Planner",
    layout="wide",
    page_icon="💪"
)

dark_mode = st.sidebar.toggle("🌙 Dark Mode", value=True)

if dark_mode:
    bg_color = "#0E1117"
    text_color = "#E0E0E0"
    card_bg = "#1E1E1E"
    input_bg = "#2A2A2A"
    card_text_color = "#E0E0E0"
else:
    bg_color = "#FFFFFF"
    text_color = "#000000"
    card_bg = "#F8F8F8"
    input_bg = "#F7F3F3"
    card_text_color = "#000000"

st.markdown(f"""
<style>
    body {{
        background-color: {bg_color};
        color: {text_color};
    }}
    .stButton>button {{
        background-color: #FF4B4B;
        color: white;
        border-radius: 12px;
        padding: 8px 16px;
        border: none;
    }}
    .card {{
        background-color: {card_bg};
        color: {card_text_color};
        padding: 20px;
        border-radius: 15px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.15);
        margin-bottom: 20px;
    }}
    .stTextInput>div>div>input, .stNumberInput>div>div>input {{
        background-color: {input_bg};
        color: {text_color};
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
    }}
    th, td {{
        text-align: left;
        padding: 8px;
        color: {card_text_color};
    }}
    th {{
        background-color: #FF4B4B;
        color: white;
    }}
</style>
""", unsafe_allow_html=True)

st.sidebar.header("📝 Your Details")
name = st.sidebar.text_input("Name")
age = st.sidebar.number_input("Age", min_value=10, max_value=100, value=25)
weight = st.sidebar.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
height = st.sidebar.number_input("Height (cm)", min_value=100, max_value=250, value=170)
diet_pref = st.sidebar.selectbox("🥗 Diet Preference", ["Vegan", "Vegetarian", "Non-Veg"])
st.sidebar.markdown("---")

bmi = weight / ((height/100) ** 2)
if bmi < 18.5:
    bmi_status = "Underweight"
    recommended_goal = "Muscle Gain"
elif 18.5 <= bmi < 25:
    bmi_status = "Normal weight"
    recommended_goal = "Maintenance"
elif 25 <= bmi < 30:
    bmi_status = "Overweight"
    recommended_goal = "Weight Loss"
else:
    bmi_status = "Obese"
    recommended_goal = "Weight Loss"

st.sidebar.markdown(f"**BMI:** {bmi:.1f} ({bmi_status})")
st.sidebar.markdown(f"**Recommended Goal:** {recommended_goal}")

goal = st.sidebar.selectbox(
    "🏋 Fitness Goal", 
    ["Weight Loss", "Muscle Gain", "Maintenance"], 
    index=["Weight Loss", "Muscle Gain", "Maintenance"].index(recommended_goal)
)

generate_plans = st.sidebar.button("Generate Workout & Diet")

st.title("💪 Personalized Workout & Diet Planner")
st.subheader(f"Welcome {name if name else 'Fitness Enthusiast'} 👋")
st.markdown(f"💡 {get_quote()}")
st.markdown("---")

if generate_plans:
   
    workout_plan = generate_workout(goal)
    diet_plan = generate_diet(diet_pref)
    schedule = create_schedule(workout_plan)
    calories = weekly_calories()

    st.header("🏋 Workout Plan")
    st.markdown(f'<div class="card">{schedule.to_html(index=False)}</div>', unsafe_allow_html=True)

    st.header("🥗 Diet Plan")
    diet_df = pd.DataFrame(diet_plan.items(), columns=["Meal", "Menu"])
    st.markdown(f'<div class="card">{diet_df.to_html(index=False)}</div>', unsafe_allow_html=True)

    st.header("🔥 Weekly Calories (Example)")
    st.bar_chart(calories)

    st.header("💬 Motivation Boost")
    st.markdown(f'<div class="card">{get_motivation()}</div>', unsafe_allow_html=True)

    with st.spinner("Fetching Gemini AI quote..."):
        gemini_quote = get_gemini_motivation()
    st.markdown(f'<div class="card">{gemini_quote}</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("Made with ❤ by Your Name | Powered by Gemini AI")
