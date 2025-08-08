import os
import re
import logging
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