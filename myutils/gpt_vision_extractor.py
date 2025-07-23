# utils/gpt_vision_extractor.py

import base64
from openai import OpenAI
from dotenv import load_dotenv
import os
from myutils.prompts import get_math_question_extraction_prompt

# Load env vars
load_dotenv()

USE_MOCK_GPT = True  # <- toggle this when needed

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("❌ OPENAI_API_KEY not found in environment.")

client = OpenAI(api_key=api_key)

def encode_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


def extract_questions_from_images(image_paths):
    """
    Given a list of image file paths, calls GPT-4o Vision model
    with the question extraction prompt, and returns the raw JSON string.
    """
    if USE_MOCK_GPT:
        with open("mocks/sample_gpt_response.json", "r") as f:
            return f.read()
    else:
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": get_math_question_extraction_prompt()}
                ]
            }
        ]

        for path in image_paths:
            base64_img = encode_image_base64(path)
            messages[0]["content"].append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{base64_img}",
                    "detail": "high"
                }
            })

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content