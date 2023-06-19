# Use the official Python base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the backend code into the container
COPY . .

EXPOSE 5000
# Set the entrypoint command to run the Flask app
CMD ["python", "app.py"]
