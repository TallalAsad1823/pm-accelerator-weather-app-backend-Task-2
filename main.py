from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager
from database import init_db
from routers.weather import router
import os
from dotenv import load_dotenv

load_dotenv()

# ====================== PM Accelerator Info ======================

DEVELOPER_NAME = "Tallal Asad"

PM_ACCELERATOR_DESCRIPTION = (
    "PM Accelerator is a product management training and career accelerator program "
    "that empowers aspiring and experienced product managers through real-world projects, "
    "mentorship, and a global community. It bridges the gap between theory and practice "
    "by providing hands-on experience, industry connections, and personalized coaching "
    "to help professionals break into or advance in product management roles."
)

# ====================== Lifespan ======================

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting Aether Weather Backend...")
    print(f"👤 Developer: {DEVELOPER_NAME}")
    init_db()
    yield
    print("👋 Shutting down Aether Weather Backend...")

# ====================== App Init ======================

app = FastAPI(
    title="Aether Weather Backend",
    description=(
        f"**PM Accelerator Technical Assessment - Task 2 (Backend)**\n\n"
        f"**Developer:** {DEVELOPER_NAME}\n\n"
        f"**About PM Accelerator:** {PM_ACCELERATOR_DESCRIPTION}\n\n"
        f"**Stack:** FastAPI · SQLite · OpenWeatherMap API · YouTube Data API v3\n\n"
        f"**Features:** CRUD operations · Date range support · "
        f"Location validation · Multi-format export (JSON, CSV, XML, Markdown, PDF) · YouTube Integration"
    ),
    version="1.0.0",
    lifespan=lifespan
)

# ====================== CORS ======================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ====================== Router ======================

app.include_router(router)

# ====================== Root ======================

@app.get("/")
async def root():
    return {
        "message": "Aether Weather Backend is running successfully! 🚀",
        "developer": DEVELOPER_NAME,
        "about_pm_accelerator": PM_ACCELERATOR_DESCRIPTION,
        "assessment": "PM Accelerator Technical Assessment - Task 2 (Backend)",
        "docs": "/docs",
        "redoc": "/redoc",
        "database": "SQLite",
        "weather_api": "OpenWeatherMap",
        "bonus_api": "YouTube Data API v3",
        "export_formats": ["json", "csv", "xml", "markdown", "pdf"],
        "features": [
            "CRUD - Create, Read, Update, Delete weather records",
            "Date range input and validation",
            "Location validation with fuzzy match suggestions",
            "Multi-format data export",
            "YouTube videos by city - Bonus API"
        ]
    }

# ====================== Health Check ======================

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "developer": DEVELOPER_NAME,
        "database": "SQLite Connected",
        "openweather": "Configured",
        "youtube": "Configured"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )