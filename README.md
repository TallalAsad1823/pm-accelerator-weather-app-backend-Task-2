# Aether Weather-App Backend

Submitted by: Tallal Asad
**PM Accelerator Technical Assessment #1 Task2 (Backend)**

Submitted by: Tallal Asad
A robust FastAPI backend for the Aether Weather application, featuring data persistence, CRUD operations, and data export.

---

## ✨ Features

- **Create**: Save weather records with city, temperature, condition, and optional date range.
- **Read**: Fetch recent search history via `/api/history`.
- **Update**: Modify existing weather records via `/api/weather/{record_id}`.
- **Delete**: Remove specific records via `/api/weather/{record_id}`.
- **Export**: Download records as **JSON** or **CSV** via `/api/export`.
- **Validation**: Fully validated with Pydantic models.
- **Documentation**: Interactive API docs via Swagger UI.

---

## 🛠️ Tech Stack

- **Framework**: FastAPI (Python 3.14)
- **Database**: SQLite (Local file: `aether_weather.db`)
- **Validation**: Pydantic
- **Documentation**: Auto-generated Swagger UI

---

## 🚀 Quick Start

### Prerequisites
- Python 3.14 or higher

### Setup & Run
```bash
# 1. Clone the repository
git clone [https://github.com/TallalAsad1823/pm-accelerator-weather-app-backend-Task-2](https://github.com/TallalAsad1823/pm-accelerator-weather-app-backend-Task-2)
cd aether-weather-backend

# 2. Activate virtual environment
source venv/bin/activate        # Mac/Linux
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the server
uvicorn main:app --reload

---

Server will start at: http://127.0.0.1:8000📖 API DocumentationOnce the server is running, access the interactive docs here:→ http://127.0.0.1:8000/docs📂 Project StructurePlaintextaether-weather-backend/
├── main.py                 # FastAPI app entry point
├── database.py             # SQLite database logic
├── models.py               # Pydantic data models
├── routers/
│   └── weather.py          # API endpoints
├── .env                    # Environment variables
├── requirements.txt        # Project dependencies
└── aether_weather.db       # SQLite database

--- 


📋 Assessment Requirements ChecklistRequirementStatusEndpointCreate weather record✅ DonePOST /api/searchView search history✅ DoneGET /api/historyUpdate record✅ DonePUT /api/weather/{id}Delete record✅ DoneDELETE /api/weather/{id}Export data (JSON/CSV)✅ DoneGET /api/export

---

Submitted by: Tallal Asad For: PM Accelerator Technical Assessment 1 Task 2 (Backend)
