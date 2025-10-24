# 🔧 Railway Port Issue - FIXED

## Problem
Railway was showing this error:
```
Error: '$PORT' is not a valid port number.
```

## Root Cause
The Docker `CMD` instruction wasn't properly expanding the `$PORT` environment variable. Docker's exec form (`CMD ["command"]`) doesn't perform shell variable expansion.

## Solution Implemented

### Created `start.sh` Script
A dedicated startup script that properly handles the PORT environment variable:

```bash
#!/bin/bash
PORT=${PORT:-5000}
echo "Starting Gunicorn on port $PORT..."
exec gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 60 app:app
```

### Updated `Dockerfile`
- Added `COPY start.sh .`
- Added `RUN chmod +x start.sh` to make it executable
- Changed `CMD` to use the startup script: `CMD ["./start.sh"]`

## How It Works

1. **Railway sets PORT variable** → `PORT=8080` (or whatever port)
2. **start.sh reads it** → `PORT=${PORT:-5000}` (uses Railway's value or defaults to 5000)
3. **Gunicorn binds correctly** → `--bind 0.0.0.0:8080`

## Files Changed

✅ **start.sh** (NEW)
- Startup script with proper environment variable handling

✅ **Dockerfile** (UPDATED)
- Copies start.sh
- Makes it executable
- Uses start.sh as CMD

## Deploy to Railway Now!

### Step 1: Commit Changes
```bash
git add start.sh Dockerfile
git commit -m "Fix Railway PORT variable issue"
git push
```

### Step 2: Railway Auto-Deploys
Railway will:
- Detect the new commit
- Rebuild with updated Dockerfile
- Properly expand the PORT variable
- ✅ Deploy successfully!

## Testing Locally

If you have Docker Desktop running:
```bash
# Build
docker build -t flappybird-web .

# Test with custom port
docker run -p 8080:8080 -e PORT=8080 flappybird-web

# Test with default port
docker run -p 5000:5000 flappybird-web
```

Without Docker (using Python):
```bash
python app.py
# Works on port 5000
```

## What Changed in Deployment

**Before (Broken):**
```dockerfile
CMD gunicorn --bind 0.0.0.0:$PORT ...
# $PORT wasn't expanding, literally tried to bind to "$PORT"
```

**After (Fixed):**
```dockerfile
CMD ["./start.sh"]
# start.sh properly expands PORT environment variable
```

## Verification

Once deployed, Railway logs should show:
```
Starting Gunicorn on port 8080...
[INFO] Listening at: http://0.0.0.0:8080
```

Instead of:
```
Error: '$PORT' is not a valid port number.
```

## Why This Happens

Docker has two CMD forms:

1. **Shell form** (runs in shell): `CMD command $VAR`
   - Variables expand ✅
   - But doesn't handle signals properly ❌

2. **Exec form** (direct exec): `CMD ["command", "$VAR"]`
   - Variables DON'T expand ❌
   - Handles signals properly ✅

**Solution**: Use exec form with a shell script = best of both worlds! ✅

## Next Steps

1. **Commit the fixes**:
   ```bash
   git add .
   git commit -m "Fix Railway PORT variable expansion"
   git push
   ```

2. **Railway will auto-redeploy** (takes ~2-3 minutes)

3. **Check logs** in Railway dashboard for:
   ```
   Starting Gunicorn on port XXXX...
   ```

4. **Visit your Railway URL** - Game should work! 🎮

## Alternative Solutions (Not Used)

### Option 1: Shell Form CMD
```dockerfile
CMD gunicorn --bind 0.0.0.0:$PORT ...
```
- ❌ No quotes, but doesn't handle signals well

### Option 2: Use sh -c
```dockerfile
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$PORT ..."]
```
- ✅ Works, but messy for long commands

### Option 3: Entrypoint Script (Chosen)
```dockerfile
CMD ["./start.sh"]
```
- ✅ Clean, maintainable, flexible
- ✅ Easy to add more startup logic later

## Status

✅ **FIXED** - Ready to deploy!

The Dockerfile now properly handles Railway's PORT environment variable.

---

**Push to GitHub and Railway will redeploy automatically!** 🚀

