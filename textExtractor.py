import streamlit as st
import ollama
from PIL import Image
import io

# Page configuration
st.set_page_config(
    page_title="Llama OCR",
    page_icon="🦙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description in main area
st.title("🦙 Llama OCR")

# Add clear button to top right
col1, col2 = st.columns([6, 1])
with col2:
    if st.button("Clear 🗑️"):
        if 'ocr_result' in st.session_state:
            del st.session_state['ocr_result']
        st.rerun()

st.markdown('<p style="margin-top: -20px;">Extract structured text from images using Llama 3.2 Vision!</p>', unsafe_allow_html=True)
st.markdown("---")

# Move upload controls to sidebar
with st.sidebar:
    st.header("Upload Image")
    uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image")
        
        # Allow users to select the model version (optional)
        model_version = st.selectbox("Select Model Version", ["llama3.2-vision", "llama2-vision"], index=0)
        
        if st.button("Extract Text 🔍", type="primary"):
            with st.spinner("Processing image..."):
                try:
                    response = ollama.chat(
                        model=model_version,
                        messages=[{
                            'role': 'user',
                            'content': """Analyze the text in the provided image. Extract all readable content
                                        and present it in a structured Markdown format that is clear, concise, 
                                        and well-organized. Ensure proper formatting (e.g., headings, lists, or
                                        code blocks) as necessary to represent the content effectively.""",
                            'images': [uploaded_file.getvalue()]  # Sending image as raw bytes
                        }]
                    )
                    
                    # Save OCR result to session state
                    if 'ocr_result' not in st.session_state:
                        st.session_state['ocr_result'] = ""
                    st.session_state['ocr_result'] = response.message.content
                    
                except ollama.exceptions.OllamaAPIError as api_error:
                    st.error(f"API Error: {str(api_error)}")
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
st.markdown("Made with ❤️ using Llama Vision Model2 | [Report an Issue](https://github.com/)")
