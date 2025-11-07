# Quick Start Guide

## Step 1: Stop any running servers
Press `Ctrl+C` in the terminal where the server is running.

## Step 2: Start the server
```bash
python3 app.py
```

## Step 3: Check the terminal output
You'll see a message like:
```
🚀 Server starting on port 5001...
📍 Open your browser and navigate to:
   http://localhost:5001
```

## Step 4: Open that exact URL in your browser
Copy and paste the URL shown in the terminal into your browser.

## Troubleshooting

### If "page can't be reached":
1. Make sure the server is still running (check the terminal)
2. Use the EXACT URL shown in the terminal (including the port number)
3. Try `http://127.0.0.1:PORT` instead of `http://localhost:PORT`
4. Make sure you're not using a proxy or VPN that blocks localhost

### If port is already in use:
```bash
# Use a specific port
PORT=8080 python3 app.py
```

### To kill processes on ports:
```bash
./kill_port.sh 5000
./kill_port.sh 5001
./kill_port.sh 5002
```

## Important Notes
- The server must be running for the page to load
- Use the URL shown in the terminal (port number is important!)
- Don't close the terminal while using the app

