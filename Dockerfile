# Use the official Python image from the Docker Hub
FROM python:3.12.3-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Expose the port that your app runs on
EXPOSE 8080

# Command to run your application
CMD ["python", "app.py"]
