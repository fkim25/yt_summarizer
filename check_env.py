#!/usr/bin/env python3
"""
Diagnostic script to check .env file configuration
"""

import os
from pathlib import Path
import config

def check_env():
    """Check .env file and environment variables."""
    print("=" * 60)
    print("Environment Configuration Check")
    print("=" * 60)
    print()
    
    env_file = config.ENV_FILE
    
    # Check if file exists
    print(f"1. Checking .env file location:")
    print(f"   Path: {env_file}")
    print(f"   Exists: {env_file.exists()}")
    
    if env_file.exists():
        file_size = env_file.stat().st_size
        print(f"   Size: {file_size} bytes")
        
        if file_size == 0:
            print()
            print("   ❌ PROBLEM: .env file is EMPTY!")
            print("   Solution: Add your API key to the file:")
            print("   OPENAI_API_KEY=your_api_key_here")
        else:
            # Read and check contents (safely, without exposing the key)
            try:
                with open(env_file, 'r') as f:
                    lines = f.readlines()
                    print(f"   Lines: {len(lines)}")
                    
                    has_key = False
                    for i, line in enumerate(lines, 1):
                        line = line.strip()
                        if line and not line.startswith('#'):
                            if 'OPENAI_API_KEY' in line:
                                has_key = True
                                # Show format without exposing key
                                if '=' in line:
                                    parts = line.split('=', 1)
                                    key_part = parts[0].strip()
                                    value_part = parts[1].strip() if len(parts) > 1 else ""
                                    print(f"   Line {i}: {key_part}={('*' * min(10, len(value_part))) if value_part else 'EMPTY'}")
                                    if not value_part:
                                        print(f"      ❌ PROBLEM: OPENAI_API_KEY has no value!")
                                else:
                                    print(f"   Line {i}: {line[:50]}...")
                                    print(f"      ❌ PROBLEM: Missing '=' sign!")
                    
                    if not has_key:
                        print()
                        print("   ❌ PROBLEM: OPENAI_API_KEY not found in .env file!")
                        print("   Solution: Add this line to .env:")
                        print("   OPENAI_API_KEY=your_api_key_here")
                        
            except Exception as e:
                print(f"   ❌ Error reading file: {e}")
    else:
        print()
        print("   ❌ PROBLEM: .env file does not exist!")
        print("   Solution: Create .env file with:")
        print("   OPENAI_API_KEY=your_api_key_here")
    
    print()
    print("2. Checking environment variable loading:")
    config.ensure_env_loaded()
    api_key = os.getenv('OPENAI_API_KEY')
    
    if api_key:
        print(f"   ✅ OPENAI_API_KEY is loaded!")
        print(f"   Length: {len(api_key)} characters")
        print(f"   Starts with: {api_key[:7]}...")
    else:
        print("   ❌ OPENAI_API_KEY is NOT loaded!")
        print()
        print("   Possible issues:")
        print("   - .env file is empty or missing")
        print("   - Wrong format in .env file")
        print("   - File has wrong line endings or encoding")
        print()
        print("   Correct format:")
        print("   OPENAI_API_KEY=sk-...")
        print()
        print("   Common mistakes:")
        print("   - Adding quotes: OPENAI_API_KEY=\"sk-...\" (don't use quotes)")
        print("   - Adding spaces: OPENAI_API_KEY = sk-... (spaces are usually OK but avoid)")
        print("   - Wrong variable name: OPENAI_KEY=... (must be OPENAI_API_KEY)")
    
    print()
    print("=" * 60)
    print()
    
    if api_key:
        print("✅ Configuration looks good!")
        return True
    else:
        print("❌ Configuration needs fixing!")
        print()
        print("To fix this, run: python3 setup_env.py")
        return False

if __name__ == "__main__":
    check_env()

