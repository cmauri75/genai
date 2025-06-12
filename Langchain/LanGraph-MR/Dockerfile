# Use official Python image as base
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

EXPOSE 5000

# Command to run the app (replace with your actual entrypoint)
CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]
