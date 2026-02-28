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
    
def extract_text_from_file(uploaded_file):
    if uploaded_file.name.endswith('.txt'):
        return uploaded_file.read().decode('utf-8')
    elif uploaded_file.name.endswith('.pdf'):
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    elif uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
        return " ".join(df.astype(str).values.flatten())
    elif uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)
        return " ".join(df.astype(str).values.flatten())
    else:
        return "  "

def text_to_speech(text, language_code):
    try:
        tts = gTTS(text=text, lang=language_code)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_file.name)
        return temp_file.name
    except Exception as err:
        return f"Error converting text to speech: {err}"

st.set_page_config(page_title="Google Gemini Language Translation Model")
st.title("Multi Language Model")
st.write("Translate your text to into Multiple Language and convert it into speech")

text_input = st.text_area("Enter the User Prompt:")
uploaded_file = st.file_uploader("Upload a file (txt, pdf, csv, xlsx):", type=["txt", "pdf", "csv", "xlsx"])

language = {'Spanish': 'es', 
            'French': 'fr', 
            'German': 'de', 
            'English': 'en', 
            'Hindi': 'hi', 
            'Chinese': 'zh-cn', 
            'Japanese': 'ja', 
            'Russian': 'ru', 
            'Odia': 'or'}

selected_language = st.selectbox("Select Target Language:", options=list(language.keys()))

if st.button('Translate and Convert to Speech'):
    if uploaded_file is not None:
        text_input = extract_text_from_file(uploaded_file)
    else:
        text = text_input
    if text.strip() == "":
        st.error("Please enter some text or upload a file to translate.")
    else:
        translated_text = translate_text_gemini(text, selected_language)
        st.subheader("Translated Text:")
        st.write(translated_text)

        # Convert to speech        language_code = language[selected_language]
        audio_file = text_to_speech(translated_text, language[selected_language])
        if audio_file:
            st.audio(audio_file, format='audio/mp3')
            with open(audio_file, "rb") as f:
                st.download_button("Download Audio", f, file_name="translated_audio.mp3", mime="audio/mp3")
        else:
            st.error("Failed to convert text to speech.")

# Execute the Streamlit app
