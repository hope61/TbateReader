import re
import logging
import os

def process_chapter_data(chapter_data, api_chapter):
    """Extract title and content from API response"""
    if str(api_chapter) in chapter_data:
        chapter_array = chapter_data[str(api_chapter)]
        if len(chapter_array) >= 2:
            title = chapter_array[0]  # First element is the title
            content = chapter_array[1]  # Second element is the content
            return title, content
        else:
            logging.error(f"Chapter data array has insufficient elements: {len(chapter_array)}")
            return None, None
    elif 'title' in chapter_data:
        return chapter_data['title'], chapter_data['content']
    else:
        logging.error(f"Unexpected response format for chapter {api_chapter}")
        return None, None
    
def sanitize_filename(title):
    """Sanitize title for safe filename and remove chapter numbers"""
    original_title = title.strip()
    
    # First, check if this is a PURELY generic title (just numbers/chapter numbers)
    purely_generic_patterns = [
        r'^Chapter\s+\d+$',  # "Chapter 234"
        r'^Chapter\s+c-?\d+$',  # "Chapter c-1" 
        r'^c-?\d+$',  # "c-1"
        r'^\d+$',  # Just a number "234"
        r'^\d+\.\d+$',  # Decimal numbers "374.5"
    ]
    
    for pattern in purely_generic_patterns:
        if re.match(pattern, original_title, re.IGNORECASE):
            return ""  # Return empty string for purely generic titles
    
    # Process non-generic titles
    safe_title = title
    
    # Remove "Chapter" followed by numbers, letters, or special patterns
    safe_title = re.sub(r'^Chapter\s*', '', safe_title, flags=re.IGNORECASE)  # Remove "Chapter" prefix
    safe_title = re.sub(r'^c?-?\d+\s*:\s*', '', safe_title)  # Remove "c-1:", "525:", etc.
    safe_title = re.sub(r'^c?-?\d+\s*-\s*', '', safe_title)  # Remove "c-1-", "525-", etc.
    safe_title = re.sub(r'^\d+\.\d+\s*[-:]?\s*', '', safe_title)  # Remove "374.5:", "374.5-", etc.
    safe_title = re.sub(r'^\d+\s*[-:]?\s*', '', safe_title)  # Remove "342:", "342-", etc.
    safe_title = re.sub(r'^v\d+ex\d+\s*:\s*', '', safe_title)  # Remove "v11ex1:", etc.
    safe_title = re.sub(r'^epl\d+\s*:\s*', '', safe_title)  # Remove "epl1:", etc.
    safe_title = re.sub(r'^Vol\s*\d+\s*', '', safe_title, flags=re.IGNORECASE)  # Remove "Vol 11"
    safe_title = re.sub(r'^Extra\s*\d+\s*:\s*', '', safe_title, flags=re.IGNORECASE)  # Remove "Extra 1:"
    safe_title = re.sub(r'^Epilogue\s*:\s*', '', safe_title, flags=re.IGNORECASE)  # Remove "Epilogue:"
    
    # Now remove or replace problematic characters for filenames
    safe_title = re.sub(r'[<>:"/\\|?*]', '', safe_title)  # Remove illegal filename chars
    safe_title = re.sub(r'[^\w\s\-\.]', '', safe_title)  # Keep alphanumeric, spaces, hyphens, dots
    
    # Clean up any remaining leading/trailing separators
    safe_title = re.sub(r'^[-_\s]+', '', safe_title)
    safe_title = re.sub(r'[-_\s]+$', '', safe_title)
    
    # Replace spaces with underscores
    safe_title = re.sub(r'\s+', '_', safe_title.strip())
    
    # Check if we're left with something meaningful
    if not safe_title or len(safe_title) < 2:
        return ""  # Return empty for generic/meaningless titles
    
    # Limit filename length to avoid filesystem issues
    if len(safe_title) > 150:  # Leave room for prefix
        safe_title = safe_title[:150]
    
    return safe_title

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