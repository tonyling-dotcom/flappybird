# Flappy Bird - Deployment Guide

## Railway Deployment

### Prerequisites
- GitHub account
- Railway account (sign up at https://railway.app)
- Your code pushed to GitHub

### Deployment Steps

#### 1. Push Code to GitHub

```bash
git init
git add .
git commit -m "Initial commit - Flappy Bird web version"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

#### 2. Deploy to Railway

**Option A: Using Railway Dashboard**

1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your flappybird repository
5. Railway will automatically detect the Dockerfile
6. Click "Deploy"
7. Once deployed, click "Generate Domain" to get a public URL

**Option B: Using Railway CLI**

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up
```

#### 3. Environment Variables (Optional)

Railway automatically sets the `PORT` variable. No additional configuration needed!

#### 4. Access Your Game

Once deployed, Railway will provide you with a URL like:
```
https://your-app-name.railway.app
```

Visit this URL to play your game!

### Automatic Deployments

Railway automatically redeploys when you push to your main branch:

```bash
git add .
git commit -m "Update game features"
git push
```

Railway will detect the changes and redeploy automatically.

### Monitoring

- **View Logs**: In Railway dashboard, click on your service and go to "Logs"
- **Metrics**: Check CPU, Memory, and Network usage in the "Metrics" tab
- **Health Check**: The app includes a health check endpoint at `/`

### Troubleshooting

#### Build Fails
- Check that all files are committed to git
- Verify Dockerfile syntax
- Check Railway build logs for specific errors

#### App Crashes
- Check logs in Railway dashboard
- Verify all required files are present
- Ensure highscore.json exists (create empty one if needed)

#### High Score Not Persisting
- Railway provides ephemeral storage
- For permanent storage, consider:
  - Railway's PostgreSQL plugin
  - External database service
  - Cloud storage (S3, etc.)

### Cost

Railway offers:
- **Free Tier**: $5 free credits per month (sufficient for hobby projects)
- **Developer Plan**: $5/month for more resources
- Pay-as-you-go for usage above free tier

### Alternative Deployment Platforms

#### Render.com
```bash
# Similar process to Railway
# Create render.yaml:
services:
  - type: web
    name: flappybird
    env: docker
    plan: free
```

#### Heroku
```bash
# Uses Procfile (already included)
heroku create your-app-name
git push heroku main
```

#### DigitalOcean App Platform
- Push to GitHub
- Connect DigitalOcean to your repo
- Select Dockerfile deployment
- Deploy

#### Google Cloud Run
```bash
gcloud builds submit --tag gcr.io/PROJECT-ID/flappybird
gcloud run deploy --image gcr.io/PROJECT-ID/flappybird --platform managed
```

### Local Development

Run locally before deploying:

```bash
# Using Python directly
python app.py

# Using Docker
docker-compose up --build

# Using Gunicorn (production-like)
gunicorn --bind 0.0.0.0:5000 app:app
```

Access at: http://localhost:5000

### Production Checklist

- [ ] All code committed to GitHub
- [ ] requirements.txt includes all dependencies
- [ ] Dockerfile builds successfully locally
- [ ] Game works correctly in browser locally
- [ ] highscore.json exists
- [ ] .gitignore configured properly
- [ ] Environment variables set (if any)
- [ ] Domain configured (optional)
- [ ] SSL/HTTPS enabled (automatic on Railway)

### Updating the Game

1. Make changes locally
2. Test thoroughly
3. Commit and push:
   ```bash
   git add .
   git commit -m "Description of changes"
   git push
   ```
4. Railway automatically redeploys

### Performance Tips

1. **Reduce Image Sizes**: Optimize PNG files
2. **Enable Caching**: Already configured in Flask
3. **CDN**: Use Railway's built-in CDN
4. **Compression**: Add gzip middleware if needed
5. **Monitor**: Check Railway metrics regularly

### Security

- **HTTPS**: Automatically enabled on Railway
- **CORS**: Configure if needed for API access
- **Rate Limiting**: Consider adding for production
- **Input Validation**: Already implemented in API endpoints

## Questions?

- Railway Docs: https://docs.railway.app
- Flask Docs: https://flask.palletsprojects.com
- Project Issues: Create an issue on GitHub

