#!/usr/bin/env python3
"""
Helper script to set up the .env file
"""

import os
from pathlib import Path

def setup_env_file():
    """Create or update the .env file with OpenAI API key."""
    env_file = Path(__file__).parent / '.env'
    
    print("=" * 60)
    print("Environment Setup")
    print("=" * 60)
    print()
    
    # Check if .env file exists and has content
    if env_file.exists() and env_file.stat().st_size > 0:
        print(f"⚠️  .env file already exists at: {env_file}")
        response = input("Do you want to overwrite it? (y/N): ").strip().lower()
        if response != 'y':
            print("Setup cancelled.")
            return
    
    # Get API key from user
    print("Please enter your OpenAI API key.")
    print("You can get one from: https://platform.openai.com/api-keys")
    print()
    api_key = input("OpenAI API Key: ").strip()
    
    if not api_key:
        print("❌ Error: API key cannot be empty!")
        return
    
    # Write to .env file
    try:
        with open(env_file, 'w') as f:
            f.write(f"OPENAI_API_KEY={api_key}\n")
        
        print()
        print("✅ .env file created successfully!")
        print(f"   Location: {env_file}")
        print()
        print("You can now run: python3 main.py")
        
    except Exception as e:
        print(f"❌ Error writing .env file: {e}")

if __name__ == "__main__":
    setup_env_file()

