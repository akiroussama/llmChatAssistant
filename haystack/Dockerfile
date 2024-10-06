FROM python:3.9-slim

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Haystack configuration and application code
COPY config.py .
COPY app.py .

# Expose Haystack port
EXPOSE 8000

# Command to run the Flask app
CMD ["python", "app.py"]