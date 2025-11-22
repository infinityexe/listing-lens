import streamlit as st
import google.generativeai as genai
from PIL import Image

# Setup
st.set_page_config(page_title="ListingLens AI", page_icon="🏠")
st.title("🏠 ListingLens: Photo-to-Description Generator")
st.subheader("Upload photos of the property, get a market-ready listing description.")

# 1. AUTHENTICATION & SETUP
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("⚠️ System Error: API Key not found. Please check Streamlit settings.")
    st.stop()

# 2. SMART MODEL DETECTION
try:
    available_models = []
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            available_models.append(m.name)
    valid_model_name = next((m for m in available_models if 'flash' in m and '1.5' in m), None)
    if not valid_model_name:
        valid_model_name = next((m for m in available_models if 'flash' in m), None)
    if not valid_model_name:
        valid_model_name = next((m for m in available_models if 'pro' in m), available_models[0])
except Exception as e:
    st.error(f"⚠️ Could not auto-detect models. Error: {e}")
    st.stop()

# 3. INTERFACE
style = st.selectbox("Description Tone", ["Standard Professional (Zillow style)", "Luxury / High-End", "Investment / Fixer-Upper"])
uploaded_files = st.file_uploader("Upload Property Photos", accept_multiple_files=True, type=['jpg', 'jpeg', 'png'])

if uploaded_files and st.button("Generate Description"):
    with st.spinner("Analyzing property details..."):
        try:
            model = genai.GenerativeModel(valid_model_name)
            images = [Image.open(file) for file in uploaded_files]
            
            # THE "HUMANIZER" PROMPT
            prompt = f"""
            Role: You are a direct, pragmatic Real Estate Agent with 20 years of experience.
            Task: Write a listing description based ONLY on the visual evidence in these images.
            
            Tone: {style}
            
            CRITICAL RULES (Do NOT break these):
            1. If the images are NOT of a house, room, or building, simply output: "⚠️ These photos do not appear to be real estate. Please upload property photos."
            2. NO FLUFF. Do not use words like: "tapestry," "symphony," "nestled," "meticulously," "breathtaking," "oasis," or "bespoke."
            3. Be factual. Describe the floors (wood/tile?), the light (windows?), the appliances.
            4. Format clearly:
               - A catchy 5-word Headline.
               - One paragraph of summary (max 3 sentences).
               - A bulleted list of 5 specific features visible in the photos.
            """
            
            response = model.generate_content([prompt] + images)
            st.markdown("### 📝 Market-Ready Description")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
