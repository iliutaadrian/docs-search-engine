# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=src/app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV OPENAI_API_KEY="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"

# Run app.py when the container launches
CMD ["flask", "run"]
