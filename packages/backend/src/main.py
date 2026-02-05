from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import logging
import os
from pathlib import Path
from src.config import settings
from src.database import init_db, seed_db
from src.routes_speakers import router as speakers_router
from src.routes_profiles import router as profiles_router

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Meno Match API",
    description="Intelligent speaker search and matching platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Starting Meno Match API")
    try:
        init_db()
        seed_db()
        logger.info("✓ Database initialized")
    except Exception as e:
        logger.error(f"Database initialization error: {e}")

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Meno Match API"
    }

# Include routers FIRST so they take priority
app.include_router(speakers_router)
app.include_router(profiles_router)

# Get HTML file path
def get_html_file():
    """Get the path to the HTML UI file"""
    # Path: /workspaces/meno-match/packages/backend/src/main.py
    # Need: /workspaces/meno-match/simple-test.html
    # So: parent.parent.parent.parent (go to /workspaces/meno-match/)
    html_file = Path(__file__).parent.parent.parent.parent / "simple-test.html"
    logger.info(f"Looking for HTML at: {html_file}")
    logger.info(f"File exists: {html_file.exists()}")
    return html_file if html_file.exists() else None

# Serve UI at root - MUST be defined AFTER routers so /api/* routes take priority
@app.get("/", tags=["UI"])
async def root():
    """Serve the simple test UI"""
    html_file = get_html_file()
    if html_file:
        logger.info(f"Serving HTML from: {html_file}")
        return FileResponse(str(html_file), media_type="text/html")
    logger.warning("HTML file not found, returning JSON")
    return JSONResponse({
        "name": "Meno Match API",
        "version": "1.0.0",
        "docs": "/docs",
        "openapi": "/openapi.json"
    })

# Also serve at /index.html explicitly
@app.get("/index.html", tags=["UI"])
async def index():
    """Serve UI at /index.html"""
    html_file = get_html_file()
    if html_file:
        return FileResponse(str(html_file), media_type="text/html")
    return JSONResponse({"error": "UI not found"}, status_code=404)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": str(exc),
            "timestamp": datetime.utcnow().isoformat()
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=settings.api_port,
        reload=settings.debug
    )
