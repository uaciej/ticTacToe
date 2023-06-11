# Use an official Python runtime as the base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /ttt_app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project to the container
COPY . .

# Set the environment variable for Flask
ENV FLASK_APP=app.py

# Expose the port your Flask app will be running on
EXPOSE 5000

# Run the Flask application
CMD ["flask", "run"]
