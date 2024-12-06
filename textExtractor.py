import streamlit as st
from PIL import Image
import pytesseract

# Page configuration
st.set_page_config(
    page_title="Tesseract OCR",
    page_icon="🦙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description in main area
st.title("🦙 Tesseract OCR")

# Add clear button to top right
col1, col2 = st.columns([6, 1])
with col2:
    if st.button("Clear 🗑️"):
        if 'ocr_result' in st.session_state:
            del st.session_state['ocr_result']
        st.rerun()

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
        
        if st.button("Extract Text 🔍", type="primary"):
            with st.spinner("Processing image..."):
                try:
                    # Use Tesseract to extract text from the image
                    ocr_result = pytesseract.image_to_string(image)

                    # Save OCR result to session state
                    if 'ocr_result' not in st.session_state:
                        st.session_state['ocr_result'] = ""
                    st.session_state['ocr_result'] = ocr_result
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

# Main content area for results
if 'ocr_result' in st.session_state:
    if st.session_state['ocr_result']:
        st.markdown(st.session_state['ocr_result'])
    else:
        st.warning("No OCR result available.")
else:
    st.info("Upload an image and click 'Extract Text' to see the results here.")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Tesseract OCR | [Report an Issue](https://github.com/)")
