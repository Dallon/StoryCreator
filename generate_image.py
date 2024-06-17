import openai
import os
import requests
from PIL import Image
from io import BytesIO

openai.api_key = os.getenv("OPENAI_API_KEY")

if openai.api_key is None:
    raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

TOKEN_COST_PER_MILLION = 15 / 1_000_000
DALL_E_COST_PER_IMAGE = 0.02

def read_story(file_path):
    with open(file_path, "r", encoding='utf-8') as file:
        return file.read()

def create_prompt(summary):
    return (f"Create an image in the artistic style of an amazing YouTube thumbnail image for an audiobook short story with the following summary: '{summary}'. "
            f"The image should dynamically adapt to the genre and mood of the story, without visible text."
            f"Incorporate visually engaging elements that represent the story's main characters, setting, and significant plot points. "
            f"The style should be vibrant and eye-catching to attract viewers' attention. "
            f"Use colors and lighting that enhance the overall appeal and accurately convey the story's atmosphere.")

def generate_image_from_summary(client, summary):
    try:
        prompt = create_prompt(summary)
        
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )

        print("API Response:", response)

        # Ensure the response data is correctly accessed
        if response and hasattr(response, 'data') and len(response.data) > 0:
            image_url = response.data[0].url
            return image_url, len(prompt)
        else:
            raise ValueError("No image URL found in the response")
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, 0

def save_image(url, save_path):
    try:
        if url:
            response = requests.get(url)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
            img.save(save_path)
            print(f"Image saved to {save_path}")
        else:
            print("Invalid URL provided")
    except requests.RequestException as req_e:
        print(f"An error occurred with the request: {req_e}")
    except IOError as io_e:
        print(f"An error occurred while saving the image: {io_e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def calculate_total_cost(token_count, dall_e_cost_per_image, token_cost_per_million):
    token_cost = (token_count / 1_000_000) * token_cost_per_million
    total_cost = token_cost + dall_e_cost_per_image
    return total_cost
