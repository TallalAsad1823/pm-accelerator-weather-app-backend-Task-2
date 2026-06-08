from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Weather Record Model
class WeatherRecord(BaseModel):
    location: str
    city: str
    country: Optional[str] = None
    temperature: float
    feels_like: float
    humidity: int
    wind_speed: float
    description: str
    icon: str
    date: datetime
    uv_index: Optional[float] = None
    pressure: Optional[int] = None
    visibility: Optional[float] = None

# Response Models
class WeatherResponse(BaseModel):
    id: str
    location: str
    city: str
    temperature: float
    description: str
    date: datetime

class RecordListResponse(BaseModel):
    records: List[WeatherResponse]
    total: int

class MessageResponse(BaseModel):
    message: str
    id: Optional[str] = None