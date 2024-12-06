# Use an official Python image as the base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install system dependencies including Tesseract and other necessary libraries
RUN apt-get update && apt-get install -y \
    git \
    tesseract-ocr \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*  # Clean up apt cache to reduce image size

# Clone the GitHub repository
RUN git clone https://github.com/your-username/your-repository.git /textExtractor

# Set the working directory inside the container
WORKDIR /textExtractor

# Install the Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Streamlit app port (default is 8501)
EXPOSE 8501

# Set the default command to run the Streamlit app
CMD ["streamlit", "run", "textExtractor.py"]
