import streamlit as st
import pytesseract
from PIL import Image
import os
import subprocess

# Function to check if Tesseract is installed and accessible
def check_tesseract():
    try:
        # Run the command to get Tesseract version
        subprocess.run(["tesseract", "--version"], check=True)
        return True
    except FileNotFoundError:
        return False

# Set the Tesseract executable path based on environment
if not check_tesseract():
    st.error("Tesseract is not installed or not found in the PATH.")
else:
    st.success("Tesseract is installed and ready to use!")

# Set Tesseract path manually (modify if necessary for Streamlit Cloud)
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"  # Common default path for Streamlit Cloud

# Page configuration
st.set_page_config(
    page_title="Llama OCR",
    page_icon="🦙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description in main area
st.title("🦙 Llama OCR")
st.markdown('<p style="margin-top: -20px;">Extract structured text from images using Tesseract OCR!</p>', unsafe_allow_html=True)
st.markdown("---")

# Move upload controls to sidebar
with st.sidebar:
    st.header("Upload Image")
    uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image")

        # Extract text from the uploaded image
        if st.button("Extract Text 🔍", type="primary"):
            with st.spinner("Processing image..."):
                try:
                    # Use pytesseract to extract text
                    extracted_text = pytesseract.image_to_string(image)
                    st.session_state['ocr_result'] = extracted_text
                except Exception as e:
                    st.error(f"Error processing image: {str(e)}")

# Display the OCR result
if 'ocr_result' in st.session_state:
    st.subheader("Extracted Text")
    st.text_area("OCR Result", st.session_state['ocr_result'], height=300)
else:
    st.info("Upload an image and click 'Extract Text' to see the results here.")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Tesseract OCR | [Report an Issue](https://github.com/)")
