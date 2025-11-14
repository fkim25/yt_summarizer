# YouTube Summarizer Pipeline

Autonomous pipeline for YouTube URL → transcript → chunk → ChatGPT summarization → final summary JSON.

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. API key is already configured in `.env` file.

## Usage

### Web Interface (Recommended)

Start the web server:
```bash
python app.py
```

Then open your browser to the URL shown (usually `http://localhost:5000`).

The web interface provides:
- 📺 Easy YouTube URL input
- ⚡ Real-time processing status
- 📊 Formatted summary display
- 🎯 Key takeaways and highlights
- 📋 Raw JSON view

### Command Line

```bash
python main.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

Or run interactively:
```bash
python main.py
```

## Output

Returns JSON response with either:
- **Success**: Final synthesis JSON with summary, key takeaways, highlights, next steps, confidence level
- **Error**: Error JSON with error_code and message

## Pipeline Steps

1. Validates YouTube URL
2. Extracts video ID
3. Fetches transcript from YouTube (English preferred, falls back to any available)
4. Cleans and normalizes transcript (preserves timestamps `[mm:ss]`)
5. Chunks transcript (~12,000 chars per chunk with 300 char overlap)
6. Summarizes each chunk using ChatGPT (temperature=0.0)
7. Synthesizes all chunks into final summary
8. Returns final JSON

## Features

- ✅ Deterministic pipeline
- ✅ Error handling with specific error codes
- ✅ Transcript chunking with overlap
- ✅ Factual summarization (no outside knowledge)
- ✅ Timestamp preservation
- ✅ Confidence levels
