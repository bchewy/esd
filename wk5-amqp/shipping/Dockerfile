# Use a base image with Python installed
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the activity_log.py file into the container
COPY shipping_record.py .
# COPY amqp_connection.py .

# Install the required Python packages
RUN pip install flask
RUN pip install flask_cors
RUN pip install requests
COPY invokes.py .


# Set the command to run the activity_log.py script
CMD ["python", "shipping_record.py"]

