# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements and install
COPY app/requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

# Copy the rest of the app code
COPY app/ .

# The app runs on 8080
EXPOSE 8080

# Command to run the app
CMD ["python", "main.py"]
