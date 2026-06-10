from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List, Dict
import httpx
import os
from dotenv import load_dotenv
from datetime import datetime, date
import io
import csv
import json
import xml.etree.ElementTree as ET

from database import (
    save_search,
    get_history,
    get_record_by_id,
    update_record,
    delete_record,
    export_records
)

# Load environment variables
load_dotenv()
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

if not OPENWEATHER_API_KEY:
    raise Exception("OPENWEATHER_API_KEY is not set in .env file")

router = APIRouter(prefix="/api", tags=["weather"])


# ====================== Pydantic Models ======================

class WeatherRequest(BaseModel):
    city: str
    lat: Optional[float] = None
    lon: Optional[float] = None
    start_date: Optional[str] = None  # Format: YYYY-MM-DD
    end_date: Optional[str] = None    # Format: YYYY-MM-DD

class WeatherResponse(BaseModel):
    city: str
    temperature: float
    feels_like: float
    condition: str
    description: str
    humidity: int
    pressure: int
    wind_speed: float
    visibility: int
    sunrise: str
    sunset: str
    icon: str
    timestamp: str
    record_id: Optional[int] = None


# ====================== Validation ======================

def validate_date_range(start_date: Optional[str], end_date: Optional[str]):
    """Validate date range input"""

    if (start_date and not end_date) or (end_date and not start_date):
        raise HTTPException(
            status_code=400,
            detail="Both start_date and end_date are required together. Format: YYYY-MM-DD"
        )

    if not start_date and not end_date:
        return

    try:
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid start_date format: '{start_date}'. Use YYYY-MM-DD (e.g. 2024-06-01)"
        )

    try:
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid end_date format: '{end_date}'. Use YYYY-MM-DD (e.g. 2024-06-07)"
        )

    if end < start:
        raise HTTPException(
            status_code=400,
            detail=f"end_date ({end_date}) cannot be before start_date ({start_date})"
        )

    if (end - start).days > 365:
        raise HTTPException(
            status_code=400,
            detail="Date range cannot exceed 365 days"
        )


async def validate_location(city: str, lat: Optional[float], lon: Optional[float]):
    """Location validation with fuzzy match suggestions"""

    if lat is not None and lon is not None:
        if not (-90 <= lat <= 90):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid latitude: {lat}. Must be between -90 and 90."
            )
        if not (-180 <= lon <= 180):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid longitude: {lon}. Must be between -180 and 180."
            )
        return

    geo_url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {
        "q": city,
        "limit": 5,
        "appid": OPENWEATHER_API_KEY
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(geo_url, params=params)

        if response.status_code != 200:
            raise HTTPException(
                status_code=503,
                detail="Location validation service unavailable. Try again later."
            )

        results = response.json()

        if not results:
            raise HTTPException(
                status_code=404,
                detail=f"Location '{city}' not found. Please check the spelling or try a nearby city name."
            )

        city_lower = city.strip().lower()
        exact_match = any(r.get("name", "").lower() == city_lower for r in results)

        if not exact_match:
            suggestions = [
                f"{r.get('name', '')}, {r.get('country', '')}"
                for r in results[:3]
            ]
            raise HTTPException(
                status_code=404,
                detail=f"Location '{city}' not found. Did you mean: {' | '.join(suggestions)}?"
            )


# ====================== Helper Function ======================

async def fetch_weather_from_openweather(
    city: str,
    lat: Optional[float] = None,
    lon: Optional[float] = None
):
    base_url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
        "lang": "en"
    }

    if lat is not None and lon is not None:
        params.update({"lat": lat, "lon": lon})
    else:
        params["q"] = city

    async with httpx.AsyncClient() as client:
        response = await client.get(base_url, params=params)

        if response.status_code != 200:
            error_detail = response.json().get("message", "Failed to fetch weather data")
            raise HTTPException(
                status_code=response.status_code,
                detail=f"OpenWeatherMap Error: {error_detail}"
            )

        data = response.json()

        sunrise = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M")
        sunset = datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M")

        return {
            "city": data["name"],
            "temperature": round(data["main"]["temp"], 1),
            "feels_like": round(data["main"]["feels_like"], 1),
            "condition": data["weather"][0]["main"],
            "description": data["weather"][0]["description"].capitalize(),
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "wind_speed": data["wind"].get("speed", 0),
            "visibility": data.get("visibility", 0),
            "sunrise": sunrise,
            "sunset": sunset,
            "icon": data["weather"][0]["icon"],
            "timestamp": datetime.now().isoformat()
        }


# ====================== Export Helper Functions ======================

def build_xml(records: List[Dict]) -> str:
    """Convert records list to XML string"""
    root = ET.Element("weather_history")
    for rec in records:
        entry = ET.SubElement(root, "record")
        for key, value in rec.items():
            child = ET.SubElement(entry, key)
            child.text = str(value) if value is not None else ""
    return ET.tostring(root, encoding="unicode", xml_declaration=False)


def build_markdown(records: List[Dict]) -> str:
    """Convert records list to Markdown table"""
    if not records:
        return "# Weather History\n\nNo records found."

    headers = list(records[0].keys())
    md = "# Aether Weather - Export\n\n"
    md += "| " + " | ".join(headers) + " |\n"
    md += "| " + " | ".join(["---"] * len(headers)) + " |\n"

    for rec in records:
        row = " | ".join(str(rec.get(h, "")) for h in headers)
        md += f"| {row} |\n"

    md += f"\n\n_Exported on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_\n"
    md += "\n**Built by Tallal Asad | PM Accelerator Technical Assessment**\n"
    return md


def build_pdf_html(records: List[Dict]) -> bytes:
    """Generate PDF using fpdf2"""
    try:
        from fpdf import FPDF

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, "Aether Weather - Export", ln=True, align="C")
        pdf.set_font("Helvetica", "", 9)
        pdf.cell(0, 8, f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="C")
        pdf.cell(0, 8, "Built by Tallal Asad | PM Accelerator Technical Assessment", ln=True, align="C")
        pdf.ln(4)

        if not records:
            pdf.cell(0, 10, "No records found.", ln=True)
            return bytes(pdf.output())

        headers = list(records[0].keys())
        col_width = 190 / len(headers)

        pdf.set_fill_color(30, 144, 255)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 7)
        for h in headers:
            pdf.cell(col_width, 7, str(h)[:14], border=1, fill=True)
        pdf.ln()

        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Helvetica", "", 7)
        fill = False
        for rec in records:
            pdf.set_fill_color(240, 248, 255) if fill else pdf.set_fill_color(255, 255, 255)
            for h in headers:
                val = str(rec.get(h, ""))[:14]
                pdf.cell(col_width, 6, val, border=1, fill=True)
            pdf.ln()
            fill = not fill

        return bytes(pdf.output())

    except ImportError:
        raise HTTPException(
            status_code=500,
            detail="PDF export requires 'fpdf2' package. Run: pip install fpdf2"
        )


# ====================== API Endpoints ======================

@router.post("/weather", response_model=WeatherResponse)
async def get_current_weather(request: WeatherRequest):
    """Fetch real-time weather from OpenWeatherMap and save to history"""
    try:
        validate_date_range(request.start_date, request.end_date)
        await validate_location(request.city, request.lat, request.lon)

        weather_data = await fetch_weather_from_openweather(
            city=request.city,
            lat=request.lat,
            lon=request.lon
        )

        record_id = save_search(
            city=weather_data["city"],
            temperature=weather_data["temperature"],
            condition=weather_data["condition"],
            start_date=request.start_date,
            end_date=request.end_date
        )

        weather_data["record_id"] = record_id
        return weather_data

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history")
async def fetch_history(limit: int = Query(20, ge=1, le=100)):
    """Get search history (newest first)"""
    return get_history(limit)


@router.get("/weather/{record_id}")
async def get_weather_record(record_id: int):
    """Get a single saved weather record by ID"""
    record = get_record_by_id(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record


@router.put("/weather/{record_id}")
async def update_weather_record(
    record_id: int,
    temperature: Optional[float] = None,
    condition: Optional[str] = None
):
    """Update temperature and/or condition of a saved record"""
    record = get_record_by_id(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    success = update_record(record_id, temperature, condition)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update record")

    return {"success": True, "message": "Record updated successfully"}


@router.delete("/weather/{record_id}")
async def delete_weather_record(record_id: int):
    """Delete a saved weather record"""
    success = delete_record(record_id)
    if not success:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"success": True, "message": "Record deleted successfully"}


@router.get("/export")
async def export_data(
    format: str = Query("json", enum=["json", "csv", "xml", "markdown", "pdf"])
):
    """Export all weather history. Formats: json | csv | xml | markdown | pdf"""
    from fastapi.responses import StreamingResponse, Response

    records = export_records()

    if not records:
        return {"message": "No records to export"}

    if format == "json":
        content = json.dumps(records, indent=2, ensure_ascii=False)
        return Response(
            content=content,
            media_type="application/json",
            headers={"Content-Disposition": "attachment; filename=weather_history.json"}
        )

    elif format == "csv":
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)
        output.seek(0)
        return StreamingResponse(
            io.BytesIO(output.getvalue().encode("utf-8")),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=weather_history.csv"}
        )

    elif format == "xml":
        xml_content = build_xml(records)
        return Response(
            content=xml_content,
            media_type="application/xml",
            headers={"Content-Disposition": "attachment; filename=weather_history.xml"}
        )

    elif format == "markdown":
        md_content = build_markdown(records)
        return Response(
            content=md_content,
            media_type="text/markdown",
            headers={"Content-Disposition": "attachment; filename=weather_history.md"}
        )

    elif format == "pdf":
        pdf_bytes = build_pdf_html(records)
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=weather_history.pdf"}
        )


# ====================== YouTube API Endpoint ======================

@router.get("/videos/{city}")
async def get_city_videos(city: str):
    """
    Fetch top 5 YouTube videos for a given city.
    Bonus API integration - YouTube Data API v3
    """
    if not YOUTUBE_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="YouTube API key not configured. Add YOUTUBE_API_KEY to .env file."
        )

    youtube_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": f"{city} weather travel",
        "type": "video",
        "maxResults": 5,
        "order": "relevance",
        "key": YOUTUBE_API_KEY
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(youtube_url, params=params)

        if response.status_code == 403:
            raise HTTPException(
                status_code=403,
                detail="YouTube API quota exceeded or API key invalid."
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"YouTube API Error: {response.json().get('error', {}).get('message', 'Unknown error')}"
            )

        data = response.json()
        items = data.get("items", [])

        if not items:
            return {
                "city": city,
                "videos": [],
                "message": f"No videos found for '{city}'"
            }

        videos = []
        for item in items:
            video_id = item["id"]["videoId"]
            snippet = item["snippet"]
            videos.append({
                "title": snippet.get("title", ""),
                "channel": snippet.get("channelTitle", ""),
                "description": snippet.get("description", "")[:150] + "..." if snippet.get("description") else "",
                "thumbnail": snippet.get("thumbnails", {}).get("high", {}).get("url", ""),
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "published_at": snippet.get("publishedAt", "")
            })

        return {
            "city": city,
            "total": len(videos),
            "videos": videos
        }