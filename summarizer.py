"""Summarize chunks and synthesize final summary using OpenAI API."""
import json
import re
from openai import OpenAI
from config import get_openai_api_key


def get_openai_client():
    """Get OpenAI client instance."""
    import httpx
    api_key = get_openai_api_key()
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment")
    
    # Create custom httpx client to avoid proxies parameter issue
    # This bypasses the internal SyncHttpxClientWrapper that has compatibility issues
    http_client = httpx.Client(timeout=60.0)
    
    # Initialize OpenAI client with custom http_client
    return OpenAI(api_key=api_key, http_client=http_client, max_retries=2)


def extract_json_from_response(text):
    """Extract JSON from response, handling markdown code blocks."""
    # Remove markdown code blocks if present
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*', '', text)
    text = text.strip()
    
    # Try to find JSON object
    json_match = re.search(r'\{.*\}', text, re.DOTALL)
    if json_match:
        return json_match.group(0)
    return text


def summarize_chunk(chunk_data, retry_count=1):
    """
    Summarize a single chunk using OpenAI API.
    
    Args:
        chunk_data: Dict with index, total, text
        retry_count: Number of retries on failure
    
    Returns:
        Dict with chunk summary JSON or None on failure
    """
    client = get_openai_client()
    
    chunk_prompt = f"""---BEGIN TRANSCRIPT---

{chunk_data['text']}

---END TRANSCRIPT---



TASK (output JSON):

{{
  "chunk_index": {chunk_data['index']},
  "chunk_total": {chunk_data['total']},
  "chunk_summary": "<1-2 sentence factual summary>",
  "key_points": ["short bullet 1","short bullet 2", "..."],
  "notable_quotes": [{{"time":"mm:ss","quote":"..."}}],
  "claims_numbers": ["exact quoted claim or number","..."],
  "verify_flags": ["phrase or claim to verify","..."]
}}"""
    
    system_message = """You are a strict transcript chunk summarizer. Only use the text inside ---BEGIN TRANSCRIPT--- and ---END TRANSCRIPT---. Do NOT add outside knowledge, do NOT infer unstated facts. Return VALID JSON ONLY matching the schema."""
    
    for attempt in range(retry_count + 1):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": chunk_prompt}
                ],
                temperature=0.0,
                max_tokens=1024,
                response_format={"type": "json_object"}
            )
            
            response_text = response.choices[0].message.content.strip()
            json_str = extract_json_from_response(response_text)
            result = json.loads(json_str)
            
            # Validate required fields
            required_fields = ["chunk_index", "chunk_total", "chunk_summary", "key_points", 
                             "notable_quotes", "claims_numbers", "verify_flags"]
            if all(field in result for field in required_fields):
                return result
            
        except json.JSONDecodeError:
            if attempt < retry_count:
                continue
        except Exception as e:
            if attempt < retry_count:
                continue
    
    return None


def synthesize_chunks(chunks_json_array, video_id, original_url, title="", retry_count=1):
    """
    Synthesize chunk summaries into final summary.
    
    Args:
        chunks_json_array: List of chunk summary dicts
        video_id: YouTube video ID
        original_url: Original YouTube URL
        title: Video title (if available)
        retry_count: Number of retries on failure
    
    Returns:
        Final synthesis dict or None on failure
    """
    client = get_openai_client()
    
    chunks_json_str = json.dumps(chunks_json_array, indent=2)
    
    synthesis_prompt = f"""Here is the array:

{chunks_json_str}



TASK (output JSON):

{{
  "status": "ok",
  "video_id": "{video_id}",
  "video_url": "{original_url}",
  "title": "{title}",
  "final_short_summary": "<2-3 sentence summary>",
  "final_key_takeaways": ["takeaway 1","takeaway 2", "..."],
  "top_claims_numbers": ["..."],
  "highlights": [{{"time":"mm:ss","quote":"..."}}],
  "next_steps": ["action 1","action 2","action 3"],
  "confidence": "<All claims are transcript-supported | Most claims are transcript-supported | Several claims require verification>",
  "chunks_count": {len(chunks_json_array)}
}}"""
    
    system_message = """You are an expert synthesizer. Use only the provided chunk JSON array. Do NOT re-open the original transcript; rely only on chunk summaries and fields. Return VALID JSON ONLY."""
    
    for attempt in range(retry_count + 1):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": synthesis_prompt}
                ],
                temperature=0.0,
                max_tokens=2048,
                response_format={"type": "json_object"}
            )
            
            response_text = response.choices[0].message.content.strip()
            json_str = extract_json_from_response(response_text)
            result = json.loads(json_str)
            
            # Validate required fields
            required_fields = ["status", "video_id", "video_url", "title", "final_short_summary",
                             "final_key_takeaways", "top_claims_numbers", "highlights", "next_steps",
                             "confidence", "chunks_count"]
            if all(field in result for field in required_fields):
                return result
            
        except json.JSONDecodeError:
            if attempt < retry_count:
                continue
        except Exception as e:
            if attempt < retry_count:
                continue
    
    return None

