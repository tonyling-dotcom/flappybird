# 🐦 Flappy Bird - City Edition (Web Version)

A modern web-based remake of the classic Flappy Bird game with a city skyline theme, built with Flask and HTML5 Canvas.

![Flappy Bird](https://img.shields.io/badge/Game-Flappy%20Bird-blue)
![Python](https://img.shields.io/badge/Python-3.13-green)
![Flask](https://img.shields.io/badge/Flask-3.0-red)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)

## 🎮 Features

- **5 Progressive Levels** - From "Easy Glide" to "Legendary Bird"
- **Dynamic Obstacles** - Navigate through city buildings with varying gaps
- **Flying Enemies** - Avoid enemies that shoot projectiles
- **Collectible Coins** - Gather coins for bonus points
- **High Score System** - Persistent high score tracking
- **Responsive Design** - Works on desktop and mobile devices
- **Beautiful UI** - Modern, gradient-based interface
- **Sound Effects** - Audio feedback for actions (flap, enemy, game over)
- **Particle Effects** - Visual feedback for collecting items

## 🚀 Quick Start

### Play Online (After Deployment)

Once deployed to Railway, simply visit your app URL and start playing!

### Run Locally

#### Option 1: Using Python (Development)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Flask app
python app.py
```

Visit http://localhost:5000 in your browser.

#### Option 2: Using Docker

```bash
# Build and run with Docker Compose
docker-compose up --build
```

Visit http://localhost:5000 in your browser.

#### Option 3: Using Production Server

```bash
# Install dependencies
pip install -r requirements.txt

# Run with Gunicorn
gunicorn --bind 0.0.0.0:5000 app:app
```

## 🎯 How to Play

### Controls
- **SPACE** - Make the bird flap
- **UP ARROW** - Make the bird flap  
- **MOUSE CLICK** - Make the bird flap
- **ESC** - Pause game (future feature)

### Objectives
- Navigate through buildings without crashing
- Avoid enemy projectiles
- Collect coins for bonus points
- Progress through 5 increasingly difficult levels

### Scoring
- **Buildings Passed**: +1 point each
- **Enemies Hit**: +3 points each
- **Coins Collected**: +2 points each

### Level Progression
| Level | Name | Required Score | Difficulty |
|-------|------|----------------|------------|
| 1 | Easy Glide | 5 | ⭐ |
| 2 | City Cruiser | 10 | ⭐⭐ |
| 3 | Urban Flyer | 15 | ⭐⭐⭐ |
| 4 | Skyline Master | 20 | ⭐⭐⭐⭐ |
| 5 | Legendary Bird | 30 | ⭐⭐⭐⭐⭐ |

## 📁 Project Structure

```
flappybird/
├── app.py                  # Flask web application
├── flappy_bird.py         # Original Pygame version
├── levels.json            # Game configuration & levels
├── highscore.json         # Persistent high score storage
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose setup
├── railway.json          # Railway deployment config
├── Procfile              # Process file for deployment
├── templates/
│   └── index.html        # Main game template
├── static/
│   ├── css/
│   │   └── style.css     # Game styling
│   ├── js/
│   │   └── game.js       # Game logic (JavaScript)
│   ├── images/           # Game assets
│   │   ├── player.png
│   │   ├── enemy.png
│   │   └── map.png
│   └── audio/            # Sound effects
│       ├── bg.mp3
│       ├── flap.mp3
│       ├── enemy.mp3
│       └── gameover.mp3
└── assets/               # Original Pygame assets
```

## 🐳 Docker Deployment

### Build and Run

```bash
# Build the image
docker build -t flappybird-web .

# Run the container
docker run -p 5000:5000 flappybird-web

# Or use Docker Compose
docker-compose up
```

### Docker Hub (Optional)

```bash
# Tag and push to Docker Hub
docker tag flappybird-web yourusername/flappybird-web
docker push yourusername/flappybird-web
```

## ☁️ Cloud Deployment

### Railway (Recommended)

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push
   ```

2. **Deploy on Railway**:
   - Go to https://railway.app
   - Create new project from GitHub repo
   - Railway auto-detects Dockerfile
   - Click "Deploy"
   - Generate domain to get public URL

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

### Other Platforms

The app is compatible with:
- **Heroku**: Uses Procfile
- **Render**: Uses Dockerfile
- **DigitalOcean App Platform**: Uses Dockerfile
- **Google Cloud Run**: Uses Dockerfile
- **AWS Elastic Beanstalk**: Uses Dockerfile

## 🛠️ Development

### Prerequisites
- Python 3.13+
- pip
- Docker (optional)

### Setup Development Environment

```bash
# Clone the repository
git clone <your-repo-url>
cd flappybird

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python app.py
```

### Modifying Game Configuration

Edit `levels.json` to adjust:
- Level difficulty settings
- Spawn intervals
- Speed parameters
- Scoring rules
- Screen dimensions

### Adding New Features

1. **Backend**: Modify `app.py` for new API endpoints
2. **Frontend Logic**: Edit `static/js/game.js` for game mechanics
3. **Styling**: Update `static/css/style.css` for appearance
4. **UI**: Modify `templates/index.html` for layout changes

## 📊 API Endpoints

- `GET /` - Main game page
- `GET /api/config` - Get game configuration and levels
- `GET /api/highscore` - Get current high score
- `POST /api/highscore` - Update high score

## 🔧 Configuration

### Environment Variables

- `PORT`: Server port (default: 5000)
- `PYTHONUNBUFFERED`: Set to 1 for logging

### Game Settings

All game settings are in `levels.json`:
- Screen dimensions
- Physics (gravity, flap strength)
- Object sizes
- Scoring values

## 🎨 Customization

### Changing Colors

Edit `static/css/style.css`:
```css
/* Primary gradient */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Modifying Game Mechanics

Edit `static/js/game.js` to change:
- Player physics
- Collision detection
- Spawn rates
- Difficulty progression

## 📝 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🐛 Troubleshooting

### Game Won't Load
- Check browser console for errors
- Ensure all assets loaded correctly
- Verify Flask server is running

### High Scores Not Saving
- Check file permissions on `highscore.json`
- Verify API endpoint is accessible
- Check browser network tab for failed requests

### Audio Not Playing
- Check browser audio permissions
- Ensure audio files exist in `static/audio/`
- Some browsers require user interaction before playing audio

## 📚 Documentation

- [Deployment Guide](DEPLOYMENT.md) - Detailed deployment instructions
- [Docker Guide](README_DOCKER.md) - Docker-specific documentation
- [Features: Coins](COINS_FEATURE.md) - Coin system documentation
- [Features: Projectiles](PROJECTILES_FEATURE.md) - Combat system documentation

## 🙏 Acknowledgments

- Original Flappy Bird by Dong Nguyen
- Flask framework by Pallets
- Pygame for the original desktop version
- Railway for easy deployment

## 📧 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review Railway/Flask documentation

---

Made with ❤️ by the Flappy Bird team

**Happy Gaming! 🎮🐦**
