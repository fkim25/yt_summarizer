"""
ChatGPT API Summarizer
Uses OpenAI's ChatGPT API to generate summaries from text.
"""

import os
from openai import OpenAI
# Import config to ensure .env is loaded
import config


class Summarizer:
    """Handles summarization using OpenAI's ChatGPT API."""
    
    def __init__(self, api_key=None):
        """
        Initialize the summarizer.
        
        Args:
            api_key: OpenAI API key (if None, will try to get from environment)
        """
        # Ensure .env is loaded
        config.ensure_env_loaded()
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            # Provide helpful error message
            env_file = config.ENV_FILE
            if not env_file.exists():
                error_msg = (
                    f"\n❌ Error: OPENAI_API_KEY not found!\n\n"
                    f"   The .env file does not exist at: {env_file}\n"
                    f"   Please create it with: OPENAI_API_KEY=your_api_key_here\n\n"
                    f"   Or run: python3 setup_env.py\n"
                )
            elif env_file.stat().st_size == 0:
                error_msg = (
                    f"\n❌ Error: OPENAI_API_KEY not found!\n\n"
                    f"   The .env file exists but is empty: {env_file}\n"
                    f"   Please add: OPENAI_API_KEY=your_api_key_here\n\n"
                    f"   Or run: python3 setup_env.py\n"
                )
            else:
                error_msg = (
                    f"\n❌ Error: OPENAI_API_KEY not found in .env file!\n\n"
                    f"   Please check that {env_file} contains:\n"
                    f"   OPENAI_API_KEY=your_api_key_here\n\n"
                    f"   Or run: python3 setup_env.py\n"
                )
            raise ValueError(error_msg)
        self.client = OpenAI(api_key=self.api_key)
    
    def summarize(self, text, max_tokens=500, model="gpt-4o-mini"):
        """
        Generate a summary of the provided text.
        
        Args:
            text: Text to summarize
            max_tokens: Maximum tokens for the summary (default: 500)
            model: OpenAI model to use (default: "gpt-4o-mini")
            
        Returns:
            Summary string
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that creates concise, well-structured summaries of video transcripts. Focus on key points, main topics, and important details."
                    },
                    {
                        "role": "user",
                        "content": f"Please provide a comprehensive summary of the following video transcript:\n\n{text}"
                    }
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            raise Exception(f"Error generating summary: {str(e)}")

