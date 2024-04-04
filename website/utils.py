import os
import openai
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())

# Set OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

def get_completion(prompt, model="gpt-3.5-turbo"):
    try:
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0.5  # Adjust temperature as needed for creativity vs consistency
        )
        return response.choices[0].message["content"]
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
