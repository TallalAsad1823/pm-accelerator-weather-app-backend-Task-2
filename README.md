# Aether Weather Backend

Submitted by: Tallal Asad

**PM Accelerator Technical Assessment #1 -TASK-2 (Backend)**

A clean, robust, and production-ready FastAPI backend for the Aether Weather application. It allows users to log weather data, view history, update/delete records, and export data.

---

## ✨ Features

- **Create**: Save weather records with city, temperature, condition, and optional date range
- **Read**: Fetch recent search history
- **Update**: Modify existing weather records
- **Delete**: Remove specific records
- **Export**: Download all records as **JSON** or **CSV**
- Fully validated with Pydantic
- Clean error handling
- Interactive API documentation (Swagger UI)

---

## 🛠️ Tech Stack

- **Framework**: FastAPI (Python 3.14)
- **Database**: SQLite (local file: `aether_weather.db`)
- **Validation**: Pydantic
- **Documentation**: Auto-generated Swagger UI

---

## 🚀 Quick Start

### Prerequisites
- Python 3.14 or higher

### Setup & Run

```bash
# 1. Clone the repository or download project
git clone (https://github.com/TallalAsad1823/pm-accelerator-weather-app-backend-Task-2)
cd aether-weather-backend

# 2. Activate virtual environment
source venv/bin/activate        # Mac/Linux
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the server
uvicorn main:app --reload

Server will start at: http://127.0.0.1:8000

---

📖 API Documentation
Interactive API documentation is available at:
→ http://127.0.0.1:8000/docs (Swagger UI)

---

📂 Project Structure
aether-weather-backend/
├── main.py                 # FastAPI app entry point
├── database.py             # SQLite database logic
├── models.py               # Pydantic data models
├── routers/
│   └── weather.py          # All API endpoints
├── .env                    # Environment variables
├── requirements.txt        # Project dependencies
├── aether_weather.db       # Auto-generated SQLite database
└── README.md

---

📋 Assessment Requirements Checklist
RequirementStatusEndpointCreate weather record✅ DonePOST /api/searchView search history✅ DoneGET /api/historyUpdate record✅ DonePUT /api/weather/{id}Delete record✅ DoneDELETE /api/weather/{id}Export data (JSON/CSV)✅ DoneGET /api/export

---

Submitted by: Tallal Asad
For: PM Accelerator Technical Assessment #1 -TASK-2 (Backend)
