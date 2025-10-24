# 🚀 Quick Start Guide - Flappy Bird Web

## ⚡ Play Now (Local)

The server is **already running**! Just open your browser:

👉 **http://localhost:5000**

---

## 🌐 Deploy to Railway (5 Minutes)

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Flappy Bird web version"
git branch -M main
git remote add origin YOUR_GITHUB_URL
git push -u origin main
```

### Step 2: Deploy on Railway
1. Go to https://railway.app (sign up with GitHub)
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your **flappybird** repository
5. Railway auto-detects the Dockerfile
6. Click **"Deploy"**
7. Once deployed, click **"Generate Domain"**
8. **Done!** Share your URL with friends! 🎉

---

## 🎮 Local Commands

### Run Web Version
```bash
python app.py
# Visit http://localhost:5000
```

### Run Desktop Version (Original)
```bash
venv\Scripts\python.exe flappy_bird.py
# Game window opens
```

### Run with Docker
```bash
docker-compose up
# Visit http://localhost:5000
```

---

## 📋 What You Got

✅ **Web-based game** - Play in any browser  
✅ **Flask backend** - REST API for scores  
✅ **Modern UI** - Responsive design  
✅ **Docker ready** - Containerized  
✅ **Railway config** - One-click deploy  
✅ **Git-ready** - .gitignore configured  
✅ **All features** - Levels, enemies, coins  

---

## 🎯 Controls

- **SPACE** / **UP ARROW** / **CLICK** - Flap
- Avoid buildings and projectiles
- Collect coins for bonus points
- Progress through 5 levels

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `app.py` | Web server |
| `static/js/game.js` | Game logic |
| `templates/index.html` | Game UI |
| `Dockerfile` | Container config |
| `railway.json` | Railway deploy |
| `levels.json` | Game settings |

---

## 🆘 Help

**Game won't load?**
- Check http://localhost:5000
- Look at console output
- Verify all files are present

**Deploy failed?**
- Check Railway build logs
- Ensure all files pushed to GitHub
- Verify Dockerfile syntax

**Need more info?**
- `DEPLOYMENT.md` - Full deploy guide
- `README.md` - Complete documentation
- `CONVERSION_SUMMARY.md` - What changed

---

## 🎉 Success!

Your game is now:
- 🌐 Web-based (playable anywhere)
- ☁️ Cloud-ready (Railway, Heroku, etc.)
- 🐳 Dockerized (portable)
- 📱 Responsive (mobile-friendly)

**Happy Gaming! 🐦**

