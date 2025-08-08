import logging
import requests
import time
from vars import BASE_URL, NOVEL_NAME, MAX_ATTEMPTS
from misc import remove_span_tags

def fetch_chapter(api_chapter):
    """Fetch chapter data from API with retry logic"""
    url = f"{BASE_URL}?n={NOVEL_NAME}&c={api_chapter}"
    
    for attempt in range(MAX_ATTEMPTS):
        try:
            logging.info(f"Requesting chapter {url}")
            headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
            }
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                cleaned_data = remove_span_tags(data)
                return cleaned_data
            
            # Handle "Chapter not found" error
            if response.status_code == 404:
                error_data = response.json()
                if error_data.get("error") == "Chapter not found":
                    return None
                
            logging.warning(f"Attempt {attempt+1}: Unexpected status {response.status_code}")
        
        except Exception as e:
            logging.warning(f"Attempt {attempt+1}: Connection error - {str(e)}")
        
        time.sleep(2)  # Backoff before retry
    
    logging.error(f"Failed to fetch chapter after {MAX_ATTEMPTS} attempts")
    return None