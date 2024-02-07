# Use a base image with Python installed
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the activity_log.py file into the container
COPY error.py .
COPY amqp_connection.py .
# Install any dependencies required by the script
RUN pip install pika

# Set the command to run the activity_log.py script
CMD ["python", "error.py"]
