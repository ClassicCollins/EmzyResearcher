# Use an official Python image as the base image
FROM python:3.11

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install system dependencies, including curl and other needed packages
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*  # Clean up apt cache to reduce image size

# Install Ollama (Install Ollama by following the instructions on their official site)
RUN curl -sSL https://ollama.com/download/ollama-linux-x86_64.tar.gz -o /tmp/ollama.tar.gz \
    && tar -xvf /tmp/ollama.tar.gz -C /usr/local/bin/ \
    && rm /tmp/ollama.tar.gz

# Set the working directory in the container
WORKDIR /textExtractor

# Copy the application files into the container
RUN git clone https://github.com/ClassicCollins/EmzyResearcher/blob/classic/textExtractor

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the necessary port (default for Streamlit is 8501)
EXPOSE 8501

# Set the default command to run the Streamlit app
CMD ["streamlit", "run", "textExtractor.py"]
