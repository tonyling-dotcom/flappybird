# Use Python 3.13 slim image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY flappy_bird.py .
COPY levels.json .
COPY highscore.json .
COPY templates/ ./templates/
COPY static/ ./static/

# Create directory for runtime data
RUN mkdir -p /app/data

# Set environment variables
ENV PORT=5000
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 5000

# Run the Flask web application with gunicorn
CMD gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 60 app:app

