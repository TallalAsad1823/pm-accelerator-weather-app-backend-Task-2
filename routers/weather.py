from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List
import io
import csv
from database import (
    save_search, get_history, get_record_by_id, 
    update_record, delete_record, export_records
)

# Router
from fastapi import APIRouter
router = APIRouter(prefix="/api", tags=["weather"])



# Request Models
class WeatherSearchRequest(BaseModel):
    city: str
    temperature: float
    condition: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class WeatherUpdateRequest(BaseModel):
    temperature: Optional[float] = None
    condition: Optional[str] = None

# POST - Save Weather
@router.post("/search")
async def create_weather_search(data: WeatherSearchRequest):
    # Date validation
    if data.start_date and data.end_date:
        if data.start_date > data.end_date:
            raise HTTPException(status_code=400, detail="end_date cannot be before start_date")
    
    record_id = save_search(
        city=data.city,
        temperature=data.temperature,
        condition=data.condition,
        start_date=data.start_date,
        end_date=data.end_date
    )
    
    return {
        "success": True,
        "message": "Weather record saved successfully",
        "record_id": record_id
    }

# GET - History
@router.get("/history")
async def fetch_history(limit: int = Query(20, le=100)):
    return get_history(limit)

# PUT - Update Record
@router.put("/weather/{record_id}")
async def update_weather_record(record_id: int, data: WeatherUpdateRequest):
    record = get_record_by_id(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    success = update_record(record_id, data.temperature, data.condition)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update record")
    
    return {"success": True, "message": "Record updated successfully"}

# DELETE - Delete Record
@router.delete("/weather/{record_id}")
async def delete_weather_record(record_id: int):
    success = delete_record(record_id)
    if not success:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"success": True, "message": "Record deleted successfully"}

# Export Data
@router.get("/export")
async def export_data(format: str = Query("json", enum=["json", "csv"])):
    records = export_records()
    
    if format == "json":
        return records
    elif format == "csv":
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=records[0].keys() if records else [])
        writer.writeheader()
        writer.writerows(records)
        output.seek(0)
        
        return StreamingResponse(
            io.BytesIO(output.getvalue().encode()),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=weather_history.csv"}
        )