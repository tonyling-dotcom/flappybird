# Use Python 3.13 slim image
FROM python:3.13-slim

# Install system dependencies for pygame and X11
RUN apt-get update && apt-get install -y \
    libsdl2-2.0-0 \
    libsdl2-image-2.0-0 \
    libsdl2-mixer-2.0-0 \
    libsdl2-ttf-2.0-0 \
    libportmidi0 \
    libfreetype6 \
    libpng16-16 \
    libjpeg62-turbo \
    libx11-6 \
    libxext6 \
    libxrender1 \
    libxrandr2 \
    libxinerama1 \
    libxi6 \
    libxcursor1 \
    libxxf86vm1 \
    xauth \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY flappy_bird.py .
COPY levels.json .
COPY highscore.json .
COPY assets/ ./assets/

# Create directory for runtime data
RUN mkdir -p /app/data

# Set environment variables for display
ENV DISPLAY=:0
ENV SDL_VIDEODRIVER=x11

# Run the game
CMD ["python", "flappy_bird.py"]

