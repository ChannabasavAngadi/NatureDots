# main.py
from fastapi import FastAPI, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel
import sqlite3
from datetime import datetime
from geopy.distance import geodesic

app = FastAPI()

# SQLite Database Configuration
DB_FILE = 'water_quality.db'

# Create SQLite Database Connection
try:
    db_connection = sqlite3.connect(DB_FILE)
    cursor = db_connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS water_quality_observations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        latitude REAL,
        longitude REAL,
        date_time TEXT,
        description TEXT,
        pH REAL,
        conductivity REAL,
        DO REAL,
        contaminants TEXT
    )
    """)
    db_connection.commit()
    cursor.close()
    print("Connected to SQLite Database!")
except sqlite3.Error as e:
    print(f"Error: {e}")

# Pydantic models
class Location(BaseModel):
    latitude: float
    longitude: float

class Parameters(BaseModel):
    pH: float
    conductivity: float
    DO: float
    contaminants: List[str]

class WaterQualityObservation(BaseModel):
    id: Optional[int] = None
    location: Location
    date_time: str
    description: str
    parameters: Parameters

# Create Observation
@app.post("/observations/", response_model=WaterQualityObservation)
async def create_observation(observation: WaterQualityObservation):
    query = "INSERT INTO water_quality_observations (latitude, longitude, date_time, description, pH, conductivity, DO, contaminants) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    values = (
        observation.location.latitude,
        observation.location.longitude,
        observation.date_time,
        observation.description,
        observation.parameters.pH,
        observation.parameters.conductivity,
        observation.parameters.DO,
        ",".join(observation.parameters.contaminants)
    )
    cursor = db_connection.cursor()
    cursor.execute(query, values)
    db_connection.commit()
    observation.id = cursor.lastrowid
    cursor.close()
    return observation

# Get Observation by ID
@app.get("/observations/", response_model=List[WaterQualityObservation])
async def get_observations():
    query = "SELECT * FROM water_quality_observations"
    cursor = db_connection.cursor()
    cursor.execute(query)
    observations = []
    for row in cursor.fetchall():
        parameters = Parameters(
            pH=row[5],
            conductivity=row[6],
            DO=row[7],
            contaminants=row[8].split(",")
        )
        location = Location(latitude=row[1], longitude=row[2])
        observation = WaterQualityObservation(id=row[0], location=location, date_time=row[3], description=row[4], parameters=parameters)
        observations.append(observation)
    cursor.close()
    return observations

# Delete Observation by ID
@app.delete("/observations/{observation_id}", response_model=WaterQualityObservation)
async def delete_observation(observation_id: int):
    query = "DELETE FROM water_quality_observations WHERE id = ?"
    cursor = db_connection.cursor()
    cursor.execute(query, (observation_id,))
    db_connection.commit()
    cursor.close()
    return {"message": "Observation deleted successfully"}

# Update Observation by ID
@app.put("/observations/{observation_id}", response_model=WaterQualityObservation)
async def update_observation(observation_id: int, observation: WaterQualityObservation):
    # Check if the observation with the specified ID exists
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM water_quality_observations WHERE id = ?", (observation_id,))
    existing_observation = cursor.fetchone()
    cursor.close()

    if existing_observation is None:
        raise HTTPException(status_code=404, detail="Observation not found")

    # Update the observation if it exists
    query = "UPDATE water_quality_observations SET latitude=?, longitude=?, date_time=?, description=?, pH=?, conductivity=?, DO=?, contaminants=? WHERE id = ?"
    values = (
        observation.location.latitude,
        observation.location.longitude,
        observation.date_time,
        observation.description,
        observation.parameters.pH,
        observation.parameters.conductivity,
        observation.parameters.DO,
        ",".join(observation.parameters.contaminants),
        observation_id
    )
    cursor = db_connection.cursor()
    cursor.execute(query, values)
    db_connection.commit()
    cursor.close()
    observation.id = observation_id
    return observation

# Endpoint to find records by closest location
@app.get("/observations/closest/")
async def get_closest_observations(latitude: float, longitude: float, limit: int = 10):
    query = "SELECT * FROM water_quality_observations"
    cursor = db_connection.cursor()
    cursor.execute(query)
    observations = []
    for row in cursor.fetchall():
        location = (row[1], row[2])
        distance = geodesic((latitude, longitude), location).kilometers
        observations.append({"id": row[0], "distance": distance, "location": location})
    cursor.close()
    observations.sort(key=lambda x: x["distance"])  # Sort by distance
    return observations[:limit]

# Endpoint to find records by date range and specific water quality parameters
@app.get("/observations/filter/")
async def filter_observations(start_date: datetime, end_date: datetime, min_pH: float = None, max_pH: float = None, contaminants: str = None):
    query = "SELECT * FROM water_quality_observations WHERE date_time BETWEEN ? AND ?"
    params = (start_date, end_date)
    if min_pH is not None:
        query += " AND pH >= ?"
        params += (min_pH,)
    if max_pH is not None:
        query += " AND pH <= ?"
        params += (max_pH,)
    if contaminants:
        query += " AND contaminants LIKE ?"
        params += (f"%{contaminants}%",)
    
    cursor = db_connection.cursor()
    cursor.execute(query, params)
    observations = cursor.fetchall()
    cursor.close()
    return observations

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Water Quality Observations Platform"}
