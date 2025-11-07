#!/bin/bash
# Start server script with consistent port handling

echo "=========================================="
echo "YouTube Video Summarizer"
echo "=========================================="
echo ""

# Kill any existing process on common ports
echo "Checking for existing servers..."
for port in 5000 5001 5002; do
    PID=$(lsof -ti:$port 2>/dev/null)
    if [ ! -z "$PID" ]; then
        echo "Found process on port $port (PID: $PID)"
        read -p "Kill it? (y/N): " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            kill -9 $PID 2>/dev/null
            echo "✅ Killed process on port $port"
        fi
    fi
done

echo ""
echo "Starting server..."
echo "=========================================="
echo ""

# Use port 8080 by default to avoid conflicts
export PORT=8080
python3 app.py

