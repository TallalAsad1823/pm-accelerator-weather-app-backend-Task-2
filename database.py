import sqlite3
import csv
import io
from datetime import datetime
from typing import List, Dict, Optional

DB_NAME = "aether_weather.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database and create table"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            temperature REAL NOT NULL,
            condition TEXT NOT NULL,
            start_date TEXT,
            end_date TEXT,
            timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ Local SQLite Database Initialized Successfully!")

def save_search(city: str, temperature: float, condition: str, 
                start_date: Optional[str] = None, end_date: Optional[str] = None):
    """Save weather record"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO weather_history 
        (city, temperature, condition, start_date, end_date)
        VALUES (?, ?, ?, ?, ?)
    ''', (city, temperature, condition, start_date, end_date))
    
    conn.commit()
    record_id = cursor.lastrowid
    conn.close()
    return record_id

def get_history(limit: int = 20) -> List[Dict]:
    """Get recent history"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, city, temperature, condition, start_date, end_date, timestamp 
        FROM weather_history 
        ORDER BY timestamp DESC 
        LIMIT ?
    ''', (limit,))
    records = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return records

def get_record_by_id(record_id: int) -> Optional[Dict]:
    """Get single record"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM weather_history WHERE id = ?", (record_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def update_record(record_id: int, temperature: Optional[float] = None, 
                  condition: Optional[str] = None) -> bool:
    """Update existing record"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    updates = []
    params = []
    if temperature is not None:
        updates.append("temperature = ?")
        params.append(temperature)
    if condition is not None:
        updates.append("condition = ?")
        params.append(condition)
    
    if not updates:
        return False
    
    params.append(record_id)
    query = f"UPDATE weather_history SET {', '.join(updates)} WHERE id = ?"
    
    cursor.execute(query, params)
    conn.commit()
    success = cursor.rowcount > 0
    conn.close()
    return success

def delete_record(record_id: int) -> bool:
    """Delete record"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM weather_history WHERE id = ?", (record_id,))
    conn.commit()
    success = cursor.rowcount > 0
    conn.close()
    return success

def export_records(format_type: str = "json"):
    """Export all records"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM weather_history ORDER BY timestamp DESC")
    records = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return records