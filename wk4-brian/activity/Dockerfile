# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
RUN curl https://bchewy.s3.ap-southeast-1.amazonaws.com/requirements.txt > requirements.txt
# COPY ../requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the activity_log.py script into the container
COPY activity_log.py .

# Set the command to run the script when the container starts
CMD ["python", "activity_log.py"]
