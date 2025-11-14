#!/bin/bash
# Quick start script for YouTube Summarizer

echo "=========================================="
echo "YouTube Summarizer"
echo "=========================================="
echo ""

# Check if dependencies are installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "Installing dependencies..."
    python3 -m pip install -r requirements.txt
    echo ""
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "   Please create .env file with OPENAI_API_KEY=your_key"
    echo ""
fi

echo "Starting web server..."
echo "Note: If port 5000 is in use, another port will be used automatically"
echo "Press Ctrl+C to stop the server"
echo "=========================================="
echo ""

python3 app.py

