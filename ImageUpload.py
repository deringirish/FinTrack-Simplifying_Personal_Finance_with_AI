import time
import json
import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter
from Input import input_value
import DisplayDetails
import DataBaseLogic
import Helper as hp
import GeminiIntegration as gi


def image_upload():
    st.subheader("Upload Receipt Image to Analyse...")
    uploaded_file = st.file_uploader(
        "Upload a Receipt...", type=["jpg", "jpeg", "png"])
    image = None

    if uploaded_file:
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)
        except Exception as e:
            st.error(f"Error processing the uploaded file: {e}")

    if st.button("Analyse Uploaded Receipt"):
        if not uploaded_file:
            st.error("Please upload an image to proceed.")
        else:
            try:
                with st.spinner('Processing receipt...'):
                    enhanced_image = hp.enhance_image(image)

                    start_time = time.time()
                    response = gi.get_gemini_response(input_value, enhanced_image)
                    elapsed_time = time.time() - start_time

                    if response:
                        st.info(f"Time Taken: {elapsed_time:.2f} seconds", icon="⌚")
                        json_string = hp.clean_response(response)

                        if json_string:
                            try:
                                json_data = json.loads(json_string)
                                json_data = hp.clean_numeric_values(json_data)

                                updated_json_data = DisplayDetails.print_response_from_image(json_data)
                                DataBaseLogic.upload_to_database(updated_json_data)

                            except json.JSONDecodeError as e:
                                st.error(f"Error decoding JSON: {e}")
                        else:
                            st.error("Cleaned JSON response is empty.")
                    else:
                        st.error("No response received from the Gemini API.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
