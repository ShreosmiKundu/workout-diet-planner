import os
import random
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_workout(goal):
    plans = {
        "Weight Loss": [
            "Mon: Cardio 30 min", "Tue: Squats + Push-ups", "Wed: Rest",
            "Thu: Cardio 30 min", "Fri: Lunges + Pull-ups", "Sat: Yoga", "Sun: Rest"
        ],
        "Muscle Gain": [
            "Mon: Chest + Triceps", "Tue: Back + Biceps", "Wed: Legs",
            "Thu: Shoulders", "Fri: Full Body", "Sat: Cardio", "Sun: Rest"
        ],
        "Maintenance": [
            "Mon: 20 min Walk", "Tue: 15 Push-ups + 15 Squats", "Wed: Rest",
            "Thu: 20 min Jog", "Fri: Stretching", "Sat: 15 min Walk", "Sun: Rest"
        ]
    }
    return plans.get(goal, plans["Maintenance"])

def generate_diet(diet_pref):
    plans = {
        "Vegan": {
            "Breakfast": "Oatmeal + Fruits",
            "Lunch": "Veggie Salad + Lentils",
            "Dinner": "Tofu Stir Fry + Rice"
        },
        "Vegetarian": {
            "Breakfast": "Eggs + Toast",
            "Lunch": "Paneer Salad + Chapati",
            "Dinner": "Veg Curry + Rice"
        },
        "Non-Veg": {
            "Breakfast": "Eggs + Toast",
            "Lunch": "Chicken Salad + Rice",
            "Dinner": "Grilled Fish + Veggies"
        }
    }
    return plans.get(diet_pref, plans["Non-Veg"])

def create_schedule(workout):
    week_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    return pd.DataFrame({"Day": week_days, "Workout": workout})

def get_motivation():
    msgs = [
        "🌟 Consistency is key! Just start today!",
        "🔥 Push yourself because no one else is going to do it for you!",
        "⚠ Rest days matter too – recovery builds strength!",
        "💥 Every small effort counts – keep going!",
        "✨ Believe in yourself and your journey!"
    ]
    return random.choice(msgs)

def get_gemini_motivation():
    if not GEMINI_API_KEY:
        return "💡 Stay consistent, stay strong! (API key missing)"

    try:
        
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-latest:generateText"
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": GEMINI_API_KEY
        }
        data = {
            "prompt": "Give me a short, powerful motivational fitness quote.",
            "temperature": 0.8,
            "maxOutputTokens": 50
        }

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        text = result.get("candidates", [{}])[0].get("output", "")
        if not text:
            raise ValueError("No text returned from API")
        return text.strip()

    except Exception as e:
        fallback = [
            "💡 Stay consistent, stay strong!",
            "💡 Every workout counts!",
            "💡 Push your limits today!"
        ]
        return random.choice(fallback)

def adjust_workout_for_bmi(workout, bmi):
    if bmi < 18.5:  
        workout = [w + " + Extra Protein Meal" if "Rest" not in w else w for w in workout]
    elif bmi >= 25:  
        workout = [w + " (Light)" if "Rest" not in w else w for w in workout]
    return workout

def adjust_diet_for_bmi(diet, bmi):
    new_diet = diet.copy()
    if bmi < 18.5:
        new_diet = {meal: menu + " + Nuts & Protein Shake" for meal, menu in diet.items()}
    elif bmi >= 25:
        new_diet = {meal: menu + " (Low Calorie)" for meal, menu in diet.items()}
    return new_diet

def weekly_calories():
    return [200, 250, 0, 220, 300, 180, 0]

def get_quote():
    quotes = [
        "💡 The body achieves what the mind believes.",
        "💡 Push yourself, because no one else is going to do it for you.",
        "💡 Don’t limit your challenges, challenge your limits.",
        "💡 One workout at a time, one meal at a time.",
    ]
    return random.choice(quotes)
