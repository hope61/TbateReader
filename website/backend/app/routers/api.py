from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.limiter import limiter
from app.utils import get_chapters_from_filesystem, get_chapter_content
import os
import socket

router = APIRouter()

@router.get("/health")
def health_check():
    """Health check endpoint for Docker."""
    return {"status": "healthy", "service": "tbate-reader-api"}

@router.get("/test")
def test_endpoint():
    """Simple test endpoint."""
    return {"message": "test works"}

def get_local_ip():
    """Get the local network IP address."""
    local_ip = "127.0.0.1"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    except Exception:
        pass
    finally:
        try:
            s.close()
        except Exception:
            pass
    return local_ip

# Simple function to get base URL for images
def get_base_url(request: Request):
    """Get base URL for image URLs."""
    # Prefer explicit API domain in production
    if os.getenv("ENVIRONMENT", "development") == "production":
        return "https://manaapi.dicki.org"
    # Fall back to request base URL in dev
    return str(request.base_url).rstrip("/")

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
# @limiter.limit("100/minute")
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
# @limiter.limit("100/minute")
def get_novel_chapters(
    request: Request,
    novel_id: int,
    db: Session = Depends(get_db)
):
    """List all chapters for a specific novel."""
    # Get novel from database to verify it exists
    novel = db.query(models.Novel).filter(models.Novel.id == novel_id).first()
    if not novel:
        raise HTTPException(status_code=404, detail="Novel not found")
    
    # Construct path to novel's chapter directory
    # Use relative path when running locally, absolute path in Docker
    if os.path.exists(f"./novels/{novel.title}"):
        novel_directory = f"./novels/{novel.title}"
    else:
        novel_directory = f"/app/novels/{novel.title}"
    
    # Get chapters from filesystem
    chapters = get_chapters_from_filesystem(novel_directory)
    
    return chapters

@router.get("/novels/{novel_id}/chapters/{chapter_number}")
# @limiter.limit("100/minute")
def get_chapter(
    request: Request,
    novel_id: int,
    chapter_number: int,
    db: Session = Depends(get_db)
):
    """Get a specific chapter of a novel."""
    # Get novel from database to verify it exists
    novel = db.query(models.Novel).filter(models.Novel.id == novel_id).first()
    if not novel:
        raise HTTPException(status_code=404, detail="Novel not found")
    
    # Construct path to novel's chapter directory
    # Use relative path when running locally, absolute path in Docker
    if os.path.exists(f"./novels/{novel.title}"):
        novel_directory = f"./novels/{novel.title}"
    else:
        novel_directory = f"/app/novels/{novel.title}"
    
    # Get chapter content from filesystem
    chapter_data = get_chapter_content(novel_directory, chapter_number)
    
    if not chapter_data:
        raise HTTPException(status_code=404, detail="Chapter not found")
    
    return chapter_data