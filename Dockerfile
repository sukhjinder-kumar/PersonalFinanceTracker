# Use the official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy source code
COPY . /app

# Install make and update the apt-get package list
# RUN apt-get update && apt-get install -y make

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Default command
# CMD ["python", "populate.py"]
