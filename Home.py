import streamlit as st
import ImageUpload
import ManualEntry

# Main application
if __name__ == "__main__":
    st.set_page_config(page_title="Receipt Scanner Demo")
    st.header("Receipt Scanner Application")

    
    image_upload, manual_entry = st.tabs(["🖼️ Image Upload", "📝Manual Entry"])

    with image_upload:
        ImageUpload.image_upload()

    with manual_entry:
        ManualEntry.manual_entry()