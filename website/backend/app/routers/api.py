from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.limiter import limiter
import os
import socket

router = APIRouter()

@router.get("/health")
def health_check():
    """Health check endpoint for Docker."""
    return {"status": "healthy", "service": "tbate-reader-api"}

def get_local_ip():
    """Get the local network IP address."""
    try:
        # Connect to a remote address to get the local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

# Use environment variable or fallback to request.base_url
def get_base_url(request: Request):
    """Get base URL for image URLs."""
    # Check for environment variable first
    env_base_url = os.getenv("API_BASE_URL")
    if env_base_url:
        return env_base_url.rstrip('/')
    
    # For mobile access, use local network IP instead of 127.0.0.1
    base_url = str(request.base_url).rstrip('/')
    local_ip = get_local_ip()
    
    # Replace 127.0.0.1 with local network IP for mobile access
    if '127.0.0.1' in base_url:
        base_url = base_url.replace('127.0.0.1', local_ip)
    elif 'localhost' in base_url:
        base_url = base_url.replace('localhost', local_ip)
    
    # Ensure we're using the correct port (8000 for backend)
    if ':8000' not in base_url:
        base_url = base_url.replace(':5173', ':8000')  # Replace Vite dev server port
        # Only add port if local_ip is in the URL and no port is specified
        if local_ip in base_url and ':8000' not in base_url and ':5173' not in base_url:
            base_url = base_url.replace(local_ip, f'{local_ip}:8000')
    
    return base_url

@router.get("/novels")
@limiter.limit("100/minute")
def get_novels(request: Request, db: Session = Depends(get_db)):
    """List all novels."""
    novels = db.query(models.Novel).all()
    base_url = get_base_url(request)
    for novel in novels:
        if novel.image_url:
            relative_url = novel.image_url.lstrip('/')
            novel.image_url = f"{base_url}/{relative_url}"
    return novels

@router.get("/novels/{novel_id}")
@limiter.limit("100/minute")
def get_novel(
    request: Request,
    novel_id: int,
    db: Session = Depends(get_db)
):
    """Get details of a specific novel."""
    novel = db.query(models.Novel).filter(models.Novel.id == novel_id).first()
    if not novel:
        raise HTTPException(status_code=404, detail="Novel not found")
    base_url = get_base_url(request)
    if novel.image_url:
        relative_url = novel.image_url.lstrip('/')
        novel.image_url = f"{base_url}/{relative_url}"
    return novel

@router.get("/novels/{novel_id}/chapters")
@limiter.limit("100/minute")
def get_novel_chapters(
    request: Request,
    novel_id: int,
    db: Session = Depends(get_db)
):
    """List all chapters for a specific novel."""
    novel = db.query(models.Novel).filter(models.Novel.id == novel_id).first()
    if not novel:
        raise HTTPException(status_code=404, detail="Novel not found")
    chapters = db.query(models.Chapter).filter(
        models.Chapter.novel_id == novel_id
    ).order_by(models.Chapter.number).all()
    return [
        {"id": chapter.id, "title": chapter.title, "number": chapter.number}
        for chapter in chapters
    ]

@router.get("/novels/{novel_id}/chapters/{chapter_number}")
@limiter.limit("100/minute")
def get_chapter(
    request: Request,
    novel_id: int,
    chapter_number: int,
    db: Session = Depends(get_db)
):
    """Get a specific chapter of a novel."""
    chapter = db.query(models.Chapter).filter(
        models.Chapter.novel_id == novel_id,
        models.Chapter.number == chapter_number
    ).first()
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return {"title": chapter.title, "content": chapter.content}