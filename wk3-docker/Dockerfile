# Use the Python 3 slim base image
FROM python:3-slim

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the requirements.txt file to the working directory
COPY requirements.txt ./

# Install the Python dependencies specified in requirements.txt
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copy the book.py file to the working directory
COPY ./book.py .

# Set the command to run when the container starts
CMD [ "python", "./book.py" ]