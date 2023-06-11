FROM python:3.11

# Set the working directory
WORKDIR /ttt_app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Set the Flask environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Expose the application port
EXPOSE 5000

# Set the default command
CMD ["flask", "run", "--host=0.0.0.0"]

