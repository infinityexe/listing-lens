import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# Setup
st.set_page_config(page_title="ListingLens AI", page_icon="🏠")
st.title("🏠 ListingLens: Photo-to-Description Generator")
st.subheader("Upload photos of the property, get a viral listing description.")

# AUTOMATION: Hides the key from the user, pulls from your Secrets
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("System Error: API Key not found. Please contact support.")

style = st.selectbox("Description Style", ["Luxury & Elegant", "Cozy & Warm", "Modern & Hip", "Urgent & Investor-Focused"])

uploaded_files = st.file_uploader("Upload Property Photos (Max 5)", accept_multiple_files=True, type=['jpg', 'jpeg', 'png'])

if uploaded_files and st.button("Generate Description"):
    with st.spinner("Analyzing photos and writing description..."):
        try:
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            images = [Image.open(file) for file in uploaded_files]
            
            prompt = f"""
            You are a world-class real estate copywriter. 
            Look at these images. Identify the key features (floors, lighting, amenities, vibe).
            Write a compelling real estate listing description in a {style} tone.
            Include a catchy headline, a feature list, and a call to action.
            """
            
            response = model.generate_content([prompt] + images)
            st.markdown("### 📝 Your Listing Description")
            st.write(response.text)
            st.success("Done! Copy and paste this to Zillow/Airbnb.")
        except Exception as e:
            st.error(f"Error: {e}")
