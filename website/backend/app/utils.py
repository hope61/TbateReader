import os
import re
import logging
from typing import Tuple, List, Dict, Optional
from . import models

logger = logging.getLogger(__name__)

def extract_number(filename):
    # Simple integer extraction
    match = re.search(r'(\d+)', filename)
    return int(match.group(1)) if match else 0

def clean_filename(filename):
    # Get the base name without extension
    name = os.path.splitext(filename)[0]
    
    # Remove consecutive dots
    name = re.sub(r'\.{2,}', '.', name)
    
    # Remove trailing and leading dots/spaces
    name = name.rstrip('. ').lstrip('. ')
    
    # Remove any remaining double spaces
    name = re.sub(r'\s{2,}', ' ', name)
    
    # Remove any dots that are not part of the chapter number
    name = re.sub(r'(?<!\d)\.|\.(?!\d)', '', name)
    
    # Return just the cleaned name without extension
    return name

def process_novels_directory(base_path: str):
    novels = []
    
    if not os.path.exists(base_path):
        logger.error(f"Novels directory not found: {base_path}")
        return novels
    
    logger.info(f"Scanning novels directory: {base_path}")
    
    for novel_dir in os.listdir(base_path):
        novel_path = os.path.join(base_path, novel_dir)
        
        if os.path.isdir(novel_path):
            logger.info(f"Processing novel: {novel_dir}")
            novel = models.Novel(
                title=novel_dir,
                image_url=f"/images/novels/{novel_dir}.jpg"
            )
            chapters = []
            
            chapter_files = [f for f in os.listdir(novel_path) if f.lower().endswith('.txt')]
            chapter_files.sort(key=lambda x: extract_number(x))
            
            logger.info(f"Found {len(chapter_files)} chapters for {novel_dir}")
            
            for chapter_file in chapter_files:
                clean_name = clean_filename(chapter_file)
                chapter_path = os.path.join(novel_path, chapter_file)
                
                try:
                    with open(chapter_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    chapter_number = extract_number(clean_name)
                    logger.info(f"Processing: {chapter_file} -> Cleaned: {clean_name} -> Number: {chapter_number}")
                    
                    chapter = models.Chapter(
                        title=clean_name,
                        number=chapter_number,
                        content=content,
                        novel=novel
                    )
                    chapters.append(chapter)
                except Exception as e:
                    logger.error(f"Error reading {chapter_path}: {e}")
            
            novel.chapters = chapters
            novels.append(novel)
    
    return novels

def parse_chapter_filename(filename: str) -> Tuple[int, Optional[str]]:
    """
    Parse chapter filename to extract chapter number and title.
    
    Expected formats:
    - "123.txt" -> (123, None)
    - "123_Title_Here.txt" -> (123, "Title Here")
    
    Returns:
        Tuple of (chapter_number, title) where title is None for generic chapters
    """
    # Remove .txt extension
    base_name = os.path.splitext(filename)[0]
    
    # Check if it's just a number (generic chapter)
    if re.match(r'^\d+$', base_name):
        return int(base_name), None
    
    # Check if it has the format "number_title"
    match = re.match(r'^(\d+)_(.+)$', base_name)
    if match:
        chapter_number = int(match.group(1))
        title_part = match.group(2)
        # Convert underscores back to spaces
        title = title_part.replace('_', ' ')
        return chapter_number, title
    
    # Fallback: try to extract number from beginning
    match = re.match(r'^(\d+)', base_name)
    if match:
        return int(match.group(1)), None
    
    # If no number found, return 0
    return 0, None

def get_chapters_from_filesystem(novel_directory: str) -> List[Dict]:
    """
    Read chapters from filesystem and return list of chapter info.
    
    Args:
        novel_directory: Path to the novel's chapter directory
        
    Returns:
        List of dictionaries with chapter info: [{"number": int, "title": str, "id": int}, ...]
    """
    chapters = []
    
    if not os.path.exists(novel_directory):
        logger.error(f"Novel directory not found: {novel_directory}")
        return chapters
    
    # Get all .txt files
    chapter_files = [f for f in os.listdir(novel_directory) if f.lower().endswith('.txt')]
    
    # Parse each filename
    chapter_data = []
    for filename in chapter_files:
        chapter_number, title = parse_chapter_filename(filename)
        chapter_data.append({
            'filename': filename,
            'number': chapter_number,
            'title': title
        })
    
    # Sort by chapter number
    chapter_data.sort(key=lambda x: x['number'])
    
    # Create response format
    for i, chapter in enumerate(chapter_data):
        chapters.append({
            'id': i + 1,  # Sequential ID for frontend
            'number': chapter['number'],
            'title': chapter['title'] or f"Chapter {chapter['number']}"  # Use generic title if none
        })
    
    return chapters

def get_chapter_content(novel_directory: str, chapter_number: int) -> Optional[Dict]:
    """
    Get chapter content by chapter number.
    
    Args:
        novel_directory: Path to the novel's chapter directory
        chapter_number: Chapter number to retrieve
        
    Returns:
        Dictionary with title and content, or None if not found
    """
    if not os.path.exists(novel_directory):
        logger.error(f"Novel directory not found: {novel_directory}")
        return None
    
    # Find the file with the matching chapter number
    chapter_files = [f for f in os.listdir(novel_directory) if f.lower().endswith('.txt')]
    
    for filename in chapter_files:
        file_chapter_number, title = parse_chapter_filename(filename)
        
        if file_chapter_number == chapter_number:
            chapter_path = os.path.join(novel_directory, filename)
            
            try:
                with open(chapter_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Use the title from filename, or fallback to generic
                display_title = title or f"Chapter {chapter_number}"
                
                return {
                    'title': display_title,
                    'content': content
                }
            except Exception as e:
                logger.error(f"Error reading chapter file {chapter_path}: {e}")
                return None
    
    # Chapter not found
    return None