from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse, HTMLResponse
import joblib
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware 

app = FastAPI(title = "EV Efficiency Predictor")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


MODEL_PATH = 'model/ev_efficiency_classifier.pkl' 

classifier = joblib.load(MODEL_PATH)

class PredictionInput(BaseModel):
    manufacturer: str
    model: str
    type: str
    drive_type: str
    fuel_type: str
    color: str
    fast_charging: str
    country: str
    city: str
    battery_kwh: float
    range_km: float
    charging_time_hr: float
    release_year: int
    seats: int
    acceleration_0_100_kmph: float
    top_speed_kmph: float
    warranty_years: int 
    cargo_space_liters: float
    safety_rating: float

class PredictionOutput(BaseModel):
    prediction: int

def preprocess(input_json):

    input_json = {k: [input_json[k]] for k in input_json.keys()}
    
    df = pd.DataFrame(input_json)
    

    if df.loc[0,'fast_charging'] == 'Yes':
        df.loc[0, 'fast_charging'] = '1'
    else:
        df.loc[0, 'fast_charging'] = '0'

    df['fast_charging'] = df['fast_charging'].astype('int8')

    correct_order_features = [
    'manufacturer', 'model', 'type', 'drive_type', 'fuel_type', 'color', 'fast_charging', 'country', 'city', 'battery_kwh',
    'range_km', 'charging_time_hr', 'release_year', 'seats', 'acceleration_0_100_kmph', 'top_speed_kmph', 'warranty_years',
    'cargo_space_liters', 'safety_rating'
    ]

    df = df[correct_order_features]

    return df

@app.post("/predict", response_model = PredictionOutput)
async def predict_efficiency(input_json: dict):
    
    input_df = preprocess(input_json)

    prediction = classifier.predict(input_df)[0]

    return {'prediction' :prediction}

@app.get("/", response_class=HTMLResponse)
def home():
    with open('UI/index.html', 'r') as f:
        return f.read()