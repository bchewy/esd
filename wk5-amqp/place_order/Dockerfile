# Use a base image with Python installed
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the activity_log.py file into the container
COPY place_order.py .
COPY amqp_connection.py .
COPY invokes.py .
# Install any dependencies required by the script
RUN pip install pika
RUN pip install flask
RUN pip install flask_cors
RUN pip install requests

EXPOSE 5100

# Set the command to run the activity_log.py script
CMD ["python", "place_order.py"]
