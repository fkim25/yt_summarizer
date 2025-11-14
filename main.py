"""Main pipeline for YouTube URL → transcript → chunk → summarize → final JSON."""
import json
import sys
from transcript_extractor import validate_youtube_url, extract_video_id, fetch_transcript, clean_transcript
from chunker import chunk_transcript
from summarizer import summarize_chunk, synthesize_chunks


def get_video_title(video_id):
    """Attempt to fetch video title (optional, can return empty string)."""
    # This could use YouTube Data API if available
    # For now, return empty string
    return ""


def process_youtube_url(user_input):
    """
    Process YouTube URL through the complete pipeline.
    
    Returns:
        JSON string with final result or error
    """
    # Step 1: Validate input
    if not validate_youtube_url(user_input):
        return json.dumps({
            "status": "error",
            "error_code": "invalid_url",
            "message": "Input is not a valid YouTube URL."
        }, indent=2)
    
    # Step 2: Extract video ID
    video_id = extract_video_id(user_input)
    
    # Step 3: Fetch transcript
    try:
        transcript_data = fetch_transcript(video_id)
        if transcript_data is None:
            return json.dumps({
                "status": "error",
                "error_code": "no_transcript",
                "message": "No transcript or captions found for this video."
            }, indent=2)
    except Exception as e:
        return json.dumps({
            "status": "error",
            "error_code": "unknown_error",
            "message": f"Error fetching transcript: {str(e)}"
        }, indent=2)
    
    # Step 4: Clean & normalize
    try:
        transcript_text = clean_transcript(transcript_data)
        
        if len(transcript_text) < 50:
            return json.dumps({
                "status": "error",
                "error_code": "transcript_too_short",
                "message": "Transcript appears too short."
            }, indent=2)
    except Exception as e:
        return json.dumps({
            "status": "error",
            "error_code": "unknown_error",
            "message": f"Error cleaning transcript: {str(e)}"
        }, indent=2)
    
    # Step 5: Chunk the transcript
    try:
        chunks = chunk_transcript(transcript_text)
    except Exception as e:
        return json.dumps({
            "status": "error",
            "error_code": "unknown_error",
            "message": f"Error chunking transcript: {str(e)}"
        }, indent=2)
    
    # Step 6: Summarize each chunk
    chunk_summaries = []
    for chunk in chunks:
        try:
            summary = summarize_chunk(chunk, retry_count=1)
            if summary is None:
                return json.dumps({
                    "status": "error",
                    "error_code": "chunk_summarization_failed",
                    "failed_chunk": chunk["index"],
                    "message": "Chunk summarization returned invalid output."
                }, indent=2)
            chunk_summaries.append(summary)
        except Exception as e:
            # Check for rate limit
            error_str = str(e).lower()
            if "rate limit" in error_str or "429" in error_str:
                return json.dumps({
                    "status": "error",
                    "error_code": "api_rate_limit",
                    "message": "Upstream API rate limit or network error."
                }, indent=2)
            return json.dumps({
                "status": "error",
                "error_code": "chunk_summarization_failed",
                "failed_chunk": chunk["index"],
                "message": f"Chunk summarization failed: {str(e)}"
            }, indent=2)
    
    # Step 7: Synthesize chunks
    try:
        title = get_video_title(video_id)
        final_result = synthesize_chunks(chunk_summaries, video_id, user_input, title, retry_count=1)
        
        if final_result is None:
            return json.dumps({
                "status": "error",
                "error_code": "synthesis_failed",
                "message": "Synthesis step failed to produce valid JSON."
            }, indent=2)
        
        # Step 8: Return final JSON
        return json.dumps(final_result, indent=2)
        
    except Exception as e:
        error_str = str(e).lower()
        if "rate limit" in error_str or "429" in error_str:
            return json.dumps({
                "status": "error",
                "error_code": "api_rate_limit",
                "message": "Upstream API rate limit or network error."
            }, indent=2)
        return json.dumps({
            "status": "error",
            "error_code": "synthesis_failed",
            "message": f"Synthesis failed: {str(e)}"
        }, indent=2)


if __name__ == "__main__":
    # Get user input
    if len(sys.argv) > 1:
        user_input = sys.argv[1]
    else:
        user_input = input("Enter YouTube URL: ").strip()
    
    # Process and output JSON
    result = process_youtube_url(user_input)
    print(result)

