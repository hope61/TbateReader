import re
import logging
import os

def process_chapter_data(chapter_data, api_chapter):
    """Extract title and content from API response"""
    if str(api_chapter) in chapter_data:
        return chapter_data[str(api_chapter)][0], chapter_data[str(api_chapter)][1]
    elif 'title' in chapter_data:
        return chapter_data['title'], chapter_data['content']
    else:
        logging.error(f"Unexpected response format")
        return None, None
    
def sanitize_filename(title):
    """Sanitize title for safe filename"""
    safe_title = re.sub(r'[^\w\s-]', '', title).strip()
    return re.sub(r'\s+', '_', safe_title)

def save_chapter(title, content):
    """Save chapter to file with proper formatting"""
    safe_title = sanitize_filename(title)
    filename = f"{safe_title}.txt"
    os.makedirs("chapters", exist_ok=True)
    filepath = os.path.join("chapters", filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"{title}\n\n")
        f.write(content)
    
    return filepath
def remove_span_tags(data):
    """
    Recursively remove <span>...</span> tags from strings in JSON-like structures.
    Keeps the inner text.
    """
    if isinstance(data, dict):
        return {k: remove_span_tags(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [remove_span_tags(item) for item in data]
    elif isinstance(data, str):
        # Remove opening <span ...> and closing </span>, but keep content
        data = re.sub(r'<\s*span[^>]*>', '', data, flags=re.IGNORECASE)
        data = re.sub(r'<\s*/\s*span\s*>', '', data, flags=re.IGNORECASE)
        return data
    else:
        return data