
import pandas as pd
import time
import os
import random
import re
import json
from PIL import Image, ImageEnhance, ImageFilter
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
from Input import input_value
import DisplayDetails
import DataBaseLogic


# Load environment variables from .env file
load_dotenv()

# Retrieve API key from environment variables
GEMINI_KEY = os.getenv("GEMINI_KEY")

# Configure the Gemini API
try:
    # Retrieve API key from environment variables
    genai.configure(api_key=GEMINI_KEY)
except Exception as e:
    st.error(f"Failed to configure Gemini API: {e}")

# Function to enhance the image for better processing
def enhance_image(image):
    try:
        image = image.convert('L')  # Convert to grayscale
        image = ImageEnhance.Sharpness(
            image).enhance(2.0)  # Increase sharpness
        image = ImageEnhance.Brightness(
            image).enhance(1.5)  # Increase brightness
        # Apply edge enhancement
        image = image.filter(ImageFilter.EDGE_ENHANCE)
        return image
    except Exception as e:
        st.error(f"Error enhancing the image: {e}")
        return image

# Function to get response from Gemini API
def get_gemini_response(input_text, image):
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content([input_text, image])
        return response.text
    except Exception as e:
        st.error(f"Error generating content with Gemini: {e}")
        return None

# Helper function to remove commas from numeric strings
def remove_commas(value):
    if value is None or not isinstance(value, str):
        return value
    return value.replace(',', '')

# Function to clean the response
def clean_response(response):
    try:
        json_string = response.replace("```", "").replace("json", "").strip()
        # Replace escape sequences
        json_string = re.sub(r'\\[nrt]', ' ', json_string)
        # Remove backslashes
        json_string = json_string.replace('\\', '')  
        return json_string
    except Exception as e:
        st.error(f"Error cleaning response: {e}")
        return ""

# Function to clean numeric values in JSON
def clean_numeric_values(json_data):
    try:
        # Process 'items' list
        for item in json_data.get('items', []):
            if 'price' in item:
                price_str = remove_commas(item['price'])
                try:
                    item['price'] = float(price_str) if price_str else None
                except ValueError:
                    st.error(f"Error converting price '{
                             item['price']}' to float. Setting to None.")
                    item['price'] = None

        # Process 'summary' values
        if 'summary' in json_data:
            for key in ['grand_total', 'discount']:
                if key in json_data['summary']:
                    value_str = remove_commas(json_data['summary'][key])
                    try:
                        json_data['summary'][key] = float(
                            value_str) if value_str else None
                    except ValueError:
                        st.error(f"Error converting '{key}' '{
                                 json_data['summary'][key]}' to float. Setting to None.")
                        json_data['summary'][key] = None
    except Exception as e:
        st.error(f"Error cleaning numeric values: {e}")
    return json_data

# Function to handle image upload
def image_upload():
    uploaded_file = st.file_uploader(
        "Upload a Receipt...", type=["jpg", "jpeg", "png"])
    image = None

    if uploaded_file:
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)
        except Exception as e:
            st.error(f"Error processing the uploaded file: {e}")

    if st.button("Analyse Receipt"):
        if not uploaded_file:
            st.error("Please upload an image to proceed.")
        else:
            try:
                with st.spinner('Processing receipt...'):
                    # Enhance the image
                    enhanced_image = enhance_image(image)

                    # Get Gemini response
                    start_time = time.time()
                    response = get_gemini_response(input_value, enhanced_image)
                    elapsed_time = time.time() - start_time

                    if response:
                        st.info(f"Time Taken: {elapsed_time:.2f} seconds", icon="⌚")
                        json_string = clean_response(response)

                        if json_string:
                            try:
                                # Parse JSON and clean numeric values
                                json_data = json.loads(json_string)
                                json_data = clean_numeric_values(json_data)

                                # Process and upload data
                                updated_json_data = DisplayDetails.print_response_from_image(json_data)
                                DataBaseLogic.upload_to_database(updated_json_data)

                                st.success(
                                    "Data successfully uploaded to the database!")
                            except json.JSONDecodeError as e:
                                st.error(f"Error decoding JSON: {e}")
                        else:
                            st.error("Cleaned JSON response is empty.")
                    else:
                        st.error("No response received from the Gemini API.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
