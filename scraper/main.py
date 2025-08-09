import logging
import os
import time
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from vars import OFFSET, REQUEST_DELAY
from fetch import fetch_chapter
from misc import process_chapter_data, sanitize_filename

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("chapter_processor.log"),
        logging.StreamHandler()
    ]
)

def main():
    try:
        # Get starting chapter from user
        while True:
            chapter_input = 1   
            
            try:
                start_chapter = int(chapter_input)
                if start_chapter < 1:
                    logging.warning("Chapter number must be at least 1")
                    continue
                break
            except ValueError:
                logging.warning("Please enter a valid number")
        
        current_chapter = start_chapter
        downloaded_count = 0
        
        logging.info(f"Starting download from chapter {start_chapter}")
        
        # Create directories if needed
        os.makedirs("chapters/text", exist_ok=True)
        
        while True:
            api_chapter = current_chapter + OFFSET
            logging.info(f"Processing chapter {current_chapter} (API: {api_chapter})")
            
            # Fetch chapter data
            chapter_data = fetch_chapter(api_chapter)
            
            # Stop if chapter not found
            if chapter_data is None:
                logging.info("Chapter not found - reached end of available chapters")
                break
            
            # Extract title and content
            title, content = process_chapter_data(chapter_data, api_chapter)
            
            if not title or not content:
                logging.warning("Skipping chapter due to processing error")
                current_chapter += 1
                continue
            
            # Create safe filename using chapter title with numeric prefix for proper sorting
            safe_title = sanitize_filename(title)
            
            # Create filename - if title is generic/empty, use only the number; otherwise include title
            if safe_title:
                text_filename = f"{downloaded_count}_{safe_title}.txt"
            else:
                text_filename = f"{downloaded_count}.txt"
                
            downloaded_count += 1
            text_path = os.path.join("chapters/text", text_filename)
            
            with open(text_path, 'w', encoding='utf-8') as f:
                f.write(f"{title}\n\n")
                f.write(str(content))
            
            logging.info(f"Saved text: {text_path}")
            
            # Prepare for next chapter
            current_chapter += 1
            time.sleep(REQUEST_DELAY)
    
    except KeyboardInterrupt:
        logging.info("Process interrupted by user")
    except Exception as e:
        logging.exception("Critical error occurred in main process")

if __name__ == "__main__":
    main()