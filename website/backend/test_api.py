#!/usr/bin/env python3
"""
Test script for API endpoints
"""
import requests
import json

def test_api():
    """Test the API endpoints."""
    base_url = "http://localhost:8000"
    
    print("Testing API endpoints...")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health check: {response.status_code}")
    except Exception as e:
        print(f"Health check failed: {e}")
    
    # Test novels endpoint
    try:
        response = requests.get(f"{base_url}/api/novels")
        print(f"Novels endpoint: {response.status_code}")
        if response.status_code == 200:
            novels = response.json()
            print(f"Found {len(novels)} novels")
            for novel in novels:
                print(f"  - {novel.get('title', 'Unknown')} (ID: {novel.get('id', 'Unknown')})")
                if novel.get('image_url'):
                    print(f"    Image URL: {novel['image_url']}")
    except Exception as e:
        print(f"Novels endpoint failed: {e}")
    
    # Test specific novel
    try:
        response = requests.get(f"{base_url}/api/novels/1")
        print(f"Novel 1 endpoint: {response.status_code}")
        if response.status_code == 200:
            novel = response.json()
            print(f"Novel details: {novel.get('title', 'Unknown')}")
    except Exception as e:
        print(f"Novel 1 endpoint failed: {e}")
    
    # Test chapters endpoint
    try:
        response = requests.get(f"{base_url}/api/novels/1/chapters")
        print(f"Chapters endpoint: {response.status_code}")
        if response.status_code == 200:
            chapters = response.json()
            print(f"Found {len(chapters)} chapters")
            if chapters:
                print(f"First chapter: {chapters[0]}")
    except Exception as e:
        print(f"Chapters endpoint failed: {e}")

if __name__ == "__main__":
    test_api()
