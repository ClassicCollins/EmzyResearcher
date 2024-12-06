# Use an official Python image as the base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install system dependencies including Tesseract
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*  # Clean up apt cache to reduce image size

# Set the working directory in the container
WORKDIR /textExtractor

# Copy the application files into the container
COPY . /textExtractor

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the default command to run the Streamlit app
CMD ["streamlit", "run", "textExtractor.py"]
