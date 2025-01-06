import re 
import streamlit as st 
from PIL import Image, ImageEnhance, ImageFilter


def enhance_image(image):
    try:
        image = image.convert('L')  
        image = ImageEnhance.Sharpness(
            image).enhance(2.0)  
        image = ImageEnhance.Brightness(
            image).enhance(1.5)  
        image = image.filter(ImageFilter.EDGE_ENHANCE)
        return image
    except Exception as e:
        st.error(f"Error enhancing the image: {e}")
        return image


def remove_commas(value):
    if value is None or not isinstance(value, str):
        return value
    return value.replace(',', '')



def clean_response(response):
    try:
        json_string = response.replace("```", "").replace("json", "").strip()
        json_string = re.sub(r'\\[nrt]', ' ', json_string)
        json_string = json_string.replace('\\', '')
        return json_string
    except Exception as e:
        st.error(f"Error cleaning response: {e}")
        return ""



def clean_numeric_values(json_data):
    try:
        for item in json_data.get('items', []):
            if 'price' in item:
                price_str = remove_commas(item['price'])
                try:
                    item['price'] = float(price_str) if price_str else None
                except ValueError:
                    st.error(f"Error converting price '{
                             item['price']}' to float. Setting to None.")
                    item['price'] = None

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
