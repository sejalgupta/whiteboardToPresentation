# import openai
import os
import requests
from ..config import OPENAI_API_KEY
import json

def get_prompt(role, presentation_context, presentation_length, example_presentation):
    # PROVIDE CONTEXT
    prompt = f"I am a {role}. Can you please provide a slide by slide structure for a {presentation_length} presentation?"

    # ADD IN AUDIO
    prompt += f"Here is a summary of the meeting with relevant content we want to incorporate: {presentation_context}"
    
    # CONSTRAINTS FOR EACH TYPE OF SLIDE
    prompt += "Here are the types of slides and the information that they need: - TITLE_SLIDE: 1 title, 1 subtitle \n - TITLE_AND_CONTENT_SLIDE: 1 title, 1 content \n- COMPARISON: 1 title, 2 subtitles, 2 contents \n- TWO_CONTENT: 1 title, 2 contents \n- SECTION_HEADER: 1 title, 1 subtitle \n- TITLE_ONLY: 1 title \n- BLANK: 1 title \n- CONTENT_WITH_CAPTION: 1 title, 1 subtitle, 1 content \n- PICTURE_WITH_CAPTION: 1 title, 1 subtitle, 1 picture"    
    
    # REQUEST JSON FORMAT
    prompt += "The slideshow should be provided in a JSON format like in the example below. Each slide should be formatted as a dictionary with "

    # FORMAT OF THE INFORMATION
    prompt += "\"layout\": REQUIRED and chosen from 'TITLE_SLIDE', \"TITLE_AND_CONTENT_SLIDE\", \"COMPARISON\", \"TWO_CONTENT\", \"SECTION_HEADER\", \"TITLE_ONLY\", \"BLANK\", \"CONTENT_WITH_CAPTION\", \"PICTURE_WITH_CAPTION\"]"
    prompt += "\"title\": REQUIRED in list format"
    prompt += "\"subtitle\": REQUIRED DEPENDING ON TYPE OF SLIDE in list format with each element being a different subtitle"
    prompt += "\"picture\": REQUIRED PICTURE DEPENDING ON TYPE OF SLIDE in a list of image paths"
    prompt += "\"content\": CONTENT DEPENDING ON TYPE OF SLIDE in a list of dictionarys format with each element being a different content. each dictionary should have the type which is image or text and the information in a \"image\" key or \"text\" key"
    
    # EXAMPLE PRESENTATION
    prompt += f"Here is an example presentation to follow {example_presentation}"

    return prompt

def get_metadata_gpt(role, presentation_context, presentation_length):
    this_folder = os.path.dirname(os.path.abspath(__file__))
    content_file = os.path.join(this_folder, "./json/example_presentation.json")
    example_presentation = open(content_file)
    prompt = get_prompt(role, presentation_context, presentation_length, example_presentation)

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
    presentation_length = "10-minute"

    answers = get_metadata_gpt(role, presentation_context, presentation_length)
    response = answers["choices"][0]["message"]["content"]
    
    prompt = json.loads(response)

    with open('data.json', 'w') as f:
        json.dump(prompt, f)