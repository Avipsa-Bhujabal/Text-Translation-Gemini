import streamlit as st
import pandas as pd
import google.generativeai as genai
from gtts import gTTS
import os
import tempfile
from dotenv import load_dotenv
import PyPDF2


load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash") 

def translate_text_gemini(text, target_language):
    try:
        prompt = f"Translate the following text to {target_language}. Provide only the translated text:\n\n{text}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error translating text: {e}"
    