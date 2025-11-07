"""
Flask Web Application for YouTube Video Summarizer
"""

from flask import Flask, render_template, request, jsonify
import sys
import socket
import os

# Import config first to ensure .env is loaded
import config

from transcript_extractor import get_transcript
from summarizer import Summarizer

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Initialize summarizer (will be created per request to handle errors gracefully)
summarizer = None

def get_summarizer():
    """Get or create summarizer instance."""
    global summarizer
    if summarizer is None:
        try:
            summarizer = Summarizer()
        except ValueError as e:
            # API key not configured
            return None
    return summarizer


@app.route('/')
def index():
    """Render the main page - serves standalone HTML file."""
    from pathlib import Path
    from flask import Response
    
    # Serve the standalone index.html file
    standalone_html = Path(__file__).parent / 'index.html'
    if standalone_html.exists():
        try:
            with open(standalone_html, 'r', encoding='utf-8') as f:
                html_content = f.read()
            return Response(html_content, mimetype='text/html')
        except Exception as e:
            return f"Error loading HTML: {str(e)}", 500
    else:
        # Fallback to template if standalone doesn't exist
        try:
            return render_template('index.html')
        except Exception as e:
            return f"Error: {str(e)}. Please ensure index.html exists in the project root.", 500


@app.route('/api/summarize', methods=['POST'])
def summarize():
    """API endpoint to summarize a YouTube video."""
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({
                'success': False,
                'error': 'Please provide a YouTube URL'
            }), 400
        
        # Step 1: Extract transcript
        try:
            transcript = get_transcript(url)
            transcript_length = len(transcript)
        except ValueError as e:
            return jsonify({
                'success': False,
                'error': f'Invalid URL: {str(e)}'
            }), 400
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Failed to extract transcript: {str(e)}'
            }), 500
        
        # Step 2: Generate summary
        summarizer_instance = get_summarizer()
        if summarizer_instance is None:
            return jsonify({
                'success': False,
                'error': 'OpenAI API key not configured. Please check your .env file.'
            }), 500
        
        try:
            summary = summarizer_instance.summarize(transcript)
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Failed to generate summary: {str(e)}'
            }), 500
        
        return jsonify({
            'success': True,
            'transcript_length': transcript_length,
            'summary': summary,
            'transcript_preview': transcript[:500] + '...' if len(transcript) > 500 else transcript
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    try:
        summarizer_instance = get_summarizer()
        api_key_configured = summarizer_instance is not None
    except Exception:
        api_key_configured = False
    
    return jsonify({
        'status': 'ok',
        'api_key_configured': api_key_configured
    })


if __name__ == '__main__':
    import socket
    import os
    
    def find_free_port(start_port=5000, max_port=5100):
        """Find a free port starting from start_port."""
        for port in range(start_port, max_port):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('', port))
                    return port
            except OSError:
                continue
        return None
    
    # Try to use port 5000, or find a free port
    # Use environment variable PORT if set, otherwise try 5000, then find free
    port_env = os.getenv('PORT')
    if port_env:
        port = int(port_env)
    else:
        port = 5000
    
    # Check if the port is available
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', port))
    except OSError:
        # Port is in use, find a free port
        if port == 5000:
            print("⚠️  Port 5000 is already in use. Finding an available port...")
        else:
            print(f"⚠️  Port {port} is already in use. Finding an available port...")
        port = find_free_port(5001, 5100)
        if port is None:
            print("❌ Error: Could not find an available port (5001-5100)")
            print("   Try setting PORT environment variable: PORT=8080 python3 app.py")
            sys.exit(1)
        print(f"✅ Using port {port} instead")
    
    print("=" * 60)
    print("YouTube Video Summarizer - Web Application")
    print("=" * 60)
    print()
    print(f"🚀 Server starting on port {port}...")
    print()
    print(f"📍 Open your browser and navigate to:")
    print(f"   http://localhost:{port}")
    print(f"   or")
    print(f"   http://127.0.0.1:{port}")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    # Disable debug mode reloader to prevent port changes on restart
    # Set use_reloader=False or use debug=False for production-like behavior
    app.run(debug=True, host='127.0.0.1', port=port, use_reloader=False)

