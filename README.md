# Aether Weather Backend


Submitted by: Tallal Asad

**PM Accelerator Technical Assessment #1 -TASK-2 (Backend)**

This project serves as the backend service for the Aether Weather application. It is built with **FastAPI** and uses **SQLite** for data persistence. It handles weather data logging, history retrieval, updates, deletions, and data export.

## 🛠️ Tech Stack
- **Framework:** FastAPI (Python 3.14+)
- **Database:** SQLite (Local file: `aether_weather.db`)
- **Validation:** Pydantic Models
- **API Documentation:** Swagger UI (Auto-generated)

## 📂 Project Structure
```text
aether-weather-backend/
├── main.py            # App entry point & configuration
├── database.py        # Database connection & CRUD operations
├── models.py          # Data validation schemas (Pydantic)
├── routers/           # API Endpoints
│   └── weather.py     # Weather-specific logic
├── .env               # Environment variables
├── requirements.txt   # Dependencies
└── aether_weather.db  # Local SQLite database (auto-generated)

--- 

🚀 How to Run
1. Prerequisites
Ensure you have Python 3.14+ installed.

2. Setup
Clone the repository and navigate to the project folder.

---

Create and activate a virtual environment:

Bash
# Create venv
python -m venv venv

# Activate venv (Mac/Linux)
source venv/bin/activate

# Activate venv (Windows)
venv\Scripts\activate
Install dependencies:

Bash
pip install -r requirements.txt
3. Start the Server
Bash
uvicorn main:app --reload
The server will start at (http://127.0.0.1:8000).

---


📖 API Documentation
Once the server is running, you can access the interactive API documentation to test all endpoints (POST, GET, PUT, DELETE, EXPORT):

URL: (http://127.0.0.1:8000/docs)

---


📋 Assessment Requirements Checklist
[x] CREATE: Save weather searches with date ranges.

[x] READ: Fetch search history via /api/history.

[x] UPDATE: Edit records via /api/weather/{record_id}.

[x] DELETE: Remove records via /api/weather/{record_id}.

[x] EXPORT: Download data as JSON or CSV via /api/export.

[x] VALIDATIONS: Date range and existence checks implemented.

---

Made for PM Accelerator Technical Assessment #1 -TASK 2 -BACKEND
Submitted by: Tallal Asad


---
