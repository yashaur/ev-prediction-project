import streamlit as st
import pandas as pd
import joblib
import numpy as np
import time
import requests


# Loading the classifier model
classifier = joblib.load('./model/ev_efficiency_classifier.pkl')

# Sample data based on highest probability of High-Efficiency EV
sample = {
    "manufacturer": "Tesla", "model": "Model 3", "type": "Sedan", "drive_type": "RWD", "fuel_type": "Electric", "color": "White",
    "fast_charging": "Yes", "country": "USA", "city": "San Francisco", "battery_kwh": 60, "range_km": 450, "charging_time_hr": 1.2, "release_year": 2023,
    "seats": 5, "acceleration_0_100_kmph": 5.8, "top_speed_kmph": 225, "warranty_years": 8, "cargo_space_liters": 425, "safety_rating": 5
    }

manufacturers = ['BYD', 'Lucid', 'Volkswagen', 'BMW', 'Chevrolet', 'Nissan', 'Ford', 'Kia', 'Tesla', 'Hyundai']

models = ['Model S', 'EV6', 'Ioniq', 'Model 3', 'Leaf', 'ID.4', 'Model X', 'Mustang Mach-E', 'Bolt', 'Air', 'i3']

types = ['Coupe', 'Hatchback', 'SUV', 'Truck', 'Crossover', 'Sedan']

fuel_types = ['Electric', 'Hybrid']

countries = ['China', 'Japan', 'Norway', 'Canada', 'UK', 'France', 'India', 'Germany', 'USA', 'South Korea']

all_cities = {
            'China': ['Shanghai', 'Shenzhen', 'Beijing'],
            'Japan': ['Tokyo', 'Osaka'],
            'Norway': ['Oslo'],
            'Canada': ['Vancouver', 'Toronto'],
            'UK': ['London', 'Manchester'],
            'France': ['Paris'],
            'India': ['Pune', 'Bangalore', 'Delhi'],
            'Germany': ['Munich', 'Berlin'],
            'USA': ['New York', 'Austin', 'San Francisco', 'Seattle'],
            'South Korea': ['Seoul']
 }

years = [year for year in range(2012,2026)]

drive_types = ['FWD', 'AWD', 'RWD']

colors = ['Blue', 'White', 'Black', 'Green', 'Yellow', 'Silver', 'Red', 'Grey']


# Initialising input values for the current streamlit session
for k in sample:
    st.session_state[k] = st.session_state.get(k, None)

st.set_page_config(
                    layout = "wide",
                    page_title = "EV Efficiency Predictor",
                    page_icon = "🚗",
                )

st.title("🚗 EV Efficiency Predictor", text_alignment = "center")

st.write("⚡️ Predict whether your electric vehicle is high-efficiency or low-efficiency. Enter the following details:")

# -------------------------
# Demo button (fills inputs only)
# -------------------------
with st.container(horizontal=True):

    if st.button("Load Demo Values"):
        for k in sample:
            st.session_state[k] = sample[k]

    if st.button("Reset"):
        for k in sample:
            st.session_state[k] = None

# -------------------------
# Input widgets
# -------------------------

### BASIC DETAILS

st.write('**BASIC DETAILS:**')

manufacturer, model, type, fuel_type, country, city, release_year = st.columns(7)

manufacturer.selectbox(
    "Manufacturer",
    options = manufacturers,
    key="manufacturer"
)

model.selectbox(
    "Model",
    options = models,
    key="model"
)

type.selectbox(
    "Type",
    options = types,
    key="type"
)

fuel_type.selectbox(
    "Fuel Type",
    options = fuel_types,
    key="fuel_type"
)

country.selectbox(
    "Country",
    options = countries,
    key="country"
)

if st.session_state.country:
    cities = all_cities[st.session_state.country]
else:
    cities = [""]

city.selectbox(
    "City",
    options = cities,
    key="city"
)

release_year.selectbox(
    "Release Year",
    options = years,
    key="release_year"
)

st.space('xxsmall')


### RANGE, CHARGING, AND EFFICIENCY

st.write("**RANGE & CHARGING:**")

drive_type, battery_kwh, range_km, charging_time_hr, fast_charging = st.columns(5)

drive_type.selectbox(
    "Drive Type",
    options = drive_types,
    key="drive_type"
)

battery_kwh.number_input(
    "Battery Capacity (kWh)",
    min_value = 0.0,
    key="battery_kwh"
)

range_km.number_input(
    "Range (km)",
    min_value = 0.0,
    key="range_km"
)

charging_time_hr.number_input(
    "Charging time (hours)",
    min_value = 0.0,
    key="charging_time_hr"
)

fast_charging.selectbox(
    "Fast charging?",
    options = ["Yes", "No"],
    key="fast_charging"
)

st.space('xxsmall')


### PERFORMANCE & SAFETY

st.write("**PERFORMANCE & SAFETY**")

acceleration_0_100_kmph, top_speed_kmph, safety_rating, warranty_years = st.columns(4)

acceleration_0_100_kmph.number_input(
    "Acceleration time: 0-100 km/h (secs)",
    min_value = 0.0,
    key="acceleration_0_100_kmph"
)

top_speed_kmph.number_input(
    "Top speed (km/h)",
    min_value = 0.0,
    key="top_speed_kmph"
)

safety_rating.number_input(
    "Safety Rating",
    min_value = 3.0,
    max_value = 5.0,
    key="safety_rating"
)

warranty_years.number_input(
    "Warranty (years)",
    min_value = 0.0,
    key="warranty_years"
)

st.space('xxsmall')


### SPACE, COMFORT, AND LIFESTYLE FIT

st.write("**SPACE, COMFORT & DESIGN**")

seats, cargo_space_liters, color = st.columns(3)

seats.number_input(
    "Number of seats",
    min_value = 2,
    max_value = 7,
    key="seats"
)

cargo_space_liters.number_input(
    "Cargo space (litres)",
    min_value = 0.0,
    key="cargo_space_liters"
)

color.selectbox(
    "Colour",
    options = colors,
    key="color"
)

st.space('xxsmall')

# -------------------------
# Predict button (runs model)
# -------------------------



if st.button("Predict", width = 'stretch', type = 'primary'):

    start = time.time()

    df = pd.DataFrame()

    for col in sample.keys():
        input_df = pd.DataFrame({str(col): [st.session_state[col]]})
        df = pd.concat([df,input_df], axis = 1)


    correct_order_features = [
        'manufacturer', 'model', 'type', 'drive_type', 'fuel_type', 'color', 'fast_charging', 'country', 'city', 'battery_kwh',
        'range_km', 'charging_time_hr', 'release_year', 'seats', 'acceleration_0_100_kmph', 'top_speed_kmph', 'warranty_years',
        'cargo_space_liters', 'safety_rating'
        ]

    df = df[correct_order_features]

    if df.loc[0,'fast_charging'] == 'Yes':
        df.loc[0, 'fast_charging'] = 1
    else:
        df.loc[0, 'fast_charging'] = 0

    df['fast_charging'] = df['fast_charging'].astype('int8')

    prediction = classifier.predict(df)

    time_taken = time.time() - start
    time_output =  f" [Time taken: {time_taken:.3f}s]"

    if prediction[0] == 1:
        st.success("Your electric vehicle is high-efficiency! ✅" + time_output)
    else:
        st.error("Your electric vehicle is low-efficiency ❗️" + time_output)


if st.button("Predict (using API)", width = 'stretch', type = 'primary'):

    start = time.time()
    
    payload = {col: st.session_state[col] for col in sample.keys()}

    try:
        response = requests.post(
            "http://localhost:8000/predict",
            json=payload,
            timeout=5
        )

        if response.status_code == 200:
            result = response.json()['prediction']
            
            time_taken = time.time() - start
            time_output =  f" [Time taken: {time_taken:.3f}s]"

            if result == 1:
                st.success("Your electric vehicle is high-efficiency! ✅" + time_output)
            else:
                st.error("Your electric vehicle is low-efficiency ❗️" + time_output)

        else:
            st.error(f"API Error {response.status_code}: {response.text}")

    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {e}")