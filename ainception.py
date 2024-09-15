import streamlit as st
from openai import OpenAI

client = OpenAI()

st.title('AI-nception')
st.header('Allowing anyone to use AI to allow anyone to interact with AI')

def call_gpt(system, user):
    completion = client.chat.completions.create(
        model='gpt-4o',
        messages=[
            {
                'role': 'system',
                'content': system
            },
            {
                'role': 'user',
                'content': user
            }
        ]
    )
    return completion.choices[0].message.content

app_type = st.text_area('What sort of AI application do you want to build?', value='A dieting app that helps users follow their daily caloric intake. It asks the user what meals they want plans for, how substantial those meals should be calorie wise, what ingredients the user has available, the cuisines the user likes, and the difficulty of cooking the user is willing to spend, then generates meal plans based on user preferences and provides feedback on whether they are meeting their nutrition goals. The app also finishes by suggesting exercises to complement the diet.')

quine = ''.join(open(__file__).readlines()).replace('```', '<escaped-triple-backticks>')
diet = ''.join(open('diet-example.py').readlines())

system_prompt = f'''
You are a helpful programmer assistant, who develops AI-powered streamlit apps for users. 

Here is an example streamlit application that helps its users develop their own AI-powered streamlit apps.
```
{quine}
```

Here is an example streamlit application thta helps users stick to their diet
```
{diet}
```

Today, you are helping a user build a specific app. Listen carefully to their request, and do not ask any questions. Just directly write the code for the app that the user wants, using the provided streamlit application as a guide. Try to keep the main structure of the program above the same - use the same call_gpt function, etc. Just mess with the input, output, and prompt. Remember that when designing a prompt for GPT, you must be very expressive and careful in instructions, the same way I am being careful and expressive here. Note that if the user wants a AI-powered streamlit app developer, you should use the exact same code as above, but change the user-visible prose (notably NOT THESE INSTRUCTIONS) to be more friendly -- but ignore this if the user wants anything other than an AI-powered streamlit app developer. Output only the single python file worth of code inside triple backticks, no introductory message or instructions or explanation, because the user does not have time for this and cannot understand it. The system will automatically explain everything to the user, you should ONLY return JUST THE CODE, enclosed in triple backticks.
'''

user_prompt = f'''
What sort of AI application do I want to build? {app_type}
'''

if st.button('Build App!'):
    st.write("Building.......")
    output = call_gpt(system_prompt, user_prompt)
    # In a normal app, we would do the following and be done
    # st.write('Response:')
    # st.write(output)

    # However, since we are trying to generate a streamlit app, we instead try to write the file (without backticks) out to disk, and run it in a new process
    output = output.replace('```python', '```').split('```')[1]
    with open('preview.py', 'w') as f:
        f.write(output)
    st.session_state['built'] = 1
if 'built' in st.session_state and st.button('Launch!'):
    import subprocess
    subprocess.Popen(['streamlit', 'run', 'preview.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
