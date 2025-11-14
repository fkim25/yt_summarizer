"""Flask web application for YouTube Summarizer Pipeline."""
from flask import Flask, render_template_string, request, jsonify
import json
import traceback
from main import process_youtube_url

app = Flask(__name__)

# HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Summarizer</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 900px;
            width: 100%;
            padding: 40px;
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        .subtitle {
            color: #666;
            text-align: center;
            margin-bottom: 30px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 600;
        }
        input[type="text"] {
            width: 100%;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input[type="text"]:focus {
            outline: none;
            border-color: #667eea;
        }
        button {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }
        button:hover:not(:disabled) {
            transform: translateY(-2px);
        }
        button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        .status {
            margin-top: 20px;
            padding: 15px;
            border-radius: 10px;
            display: none;
        }
        .status.info {
            background: #e3f2fd;
            color: #1976d2;
            border: 1px solid #90caf9;
        }
        .status.error {
            background: #ffebee;
            color: #c62828;
            border: 1px solid #ef5350;
        }
        .result {
            margin-top: 30px;
            display: none;
        }
        .result-box {
            background: #f5f5f5;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 15px;
        }
        .result-box h2 {
            color: #333;
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        .result-box p, .result-box ul {
            color: #555;
            line-height: 1.8;
            margin-bottom: 10px;
        }
        .result-box ul {
            padding-left: 25px;
        }
        .result-box li {
            margin-bottom: 8px;
        }
        .highlight {
            background: #fff3cd;
            padding: 15px;
            border-radius: 8px;
            margin-top: 10px;
            border-left: 4px solid #ffc107;
        }
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255,255,255,0.3);
            border-top-color: white;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
            margin-right: 10px;
            vertical-align: middle;
        }
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        pre {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
            font-size: 14px;
            line-height: 1.6;
        }
        .json-view {
            background: #282c34;
            color: #abb2bf;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            font-size: 13px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📺 YouTube Summarizer</h1>
        <p class="subtitle">AI-Powered Video Summary Pipeline</p>

        <form id="summarizeForm">
            <div class="form-group">
                <label for="videoUrl">YouTube Video URL:</label>
                <input 
                    type="text" 
                    id="videoUrl" 
                    name="url" 
                    placeholder="https://www.youtube.com/watch?v=..." 
                    required
                >
            </div>
            <button type="submit" id="submitBtn">
                <span id="btnText">Summarize</span>
                <span id="btnLoader" class="loading" style="display: none;"></span>
            </button>
        </form>

        <div id="status" class="status"></div>

        <div id="result" class="result">
            <div class="result-box">
                <h2>Summary</h2>
                <div id="summaryContent"></div>
            </div>
            <div class="result-box">
                <h2>Key Takeaways</h2>
                <ul id="takeawaysContent"></ul>
            </div>
            <div class="result-box">
                <h2>Highlights</h2>
                <div id="highlightsContent"></div>
            </div>
            <div class="result-box">
                <h2>Next Steps</h2>
                <ul id="nextStepsContent"></ul>
            </div>
            <div class="result-box">
                <h2>Raw JSON Response</h2>
                <pre class="json-view" id="jsonContent"></pre>
            </div>
        </div>
    </div>

    <script>
        const form = document.getElementById('summarizeForm');
        const videoUrlInput = document.getElementById('videoUrl');
        const submitBtn = document.getElementById('submitBtn');
        const btnText = document.getElementById('btnText');
        const btnLoader = document.getElementById('btnLoader');
        const status = document.getElementById('status');
        const result = document.getElementById('result');

        function setLoading(loading) {
            submitBtn.disabled = loading;
            if (loading) {
                btnText.textContent = 'Processing...';
                btnLoader.style.display = 'inline-block';
            } else {
                btnText.textContent = 'Summarize';
                btnLoader.style.display = 'none';
            }
        }

        function showStatus(message, type) {
            status.textContent = message;
            status.className = 'status ' + type;
            status.style.display = 'block';
            result.style.display = 'none';
        }

        function hideStatus() {
            status.style.display = 'none';
        }

        function displayResult(data) {
            hideStatus();
            
            // Display summary
            document.getElementById('summaryContent').innerHTML = 
                '<p>' + (data.final_short_summary || 'N/A') + '</p>' +
                '<p><strong>Confidence:</strong> ' + (data.confidence || 'N/A') + '</p>';

            // Display takeaways
            const takeaways = data.final_key_takeaways || [];
            const takeawaysHTML = takeaways.map(t => '<li>' + t + '</li>').join('');
            document.getElementById('takeawaysContent').innerHTML = takeawaysHTML || '<li>No takeaways available</li>';

            // Display highlights
            const highlights = data.highlights || [];
            let highlightsHTML = '';
            if (highlights.length > 0) {
                highlightsHTML = highlights.map(h => 
                    '<div class="highlight"><strong>[' + (h.time || '') + ']</strong> ' + h.quote + '</div>'
                ).join('');
            } else {
                highlightsHTML = '<p>No highlights available</p>';
            }
            document.getElementById('highlightsContent').innerHTML = highlightsHTML;

            // Display next steps
            const nextSteps = data.next_steps || [];
            const nextStepsHTML = nextSteps.map(s => '<li>' + s + '</li>').join('');
            document.getElementById('nextStepsContent').innerHTML = nextStepsHTML || '<li>No next steps available</li>';

            // Display raw JSON
            document.getElementById('jsonContent').textContent = JSON.stringify(data, null, 2);

            result.style.display = 'block';
        }

        function displayError(errorData) {
            showStatus('Error: ' + (errorData.message || 'Unknown error occurred'), 'error');
        }

        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const url = videoUrlInput.value.trim();
            if (!url) {
                showStatus('Please enter a YouTube URL', 'error');
                return;
            }

            setLoading(true);
            showStatus('Processing... This may take a few moments.', 'info');

            try {
                const response = await fetch('/api/summarize', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ url: url })
                });

                const data = await response.json();
                
                if (data.status === 'error') {
                    displayError(data);
                } else if (data.status === 'ok') {
                    displayResult(data);
                } else {
                    displayError({ message: 'Unexpected response format' });
                }
            } catch (error) {
                showStatus('Network error: ' + error.message, 'error');
            } finally {
                setLoading(false);
            }
        });
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    """Render the main page."""
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/summarize', methods=['POST'])
def summarize():
    """API endpoint to summarize YouTube video."""
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({
                "status": "error",
                "error_code": "invalid_url",
                "message": "Input is not a valid YouTube URL."
            }), 400
        
        # Process the URL through the pipeline
        result_json = process_youtube_url(url)
        result = json.loads(result_json)
        
        return jsonify(result)
        
    except json.JSONDecodeError as e:
        return jsonify({
            "status": "error",
            "error_code": "unknown_error",
            "message": f"Invalid JSON response: {str(e)}"
        }), 500
    except Exception as e:
        return jsonify({
            "status": "error",
            "error_code": "unknown_error",
            "message": f"Unexpected error: {str(e)}"
        }), 500


if __name__ == '__main__':
    import socket
    import os
    
    def find_free_port(start_port=5000, max_port=5100):
        """Find a free port."""
        for port in range(start_port, max_port):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('', port))
                    return port
            except OSError:
                continue
        return None
    
    port = int(os.getenv('PORT', 5000))
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', port))
    except OSError:
        port = find_free_port(5001, 5100)
        if port is None:
            print("❌ Error: Could not find an available port")
            exit(1)
        print(f"⚠️  Port 5000 in use. Using port {port} instead")
    
    print("=" * 60)
    print("YouTube Summarizer - Web Application")
    print("=" * 60)
    print(f"\n🚀 Server starting on port {port}...")
    print(f"📍 Open your browser: http://localhost:{port}")
    print("\nPress Ctrl+C to stop")
    print("=" * 60)
    
    app.run(debug=True, host='127.0.0.1', port=port, use_reloader=False)

