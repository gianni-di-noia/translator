# Use the official Python image as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY . /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container

EXPOSE 8000

# Command to run on container start
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


# FROM python:3.11-slim
# ENV PYTHONUNBUFFERED 1
# COPY ./requirements.txt /tmp/requirements.txt
# RUN pip install --no-cache-dir -q -r /tmp/requirements.txt
# EXPOSE 80
# WORKDIR /app
# COPY . /app
