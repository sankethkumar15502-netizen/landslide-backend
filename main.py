from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class SensorData(BaseModel):
    elevation_m: float
    slope_degrees: float
    rainfall_mm_24h: float
    rainfall_mm_72h: float

def clamp(value, min_val, max_val):
    return max(min_val, min(max_val, value))

def get_risk_status(risk):
    if risk < 25:
        return "Low"
    if risk < 50:
        return "Moderate"
    if risk < 75:
        return "High"
    return "Critical"

# In-memory storage for the latest dashboard snapshot
latest_state = {
    "elevation_m": 359.9,
    "slope_degrees": 61.0,
    "rainfall_mm_24h": 120.0,
    "rainfall_mm_72h": 300.0,
    "risk_probability_percent": 68.5,
    "risk_level": "High",
}

@app.post("/predict")
def predict_risk(data: SensorData):
    global latest_state

    MAX_RAINFALL = 500
    MAX_SLOPE = 90

    slope_risk = clamp((data.slope_degrees / MAX_SLOPE) * 100, 0, 100)
    rainfall_risk = clamp((data.rainfall_mm_24h / MAX_RAINFALL) * 100, 0, 100)
    soil_risk = 50.0

    total_risk = (slope_risk * 0.5) + (rainfall_risk * 0.3) + (soil_risk * 0.2)
    final_risk = round(clamp(total_risk, 0, 100), 1)
    risk_status = get_risk_status(final_risk)

    # Save latest data snapshot from dashboard
    latest_state = {
        "elevation_m": data.elevation_m,
        "slope_degrees": data.slope_degrees,
        "rainfall_mm_24h": data.rainfall_mm_24h,
        "rainfall_mm_72h": data.rainfall_mm_72h,
        "risk_probability_percent": final_risk,
        "risk_level": risk_status,
    }

    # Respond to web dashboard as normal
    return {
        "risk_probability_percent": final_risk,
        "risk_level": risk_status,
    }

@app.get("/latest")
def get_latest_data():
    """Endpoint for mobile app to read the active monitoring data"""
    return latest_state