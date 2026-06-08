from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from database import init_db
from routers.weather import router

app = FastAPI(
    title="Aether Weather Backend",
    description="PM Accelerator Technical Assessment #2 - Backend (SQLite)",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # Change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Router (router already has `prefix="/api"`)
app.include_router(router)

# Startup Event
@app.on_event("startup")
async def startup_event():
    init_db()

# Root Route
@app.get("/")
async def root():
    return {
        "message": "Aether Weather Backend is running successfully! 🚀",
        "assessment": "PM Accelerator Technical Assessment #1 TASK-2 (Backend)",
        "docs": "/docs",
        "database": "SQLite (Local)"
    }

# Health Check
@app.get("/health")
async def health():
    return {"status": "healthy", "database": "SQLite Connected"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)