# TbateReader

A web application for reading novels with a clean, modern interface.

## Features

- 📚 Novel browsing and reading
- 🔍 Chapter navigation
- 📱 Responsive design
- ⚡ Fast loading with optimized performance

## Tech Stack

- **Frontend**: Vue.js 3, Bootstrap 5
- **Backend**: Python FastAPI
- **Database**: SQLite
- **Deployment**: Docker, Nginx

## Quick Start

1. Clone the repository
2. Run with Docker Compose:
   ```bash
   docker-compose up -d
   ```

## Project Structure

```
TbateReader/
├── website/
│   ├── frontend/     # Vue.js frontend
│   └── backend/      # FastAPI backend
├── scraper/          # Novel scraping tools
└── docker-compose.yml
```

## Development

- Frontend: `cd website/frontend && npm run dev`
- Backend: `cd website/backend && python -m uvicorn app.main:app --reload`
