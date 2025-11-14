"""Extract and clean YouTube video transcripts."""
import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable


def extract_video_id(url):
    """Extract video ID from YouTube URL."""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
        r'youtube\.com\/watch\?.*v=([^&\n?#]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def validate_youtube_url(url):
    """Validate if input is a YouTube URL."""
    video_id = extract_video_id(url)
    return video_id is not None


def fetch_transcript(video_id):
    """Fetch transcript from YouTube video."""
    try:
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)
        
        # Try to get English transcript first
        try:
            transcript = transcript_list.find_transcript(['en'])
        except NoTranscriptFound:
            # Try any available transcript
            available = list(transcript_list)
            if not available:
                return None
            transcript = available[0]
        
        transcript_data = transcript.fetch()
        return transcript_data
        
    except (VideoUnavailable, TranscriptsDisabled, NoTranscriptFound):
        return None
    except Exception:
        return None


def clean_transcript(transcript_data):
    """Clean and normalize transcript text with timestamps."""
    lines = []
    
    for entry in transcript_data:
        # Handle both dictionary format and FetchedTranscriptSnippet objects
        if hasattr(entry, 'start'):
            # It's a FetchedTranscriptSnippet object
            start = entry.start
            text = str(entry.text).strip() if hasattr(entry, 'text') else ''
        else:
            # It's a dictionary
            start = entry.get('start', 0)
            text = entry.get('text', '').strip()
        
        # Skip empty entries
        if not text or len(text.strip()) == 0:
            continue
        
        # Format timestamp [mm:ss]
        minutes = int(start // 60)
        seconds = int(start % 60)
        timestamp = f"[{minutes:02d}:{seconds:02d}]"
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove empty brackets and musical notation symbols
        text = re.sub(r'\[\s*\]', '', text)  # Remove empty brackets
        text = re.sub(r'♪+', '', text)  # Remove musical note symbols
        
        # Keep more characters including punctuation
        text = re.sub(r'[^\w\s\.,!?;:\-\[\]()\'"]', '', text)
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Skip entries that are just brackets or special characters
        if not text or len(text.strip()) == 0 or text.strip() in ['[]', '[', ']']:
            continue
        
        # Only add if text has meaningful content
        if text and len(text) > 0:
            lines.append(f"{timestamp} {text}")
    
    full_text = ' '.join(lines)
    
    # Remove speaker-stage noise lines like "[music]" (only if clearly bracketed and standalone)
    full_text = re.sub(r'\s+\[music\]\s+', ' ', full_text, flags=re.IGNORECASE)
    full_text = re.sub(r'\s+\[inaudible\]\s+', ' [inaudible] ', full_text, flags=re.IGNORECASE)
    
    # Final whitespace normalization
    full_text = re.sub(r'\s+', ' ', full_text).strip()
    
    return full_text

