
# Backend Dockerfile
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy the application code
COPY backend/ /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application port
EXPOSE 5000

# Start the application
CMD ["python", "app.py"]
