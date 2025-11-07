"""
YouTube Transcript Extractor
Extracts raw transcript text from YouTube videos.
"""

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
import re


# Add get_transcript as a static method for compatibility with expected API
# This wrapper uses the new API (list/fetch) internally
def _get_transcript_wrapper(video_id, languages=None):
    """
    Compatibility wrapper for YouTubeTranscriptApi.get_transcript()
    Uses the new API (list/fetch) internally with better error handling.
    
    Args:
        video_id: YouTube video ID
        languages: List of language codes (default: ['en'])
        
    Returns:
        List of transcript dictionaries with 'text', 'start', and 'duration' keys
    """
    import time
    import random
    
    if languages is None:
        languages = ['en']
    
    api = YouTubeTranscriptApi()
    
    # Try multiple times with different approaches
    max_retries = 3
    for attempt in range(max_retries):
        try:
            transcript_list = api.list(video_id)
            
            # Try to find transcript in requested languages
            transcript = None
            try:
                transcript = transcript_list.find_transcript(languages)
            except NoTranscriptFound:
                # Try any available transcript
                available = list(transcript_list)
                if available:
                    # Prefer manually created over auto-generated
                    try:
                        manual = [t for t in available if not t.is_generated]
                        if manual:
                            transcript = manual[0]
                        else:
                            # Use auto-generated if available
                            auto = [t for t in available if t.is_generated]
                            if auto:
                                transcript = auto[0]
                            else:
                                transcript = available[0]
                    except:
                        transcript = available[0]
                else:
                    raise NoTranscriptFound(f"No transcripts available for video: {video_id}")
            
            if transcript:
                # Fetch with retry logic for XML parsing errors
                try:
                    transcript_data = transcript.fetch()
                except Exception as fetch_error:
                    error_str = str(fetch_error).lower()
                    if "no element found" in error_str or "xml" in error_str or "parse" in error_str:
                        if attempt < max_retries - 1:
                            # Wait a bit and retry
                            time.sleep(1 + random.uniform(0, 1))
                            continue
                        else:
                            # Last attempt failed, try translating to English if available
                            try:
                                if transcript.language_code != 'en':
                                    transcript = transcript.translate('en')
                                    transcript_data = transcript.fetch()
                                else:
                                    raise Exception("YouTube returned invalid XML response. The video may not have transcripts available.")
                            except:
                                raise Exception(
                                    f"Failed to fetch transcript after {max_retries} attempts. "
                                    f"This video may not have transcripts, or YouTube is temporarily blocking requests. "
                                    f"Please try a different video or try again later."
                                )
                    else:
                        raise
            
            # Convert to list of dicts for compatibility
            result = []
            for snippet in transcript_data:
                result.append({
                    'text': snippet.text,
                    'start': snippet.start,
                    'duration': snippet.duration
                })
            
            if not result:
                raise NoTranscriptFound(f"Transcript is empty for video: {video_id}")
            
            return result
            
        except (VideoUnavailable, TranscriptsDisabled, NoTranscriptFound) as e:
            # Don't retry these errors
            raise
        except Exception as e:
            error_msg = str(e).lower()
            if "no element found" in error_msg or "xml" in error_msg:
                if attempt < max_retries - 1:
                    time.sleep(1 + random.uniform(0, 1))
                    continue
                else:
                    raise Exception(
                        f"Failed to extract transcript. YouTube returned an invalid response.\n"
                        f"This might be because:\n"
                        f"1. The video doesn't have transcripts/captions enabled\n"
                        f"2. YouTube is temporarily blocking the request\n"
                        f"3. The video is restricted or unavailable\n\n"
                        f"Try a different video that you know has captions enabled."
                    )
            raise
    
    raise Exception("Failed to extract transcript after multiple attempts")


# For newer versions of youtube-transcript-api (1.2.0+), get_transcript is built-in
# For older versions, we use our wrapper function
if not hasattr(YouTubeTranscriptApi, 'get_transcript'):
    YouTubeTranscriptApi.get_transcript = staticmethod(_get_transcript_wrapper)


def extract_video_id(url):
    """
    Extract video ID from various YouTube URL formats.
    
    Args:
        url: YouTube URL (various formats supported)
        
    Returns:
        Video ID string or None if invalid
    """
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
        r'youtube\.com\/watch\?.*v=([^&\n?#]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def get_transcript(url, languages=['en']):
    """
    Get transcript from YouTube video.
    
    Args:
        url: YouTube video URL
        languages: List of language codes (default: ['en'])
        
    Returns:
        Raw transcript text as string
        
    Raises:
        ValueError: If URL is invalid
        TranscriptsDisabled: If transcripts are disabled for the video
        NoTranscriptFound: If no transcript found in specified languages
        VideoUnavailable: If video is unavailable
    """
    video_id = extract_video_id(url)
    
    if not video_id:
        raise ValueError(f"Invalid YouTube URL: {url}")
    
    try:
        # Use our wrapper which has better error handling
        # This avoids the XML parsing issues by using the list/fetch API directly
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
        
        if not transcript_list:
            raise NoTranscriptFound(f"No transcript data retrieved for video: {url}")
        
        # Combine all transcript entries into a single text
        transcript_text = ' '.join([entry['text'] for entry in transcript_list])
        
        if not transcript_text or len(transcript_text.strip()) == 0:
            raise NoTranscriptFound(f"Transcript is empty for video: {url}")
        
        return transcript_text
    
    except TranscriptsDisabled as e:
        raise TranscriptsDisabled(f"Transcripts are disabled for video: {url}. {str(e)}")
    except NoTranscriptFound as e:
        raise NoTranscriptFound(f"No transcript found for video: {url}. {str(e)}")
    except VideoUnavailable as e:
        raise VideoUnavailable(f"Video is unavailable: {url}. {str(e)}")
    except Exception as e:
        # Provide more helpful error messages
        error_msg = str(e)
        error_lower = error_msg.lower()
        
        if "no element found" in error_lower or "xml" in error_lower or "parse" in error_lower:
            raise Exception(
                f"Failed to extract transcript from {url}.\n\n"
                f"Possible reasons:\n"
                f"1. The video doesn't have transcripts/captions enabled\n"
                f"2. YouTube is temporarily blocking requests\n"
                f"3. The video is restricted or unavailable\n\n"
                f"Please try:\n"
                f"- A different video that has captions enabled\n"
                f"- Waiting a few minutes and trying again\n"
                f"- Checking if the video has subtitles available on YouTube"
            )
        raise Exception(f"Error extracting transcript: {error_msg}")

