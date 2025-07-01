#!/usr/bin/env python3
"""API動作確認用のシンプルなテストスクリプト"""
import requests
import json

# API URL
API_URL = "http://localhost:8000"

def test_research_endpoint():
    """調査エンドポイントをテスト"""
    url = f"{API_URL}/research"
    payload = {
        "query": "テスト調査",
        "model_id": "gpt-4o",
        "max_slides": 3
    }
    
    print(f"Sending POST request to {url}")
    print(f"Payload: {json.dumps(payload, ensure_ascii=False)}")
    
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # まずヘルスチェック
    try:
        health = requests.get(f"{API_URL}/health")
        print("Health check:", health.json())
    except Exception as e:
        print(f"Health check failed: {e}")
    
    # 調査エンドポイントのテスト
    test_research_endpoint()