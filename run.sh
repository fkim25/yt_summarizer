#!/bin/bash
# Quick start script for YouTube Video Summarizer

echo "=========================================="
echo "YouTube Video Summarizer"
echo "=========================================="
echo ""

# Check if Flask is installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "Installing dependencies..."
    python3 -m pip install -r requirements.txt
    echo ""
fi

# Check if .env file exists and has content
if [ ! -f .env ] || [ ! -s .env ]; then
    echo "⚠️  Warning: .env file is missing or empty!"
    echo "   Run: python3 setup_env.py"
    echo "   Or: python3 check_env.py"
    echo ""
fi

echo "Starting web server..."
echo "Note: If port 5000 is in use, the app will automatically use another port"
echo "Press Ctrl+C to stop the server"
echo "=========================================="
echo ""

python3 app.py

