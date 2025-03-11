from openai import OpenAI, api_key
from . import prompt
from openai_secret import API_KEY #create a python file called secret.py and add ur own API key
import requests
import re
import base64
import os

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def getGPTresponse(persona="Peter Griffin"):
    # Construct the prompt
    client = OpenAI(api_key = API_KEY)

    user_prompt = []
    user_prompt.append({'type': 'text', 'text' : prompt.basic_prompt})
    for file in os.listdir():
        if file.endswith('.png'):
            continue #he may not be supposed to view these images
            user_prompt.append(
                {
                "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encode_image(file)}"
                    }
                } 
            )    
        elif file == 'extract.txt':
            with open(file, "r") as file:
                text = file.read()

                user_prompt.append({'type': 'text', 'text' : text})
        


    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "developer", "content": persona},
        {"role": "user", "content": user_prompt
        }
    ]
    )
    content = completion.choices[0].message.content

    match = re.search(r'RELATED:(.*?)BEGIN:(.*)', content, re.DOTALL)
    contents = []
    if match:
        related_part = match.group(1).strip()
        related_part.replace("*", '')

        begin_part = match.group(2).strip()
        begin_part.replace("*", '')

        contents = [related_part, begin_part]

    return contents
