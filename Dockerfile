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
COPY start.sh .

# Make start script executable
RUN chmod +x start.sh

# Create directory for runtime data
RUN mkdir -p /app/data

# Set environment variables
ENV PORT=5000
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 5000

# Run the Flask web application using startup script
CMD ["./start.sh"]

