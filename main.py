"""
YouTube Video Summarizer
Main application that extracts YouTube video transcripts and generates summaries.
"""

import sys
# Import config first to ensure .env is loaded for all modules
import config

from transcript_extractor import get_transcript
from summarizer import Summarizer


def main():
    """Main application entry point."""
    print("=" * 60)
    print("YouTube Video Summarizer")
    print("=" * 60)
    print()
    
    # Get YouTube URL from user
    url = input("Enter YouTube video URL: ").strip()
    
    if not url:
        print("Error: No URL provided.")
        sys.exit(1)
    
    print("\n📥 Extracting transcript...")
    try:
        # Extract transcript
        transcript = get_transcript(url)
        print(f"✅ Transcript extracted successfully ({len(transcript)} characters)")
        print()
    except ValueError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error extracting transcript: {e}")
        sys.exit(1)
    
    # Initialize summarizer
    print("🤖 Generating summary with ChatGPT...")
    try:
        summarizer = Summarizer()
        summary = summarizer.summarize(transcript)
        
        print()
        print("=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print()
        print(summary)
        print()
        print("=" * 60)
        
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("\nPlease make sure you have set the OPENAI_API_KEY environment variable.")
        print("You can create a .env file with: OPENAI_API_KEY=your_key_here")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error generating summary: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

