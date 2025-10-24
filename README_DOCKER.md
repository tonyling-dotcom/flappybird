# Flappy Bird - Docker Setup

This guide explains how to run the Flappy Bird game using Docker.

## Prerequisites

- Docker installed on your system
- Docker Compose (usually included with Docker Desktop)

## Platform-Specific Setup

### Linux

1. **Allow X11 connections** (run this each time before starting):
   ```bash
   xhost +local:docker
   ```

2. **Build and run**:
   ```bash
   docker-compose build
   docker-compose up
   ```

3. **After you're done** (optional, for security):
   ```bash
   xhost -local:docker
   ```

### macOS

1. **Install XQuartz**:
   ```bash
   brew install --cask xquartz
   ```

2. **Start XQuartz** and configure it:
   - Open XQuartz from Applications
   - Go to Preferences → Security
   - Enable "Allow connections from network clients"
   - Restart XQuartz

3. **Allow connections**:
   ```bash
   xhost + 127.0.0.1
   ```

4. **Set DISPLAY variable**:
   ```bash
   export DISPLAY=host.docker.internal:0
   ```

5. **Build and run**:
   ```bash
   docker-compose build
   docker-compose up
   ```

### Windows

Running GUI applications with Docker on Windows is more complex. Options include:

1. **VcXsrv (Recommended)**:
   - Download and install [VcXsrv](https://sourceforge.net/projects/vcxsrv/)
   - Start XLaunch with settings: Multiple windows, Display 0, Start no client, **Disable access control**
   - Set environment variable:
     ```cmd
     set DISPLAY=host.docker.internal:0
     ```
   - Build and run:
     ```cmd
     docker-compose build
     docker-compose up
     ```

2. **WSL2 with GUI support**:
   - Use WSL2 with built-in GUI support (Windows 11 or Windows 10 with WSLg)
   - Run Docker from within WSL2

## Quick Start Commands

```bash
# Build the Docker image
docker-compose build

# Run the game
docker-compose up

# Run in detached mode (background)
docker-compose up -d

# Stop the game
docker-compose down

# Rebuild and run
docker-compose up --build

# Remove containers and images
docker-compose down --rmi all
```

## Development

To make changes and test:

1. Edit your Python code or assets locally
2. Rebuild the image:
   ```bash
   docker-compose build
   ```
3. Run again:
   ```bash
   docker-compose up
   ```

## Troubleshooting

### "Cannot open display" error
- **Linux/Mac**: Make sure you ran `xhost +local:docker`
- **Windows**: Ensure VcXsrv is running and access control is disabled

### No sound
- Audio requires additional setup for Docker
- The compose file includes device mapping, but it may need adjustment for your system

### Permission errors
- On Linux, you might need to add your user to the docker group:
  ```bash
  sudo usermod -aG docker $USER
  ```
- Log out and back in for changes to take effect

### High score not persisting
- The `highscore.json` is mounted as a volume
- Make sure the file exists in your project directory before running
- Check file permissions

## Alternative: Run without Docker Compose

```bash
# Build
docker build -t flappybird .

# Run (Linux)
xhost +local:docker
docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v $(pwd)/highscore.json:/app/highscore.json \
  --network host \
  flappybird

# Run (macOS)
docker run -it --rm \
  -e DISPLAY=host.docker.internal:0 \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v $(pwd)/highscore.json:/app/highscore.json \
  --network host \
  flappybird
```

## Notes

- The container uses `network_mode: host` for easier X11 access
- High scores are persisted through a volume mount
- For production deployment, consider using a web-based renderer instead of X11

