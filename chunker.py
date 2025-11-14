"""Chunk transcript text with overlap and sentence boundaries."""
import re


def chunk_transcript(text, target_chars=12000, overlap_chars=300):
    """
    Chunk transcript text into overlapping segments.
    
    Args:
        text: Full transcript text
        target_chars: Target characters per chunk (default 12000)
        overlap_chars: Overlap between chunks (default 300)
    
    Returns:
        List of chunk dicts: [{index: int, total: int, text: str}, ...]
    """
    if len(text) <= target_chars:
        return [{"index": 1, "total": 1, "text": text}]
    
    chunks = []
    current_pos = 0
    chunk_index = 1
    text_length = len(text)
    
    while current_pos < text_length:
        chunk_end = current_pos + target_chars
        
        if chunk_end >= text_length:
            # Last chunk
            chunk_text = text[current_pos:].strip()
            if chunk_text:
                chunks.append({
                    "index": chunk_index,
                    "total": len(chunks) + 1,  # Will be updated at end
                    "text": chunk_text
                })
            break
        
        # Try to split at sentence boundary
        chunk_text = text[current_pos:chunk_end]
        
        # Look for sentence endings (. ! ?) followed by space or timestamp pattern
        sentence_end = max(
            chunk_text.rfind('. '),
            chunk_text.rfind('! '),
            chunk_text.rfind('? '),
            chunk_text.rfind('.\n'),
            chunk_text.rfind('!\n'),
            chunk_text.rfind('?\n'),
        )
        
        # Also look for timestamp pattern [mm:ss]
        timestamp_pattern = re.search(r'\[\d{2}:\d{2}\]', chunk_text[::-1])
        if timestamp_pattern:
            timestamp_pos = len(chunk_text) - timestamp_pattern.start()
            if timestamp_pos > target_chars - 500:  # If timestamp is near end
                sentence_end = max(sentence_end, timestamp_pos)
        
        if sentence_end > target_chars * 0.7:  # Only use if it's not too early
            chunk_text = chunk_text[:sentence_end + 1].strip()
            chunk_end = current_pos + len(chunk_text)
        else:
            # Force split, but try to avoid breaking mid-word
            last_space = chunk_text.rfind(' ')
            if last_space > target_chars * 0.9:
                chunk_text = chunk_text[:last_space].strip()
                chunk_end = current_pos + len(chunk_text)
            else:
                chunk_text = chunk_text.strip()
        
        if chunk_text:
            chunks.append({
                "index": chunk_index,
                "total": 0,  # Will be updated at end
                "text": chunk_text
            })
            chunk_index += 1
        
        # Move position back by overlap
        current_pos = chunk_end - overlap_chars
        if current_pos < 0:
            current_pos = chunk_end
    
    # Update total count for all chunks
    total = len(chunks)
    for chunk in chunks:
        chunk["total"] = total
    
    return chunks

