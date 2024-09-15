import streamlit as st
from openai import OpenAI

client = OpenAI()

st.title('Personal Dieting Assistant')
st.header("Helping you follow your daily caloric intake and stay fit!")

def call_gpt(system, user):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": system
            },
            {
                "role": "user",
                "content": user
            }
        ]
    )
    return completion.choices[0].message.content

meal_plans = st.text_input("What meals do you want plans for? (e.g., breakfast, lunch, dinner, snacks)")
caloric_intake = st.number_input("How substantial should those meals be calorie-wise?", min_value=0)
ingredients_available = st.text_area("What ingredients do you have available?")
cuisines_liked = st.text_area("What cuisines do you like?")
cooking_difficulty = st.selectbox("What level of cooking difficulty are you willing to spend?", ["Easy", "Medium", "Hard"])

system_prompt = f"""
You are a helpful programming assistant that helps users manage their diet and exercise.

Generate a meal plan based on the following user preferences:
- Meals for: {meal_plans}
- Caloric intake: {caloric_intake} calories per meal
- Ingredients available: {ingredients_available}
- Cuisines liked: {cuisines_liked}
- Cooking difficulty: {cooking_difficulty}

Also, provide feedback on whether they are meeting their nutrition goals and suggest exercises to complement the diet.
"""

user_prompt = "Generate a personalized diet and exercise plan based on the above details."

# Button to run GPT
if st.button('Generate Plan'):
    output = call_gpt(system_prompt, user_prompt)
    st.write('Your Personalized Diet and Exercise Plan:')
    st.write(output)
