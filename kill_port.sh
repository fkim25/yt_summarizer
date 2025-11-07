#!/bin/bash
# Script to kill process running on port 5000

PORT=${1:-5000}

echo "Checking for processes on port $PORT..."

# Find process ID using the port
PID=$(lsof -ti:$PORT 2>/dev/null)

if [ -z "$PID" ]; then
    echo "No process found on port $PORT"
    exit 0
fi

echo "Found process(es) on port $PORT:"
lsof -i:$PORT

echo ""
read -p "Do you want to kill the process(es) on port $PORT? (y/N): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    kill -9 $PID
    echo "✅ Killed process(es) on port $PORT"
else
    echo "Cancelled."
fi

