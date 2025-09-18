from fastapi import FastAPI, Depends
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from .database import SessionLocal, engine, get_db
from . import models, utils
from .routers import api
import logging
import os
import dotenv

# Load environment variables
dotenv.load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables if they don't exist
try:
    models.Base.metadata.create_all(bind=engine)
except Exception as e:
    logger.error(f"Database initialization error: {e}")
    # Continue anyway, the startup event will handle it

app = FastAPI(
    title="Mana's Embrace API",
    description="API for reading web novels",
    version="1.0.0",
    docs_url="/docs" if os.getenv("ENABLE_DOCS", "false").lower() == "true" else None,
    redoc_url=None
)

# Always Added Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=600
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Production-Only Middleware
if os.getenv("ENVIRONMENT", "development") == "production":
    # Skip HTTPS redirect for now to avoid complications behind Cloudflare/NGINX
    # app.add_middleware(HTTPSRedirectMiddleware)
    # Allow API and frontend domains, plus localhost for debugging
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=[
            "tbateapi.dicki.org",
            "tbate.dicki.org",
            "*.dicki.org",
            "localhost",
            "127.0.0.1",
            "0.0.0.0",
        ],
    )

# Routers
app.include_router(api.router)

# Serve static files
app.mount("/images", StaticFiles(directory="images"), name="images")

# Startup Event
@app.on_event("startup")
def startup_event():
    logger.info("Running startup initialization...")
    db = SessionLocal()
    try:
        novel_count = db.query(models.Novel).count()
        logger.info(f"Found {novel_count} novels in database")
        if novel_count == 0:
            logger.info("Initializing database from novels directory")
            novels_data = utils.process_novels_directory("./novels")
            logger.info(f"Found {len(novels_data)} novels to add")
            for novel in novels_data:
                db.add(novel)
                logger.info(f"Added novel: {novel.title}")
            db.commit()
            logger.info("Database initialized successfully")
        else:
            logger.info("Database already initialized")
    except Exception as e:
        db.rollback()
        logger.error(f"Startup error: {e}")
        raise
    finally:
        db.close()

