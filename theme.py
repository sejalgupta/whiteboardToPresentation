import json
import requests
from presentation_theme import PresentationTheme
from utils import OPENAI_API_KEY

def theme_prompt(role, presentation_context):
    prompt = f"{role} {presentation_context} Can you provide the best background color, title color, text_color, and font type for my presentation? Please provide the output as only JSON format. Here is an example of an output where colors are represented as a list of RGB values:"
    prompt += "{\"background_color\":  [255, 223, 186], \"title\": { \"color\": [0, 51, 102], \"size\":40, \"font\":Arial }, \"body\": { \"color\": [0, 0, 0], \"size\":24, \"font\": Georgia }}"
    return prompt

def get_theme_gpt(role, presentation_context):
    prompt = theme_prompt(role, presentation_context)

    answers = None

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    payload = {
        "model": "gpt-4-1106-preview",
        "response_format": {
            "type": "json_object"
        },
        "messages": [
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": prompt
                },
            ],
            }
        ],
        "max_tokens": 1000
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    # Check if the response is successful
    if response.status_code == 200:
        # Parse the response as JSON
        answers = response.json()
    else:
        # Handle errors (non-200 responses)
        print(f"Error: {response.status_code} - {response.text}")

    return answers

if __name__ == "__main__":
    role = "teacher for sixth grade math"
    presentation_context = "I am trying to teach about multiplying fractions. I need to create a lesson plan for tomorrow."

    answers = get_theme_gpt(role, presentation_context)
    response = answers["choices"][0]["message"]["content"]
    
    prompt_answer = json.loads(response)

    with open('data.json', 'w') as f:
        json.dump(prompt_answer, f)

    theme = PresentationTheme(prompt_answer)