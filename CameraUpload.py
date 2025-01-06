import time
import json
import streamlit as st
from PIL import Image
from Input import input_value
import DisplayDetails
import DataBaseLogic
import Helper as hp
import GeminiIntegration as gi
from streamlit_back_camera_input import back_camera_input  

def image_upload():
    
    st.subheader("Capture Receipt Image to Analyse...")
    enable = st.checkbox("Enable back camera")
    if not enable:
        st.info("ℹ️  Please enable the back camera to capture an Receipt.")
    camera_placeholder = st.empty()
    if enable:
        st.info("⚠️ Please tap on the camera screen to capture the receipt.")
        picture = back_camera_input()

        if picture:
            try:
                image = Image.open(picture)
                st.image(image, caption="Captured Receipt", use_container_width=True)

                if st.button("Analyse Captured Receipt"):
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
                        st.error(f"An error occurred during the receipt analysis: {e}")
            except Exception as e: 
                st.error(f"Error processing the image: {e}")
