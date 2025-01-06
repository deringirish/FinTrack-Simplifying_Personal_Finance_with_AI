import streamlit as st
import ImageUpload
import ManualEntry
import CameraUpload

if __name__ == "__main__":
    st.set_page_config(page_title="Receipt Scanner Demo")
    st.header("Receipt Scanner Application")

    image_upload, camera_upload, manual_entry = st.tabs(
        ["🖼️ Image Upload", "📸 Camera Upload", "📝 Manual Entry"])

    with image_upload:
        ImageUpload.image_upload()

    with camera_upload:
        CameraUpload.image_upload()

    with manual_entry:
        ManualEntry.manual_entry()
