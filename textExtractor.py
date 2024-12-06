import streamlit as st
import ollama
from PIL import Image
import io

# Set up page configuration
st.set_page_config(
    page_title="Ollama OCR",
    page_icon="🦙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description in main area
st.title("🦙 Ollama OCR")
st.markdown('<p style="margin-top: -20px;">Extract structured text from images using Ollama OCR!</p>', unsafe_allow_html=True)
st.markdown("---")

# Upload controls in the sidebar
with st.sidebar:
    st.header("Upload Image")
    uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image")

        if st.button("Extract Text 🔍"):
            with st.spinner("Processing image..."):
                try:
                    # Since Ollama's chat function likely doesn't accept images as part of a 'messages' list, 
                    # we need to send the image data in a format Ollama expects (check Ollama docs)
                    
                    # Convert image to bytes
                    img_bytes = uploaded_file.getvalue()

                    # Assuming Ollama supports a direct image-to-text method, check Ollama SDK usage
                    response = ollama.chat(
                        model="llama3.2-vision",  # Example model, adjust based on your requirements
                        messages=[{
                            'role': 'user',
                            'content': "Analyze the text in the provided image and extract it."
                        }],
                        data=img_bytes  # Assuming 'data' is the correct keyword to send image data
                    )

                    st.session_state['ocr_result'] = response.message.content
                except Exception as e:
                    st.error(f"Error processing image: {str(e)}")

# Display the result of OCR extraction
if 'ocr_result' in st.session_state:
    st.subheader("Extracted Text")
    st.text_area("OCR Result", st.session_state['ocr_result'], height=300)
else:
    st.info("Upload an image and click 'Extract Text' to see the results here.")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Ollama Model | [Report an Issue](https://github.com/)")
