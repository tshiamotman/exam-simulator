# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application source code into the container
COPY . .

# Expose port 5000 (the default Flask port)
EXPOSE 8000

# Set an environment variable for the Flask application entry point
ENV FLASK_APP=app.py

# Command to run the application when the container starts
CMD ["flask", "run", "--host=0.0.0.0"]
