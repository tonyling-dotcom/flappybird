#!/bin/bash
echo "Starting Flappy Bird Web Server..."
echo ""
echo "Visit http://localhost:5000 in your browser"
echo "Press Ctrl+C to stop the server"
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Start the Flask app
python app.py

