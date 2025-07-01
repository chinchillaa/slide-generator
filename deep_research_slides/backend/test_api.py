#!/usr/bin/env python3
"""APIキーのテストスクリプト"""
import os
from dotenv import load_dotenv

load_dotenv()

print("=== API Keys Status ===")
print(f"OPENAI_API_KEY: {'✓ Set' if os.getenv('OPENAI_API_KEY') else '✗ Not set'}")
print(f"SERPAPI_API_KEY: {'✓ Set' if os.getenv('SERPAPI_API_KEY') else '✗ Not set'}")
print(f"SERPER_API_KEY: {'✓ Set' if os.getenv('SERPER_API_KEY') else '✗ Not set'}")
print(f"HF_TOKEN: {'✓ Set' if os.getenv('HF_TOKEN') else '✗ Not set'}")

# SERPAPIのテスト
serpapi_key = os.getenv('SERPAPI_API_KEY')
if serpapi_key:
    print(f"\nSERPAPI_API_KEY length: {len(serpapi_key)}")
    print(f"First 10 chars: {serpapi_key[:10]}...")
    
    # SERPAPIのテスト
    import requests
    url = f"https://serpapi.com/search?api_key={serpapi_key}&q=test&engine=google"
    response = requests.get(url)
    print(f"\nSERPAPI Test Response: {response.status_code}")
    if response.status_code != 200:
        print(f"Error: {response.text[:200]}")