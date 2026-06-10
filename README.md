# 🌤️ Aether Weather-App Backend

**Name:** Tallal Asad  
**Project:** PM Accelerator Technical Assessment-1 — Task 2 (Backend Integration)  


---

## 🎯 About PM Accelerator
PM Accelerator is a premier product management training and career accelerator program that empowers aspiring and experienced product managers through real-world projects, mentorship, and a global community. It bridges the gap between theory and practice by providing hands-on experience, industry connections, and personalized coaching to help professionals break into or advance in product management roles.

---

## ✨ Features & Capabilities

- **Core CRUD Operations:** Full capability to Create, Read, Update, and Delete weather records dynamically.
- **Advanced Location Validation:** Validates coordinate ranges and integrates with the OpenWeatherMap Geocoding API to verify if a city exists. Features **Fuzzy Matching** capabilities (e.g., searching "Lahroe" suggests *"Did you mean: Lahore, PK?"*).
- **Date Range Support & Validation:** Robust server-side validation rules preventing `end_date` from being before `start_date` or exceeding a strict 365-day query limit.
- **Multi-Format Data Export:** Seamless history extraction into **JSON, CSV, XML, Markdown (MD), and PDF** formats.
- **Bonus Feature (YouTube API Integration):** Captures real-time media contexts by fetching the top 5 travel/weather videos for searched locations using the YouTube Data API v3.

---

## 🛠️ Tech Stack

- **Backend Framework:** FastAPI (Python)
- **Database Architecture:** SQLite (Local file: `aether_weather.db`)
- **Data Validation:** Pydantic v2
- **PDF Generation Library:** `fpdf2`
- **HTTP Client:** `httpx` (Asynchronous async-await operations)

---

## 🚀 Quick Start Guide

### 📋 Prerequisites
- Python 3.10 or higher installed on your system.

### ⚙️ Installation & Local Setup

```bash
# 1. Clone the repository
git clone [https://github.com/TallalAsad1823/pm-accelerator-weather-app-backend-Task-2](https://github.com/TallalAsad1823/pm-accelerator-weather-app-backend-Task-2)
cd aether-weather-backend

# 2. Setup Virtual Environment
python -m venv venv

# 3. Activate Virtual Environment
source venv/bin/activate        # On Mac/Linux
# venv\Scripts\activate         # On Windows

# 4. Install Dependencies
pip install -r requirements.txt

```

### 🔑 Environment Variables Setup (`.env`)

Create a file named `.env` in your project's root directory and add your secret API keys as follows:

```env
DATABASE_URL=sqlite:///./aether_weather.db
OPENWEATHER_API_KEY=your_openweathermap_api_key_here
YOUTUBE_API_KEY=Your_Actual_Youtube_API_KEY 

```

### 🏃 Running the Application

```bash
uvicorn main:app --reload

```

Once executed, the local terminal server will provide the live development endpoints:

* **Base URL:** `http://127.0.0.1:8000`
* **Health Status Route:** `http://127.0.0.1:8000/health`

---

## 📖 Interactive API Documentation (Swagger UI)

FastAPI automatically handles documentation generation via **Swagger UI**. This interactive interface lets developers and evaluators easily test all endpoint models directly from the browser without needing a separate frontend setup.

Once your local server is running, you can access the live documentation portal here:
👉 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

---

## 🧪 Evaluation & Testing Guide (Quick Demo Links)

To make evaluation simple, use these direct links and sample formats to test the backend logic instantly:

### 1. Storing Records & Validation (`POST /api/weather`)

Navigate to Swagger UI and pass the following sample JSON structure into the request body to execute location tracking and DB storage:

```json
{
  "city": "Texas",
  "start_date": "2026-06-01",
  "end_date": "2026-06-07"
}

```

### 2. Live Media Video Context (`GET /api/videos/{city}`)

Click these direct endpoints to verify how the backend asynchronously requests metadata pipelines and formats structured YouTube search payloads:

* **Test Lahore Videos:** [http://localhost:8000/api/videos/Lahore](https://www.google.com/search?q=http://localhost:8000/api/videos/Lahore)
* **Test London Videos:** [http://localhost:8000/api/videos/London](https://www.google.com/search?q=http://localhost:8000/api/videos/London)
* **Test New York Videos:** [http://localhost:8000/api/videos/New%20York](https://www.google.com/search?q=http://localhost:8000/api/videos/New%2520York)

### 3. Data Export Downloader Core (`GET /api/export`)

Test the output streaming endpoints by directly invoking your preferred download format:

* **Download JSON Engine:** [http://localhost:8000/api/export?format=json](https://www.google.com/search?q=http://localhost:8000/api/export%3Fformat%3Djson)
* **Download CSV Sheet:** [http://localhost:8000/api/export?format=csv](https://www.google.com/search?q=http://localhost:8000/api/export%3Fformat%3Dcsv)
* **Download XML Structure:** [http://localhost:8000/api/export?format=xml](https://www.google.com/search?q=http://localhost:8000/api/export%3Fformat%3Dxml)
---

## 📂 Project Structure

```plaintext
aether-weather-backend/
├── main.py                 # FastAPI application entry point & metadata configurations
├── database.py             # SQLite structural initialization and abstract SQL CRUD logic
├── models.py               # Data transfer definitions & shared Pydantic input systems
├── requirements.txt        # Controlled listing of environmental external modules
├── .env                    # Hidden parameters mapping core tokens and api access credentials
├── aether_weather.db       # Local persistent file storing history streams securely
└── routers/
    └── weather.py          # Master routing controller managing functional core endpoints

```

---

## 📋 Task 2 Requirements Verification Matrix

| Requirement Specification | Technical Routing | Operational Status |
| --- | --- | --- |
| **Location Input Tracking** | `POST /api/weather` | ✅ Complete |
| **Fuzzy Match Fallbacks** | Geocoding Validation Logic | ✅ Complete |
| **Date Range Constraints** | `validate_date_range()` Handler | ✅ Complete |
| **Search Logging (Read History)** | `GET /api/history` | ✅ Complete |
| **Individual Entity Retrieval** | `GET /api/weather/{record_id}` | ✅ Complete |
| **Log Updates (PUT System)** | `PUT /api/weather/{record_id}` | ✅ Complete |
| **Log Record Discard (Delete)** | `DELETE /api/weather/{record_id}` | ✅ Complete |
| **Baseline Streaming Layouts** | `JSON` & `CSV` Data Transformers | ✅ Complete |
| **Advanced Export Extensions** | `XML`, `Markdown`, `PDF` Custom Builders | ✅ Complete |
| **Developer Metadata Rendering** | System Core Context Injection | ✅ Complete |
| **Bonus 3rd Party Integrations** | `GET /api/videos/{city}` (YouTube Pipeline) | ✅ Complete |

---

**Submitted by Tallal Asad for the PM Accelerator Backend Technical Assessment-1 Task-1.**

```

```