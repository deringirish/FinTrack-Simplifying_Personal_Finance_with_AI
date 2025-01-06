import os 
import streamlit as st
from dotenv import load_dotenv  
import google.generativeai as genai  


load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_KEY")

try:
    genai.configure(api_key=GEMINI_KEY)
except Exception as e:
    st.error(f"Failed to configure Gemini API: {e}")



def get_gemini_response(input_text, image):
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content([input_text, image])
        return response.text
    except Exception as e:
        st.error(f"Error generating content with Gemini: {e}")
        return None
