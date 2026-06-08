# Aether Weather Backend

Submitted by: Tallal Asad

**PM Accelerator Technical Assessment #1 -TASK-2 (Backend)**

<<<<<<< HEAD
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

=======
A clean, robust, and production-ready FastAPI backend for the Aether Weather application. It allows users to log weather data, view history, update/delete records, and export data.
>>>>>>> c72d095

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
