import streamlit as st
import google.generativeai as genai
from PIL import Image

# Setup
st.set_page_config(page_title="ListingLens AI", page_icon="🏠")
st.title("🏠 ListingLens: Photo-to-Description Generator")
st.subheader("Upload photos of the property, get a viral listing description.")

# 1. AUTHENTICATION
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("⚠️ System Error: API Key not found in Secrets. Please check Streamlit settings.")
    st.stop()

# 2. SMART MODEL DETECTION (The Fix)
# This block asks Google: "Which models are available to me?" and picks the best one.
try:
    available_models = []
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            available_models.append(m.name)
    
    # Priority: Try to find a 'Flash' model first (fastest), then 'Pro', then whatever works.
    valid_model_name = next((m for m in available_models if 'flash' in m and '1.5' in m), None)
    if not valid_model_name:
        valid_model_name = next((m for m in available_models if 'flash' in m), None)
    if not valid_model_name:
        valid_model_name = next((m for m in available_models if 'pro' in m), available_models[0])
        
    # st.write(f"DEBUG: Connected to {valid_model_name}") # Uncomment to see which model picked
    
except Exception as e:
    st.error(f"⚠️ Could not auto-detect models. Error: {e}")
    st.stop()

# 3. THE APP INTERFACE
style = st.selectbox("Description Style", ["Luxury & Elegant", "Cozy & Warm", "Modern & Hip", "Urgent & Investor-Focused"])

uploaded_files = st.file_uploader("Upload Property Photos (Max 5)", accept_multiple_files=True, type=['jpg', 'jpeg', 'png'])

if uploaded_files and st.button("Generate Description"):
    with st.spinner("Analyzing photos... (This usually takes 5-10 seconds)"):
        try:
            # Connect to the auto-detected model
            model = genai.GenerativeModel(valid_model_name)
            
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
            st.error(f"An error occurred: {e}")
