


import streamlit as st
import base64

# Step 1: Encode local image to base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Step 2: Use raw string for path to avoid Unicode error
img_path = r"C:\\Users\\tirth\\OneDrive\\Desktop\\3Major_Project\background_img.png"
img_base64 = get_base64_image(img_path)

# Step 3: Inject CSS to add background
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/jpg;base64,{img_base64}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

# Step 4: Some sample content
st.title("📡 AwareNow Dashboard")
st.write("This page has a custom background image.")
