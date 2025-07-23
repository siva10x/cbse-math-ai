# views/upload.py
import streamlit as st
import os
import tempfile
import base64
from pdf2image import convert_from_path
from openai import OpenAI
import json
from collections import defaultdict

from myutils.logger import setup_logger
from myutils.prompts import get_math_question_extraction_prompt
from myutils.question_image_extractor import extract_images_for_questions
from myutils.gpt_vision_extractor import extract_questions_from_images

logger = setup_logger(__name__)

UPLOAD_DIR = "uploads"

llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def convert_pdf_to_images(pdf_path, output_folder="temp_images"):
    os.makedirs(output_folder, exist_ok=True)
    pages = convert_from_path(pdf_path, dpi=300)

    image_paths = []
    for i, page in enumerate(pages):
        image_path = os.path.join(output_folder, f"page_{i+1}.png")
        page.save(image_path, "PNG")
        image_paths.append(image_path)

    logger.info(f"✅ Converted {len(image_paths)} pages to images.")
    return image_paths



# Render the Streamlit UI for uploading question papers
# This function sets up the UI elements for file upload and processing.
# It allows users to upload multiple PDF files and processes them.
# The processing includes extracting images and saving them for further analysis.
def render():
    st.title("📤 Upload Question Papers")
    st.markdown("Upload scanned CBSE Math question papers (in PDF format).")

    uploaded_file = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=False)

    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            pdf_path = tmp_file.name

        st.success("✅ PDF uploaded successfully.")

        if st.button("🚀 Process File"):
            st.info("🔄 Converting PDF to images...")
            image_paths = convert_pdf_to_images(pdf_path)
            
            # if st.button("🚀 Extract Questions"):
            # Step 1: GPT Extraction
            gpt_output_raw = extract_questions_from_images(image_paths)

            # Step 2: Visual Extraction
            st.info("🔍 Detecting supporting images (red boxes)...")
            cropped_images = extract_images_for_questions(pdf_path)
            
            # Step 3: Combine (Assumes GPT output is list of dicts)
            try:
                gpt_questions_json = json.loads(gpt_output_raw)
                gpt_questions = gpt_questions_json.get('questions')
            except Exception as e:
                st.error("❌ GPT output is not valid JSON.")
                st.code(gpt_output_raw)
                return

            # Match images to questions
            for q in gpt_questions:
                qid = q.get("question_id")
                q["supporting_images"] = [
                    # img for img in cropped_images if img["question_id"] == qid
                    img_path for img_path in cropped_images.get(q["question_id"], [])
                ]

            # Save
            output_path = os.path.join("outputs", "questions_combined.json")
            os.makedirs("outputs", exist_ok=True)
            with open(output_path, "w") as f:
                json.dump(gpt_questions, f, indent=2)

            st.success("✅ Questions + images extracted and saved!")
            
            # Convert to pretty JSON string
            json_str = json.dumps(gpt_questions, indent=2)

            # Display in Streamlit as code
            st.code(json_str, language="json")
            