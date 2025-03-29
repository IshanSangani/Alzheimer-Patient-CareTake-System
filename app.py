import streamlit as st
import base64
from PIL import Image
import io
from google import generativeai as genai

# Set up the API key
API_KEY = "AIzaSyD16PQAtvVGsanvV5mcuN38LFjd541JyYM"
genai.configure(api_key=API_KEY)

# Set up Streamlit page
st.set_page_config(page_title="Image Recognition App", layout="centered")
st.title("Image Recognition App")
st.write("Upload an image and the app will tell you what it sees!")

# File uploader
uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_container_width=True)
    
    # Convert image for Gemini API
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    image_bytes = buffered.getvalue()
    
    # Add a button to analyze the image
    if st.button("Analyze Image"):
        with st.spinner("Analyzing image..."):
            try:
                # Initialize Gemini model with the updated model name
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Generate content with the image
                response = model.generate_content([
                    "What is in this image? Describe it in detail.",
                    {"mime_type": "image/jpeg", "data": image_bytes}
                ])
                
                # Display results
                st.subheader("Analysis Results")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Error analyzing image: {str(e)}")
                import traceback
                st.error(traceback.format_exc())

# Instructions at the bottom
st.markdown("""
### How to use:
1. Upload an image using the file uploader
2. Click the 'Analyze Image' button
3. Wait for the analysis results
""")