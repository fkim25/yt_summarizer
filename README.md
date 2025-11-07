# YouTube Video Summarizer

An AI-powered agent that extracts transcripts from YouTube videos and generates concise summaries using ChatGPT API.

## Features

- 📺 Extract transcripts from YouTube videos
- 🤖 Generate AI-powered summaries using OpenAI's ChatGPT API
- 🔍 Supports various YouTube URL formats
- ⚡ Fast and efficient processing
- 🎯 Handles multiple languages and auto-generated transcripts

## Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd yt_summarizer
```

2. Install dependencies:
```bash
python3 -m pip install -r requirements.txt
```

   This will install:
   - `youtube-transcript-api` - For extracting YouTube video transcripts
   - `openai` - For ChatGPT API integration
   - `python-dotenv` - For loading environment variables
   - `flask` - For the web interface
   
   Or install packages individually:
```bash
python3 -m pip install youtube-transcript-api openai python-dotenv flask
```

3. Set up your OpenAI API key:

   **Option 1: Use the setup script (Recommended)**
   ```bash
   python3 setup_env.py
   ```
   This will interactively guide you through setting up your `.env` file.

   **Option 2: Manually create `.env` file**
   
   Create a `.env` file in the project root:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   ```
   
   **Important:** 
   - Do NOT use quotes around the API key
   - Do NOT add spaces around the `=` sign (or keep it consistent)
   - The file should contain exactly: `OPENAI_API_KEY=sk-...`

   **Option 3: Set as environment variable**
   ```bash
   export OPENAI_API_KEY=your_openai_api_key_here
   ```

   **Verify your setup:**
   ```bash
   python3 check_env.py
   ```
   This will diagnose any issues with your `.env` file configuration.

## Usage

### Web Interface (Recommended)

**Quick Start:**
```bash
./run.sh
```

Or manually:
```bash
python3 app.py
```

Then open your browser and navigate to the URL shown in the terminal (usually `http://localhost:5000` or another port if 5000 is in use).

**Note:** If port 5000 is already in use, the application will automatically find and use an available port (5001, 5002, etc.). Check the terminal output for the correct URL.

The web interface provides:
- 🎨 Modern, beautiful UI
- 📱 Responsive design (works on mobile)
- ⚡ Real-time status updates
- 📊 Transcript preview
- ✨ Smooth animations and transitions

### Command Line Interface

Alternatively, you can use the CLI version:
```bash
python3 main.py
```

Then enter a YouTube video URL when prompted:
```
Enter YouTube video URL: https://www.youtube.com/watch?v=VIDEO_ID
```

The application will:
1. Extract the video transcript
2. Send it to ChatGPT API for processing
3. Display the generated summary

## Example

```
$ python main.py
============================================================
YouTube Video Summarizer
============================================================

Enter YouTube video URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ

📥 Extracting transcript...
✅ Transcript extracted successfully (12345 characters)

🤖 Generating summary with ChatGPT...

============================================================
SUMMARY
============================================================

[Summary will appear here]

============================================================
```

## Project Structure

```
yt_summarizer/
├── app.py                   # Flask web application
├── main.py                  # CLI application entry point
├── transcript_extractor.py  # YouTube transcript extraction
├── summarizer.py            # ChatGPT API integration
├── config.py                # Configuration module (loads .env)
├── setup_env.py             # Helper script to set up .env file
├── check_env.py             # Diagnostic script to check .env configuration
├── requirements.txt         # Python dependencies
├── templates/               # HTML templates
│   └── index.html          # Main web interface
├── static/                  # Static files
│   ├── css/
│   │   └── style.css       # Stylesheet
│   └── js/
│       └── main.js         # JavaScript for interactivity
├── .env                     # Environment variables (create this)
└── README.md               # This file
```

## How It Works

1. **Transcript Extraction**: Uses `youtube-transcript-api` to fetch video transcripts
2. **Text Processing**: Combines transcript entries into raw text
3. **AI Summarization**: Sends text to OpenAI's ChatGPT API with a summarization prompt
4. **Output**: Displays the generated summary to the user

## Supported URL Formats

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`

## Error Handling

The application handles various error cases:
- Invalid YouTube URLs
- Videos with disabled transcripts
- Unavailable videos
- Missing OpenAI API key
- API errors

## Configuration

You can customize the summarization by modifying `summarizer.py`:
- Change the model (default: `gpt-4o-mini`)
- Adjust `max_tokens` for summary length
- Modify the system prompt for different summary styles

## License

See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
