import joblib
import pandas as pd

loaded_model = joblib.load("model/ev_efficiency_classifier.pkl")


new_ev = pd.DataFrame([{
    "manufacturer": "Tesla",
    "model": "Model 3",
    "type": "Sedan",
    "drive_type": "RWD",
    "fuel_type": "Electric",
    "color": "White",
    "fast_charging": 1,
    "country": "USA",
    "city": "San Francisco",

    "battery_kwh": 60,
    "range_km": 450,
    "charging_time_hr": 1.2,
    "release_year": 2023,
    "seats": 5,
    "acceleration_0_100_kmph": 5.8,
    "top_speed_kmph": 225,
    "warranty_years": 8,
    "cargo_space_liters": 425,
    "safety_rating": 5
}])
prediction = loaded_model.predict(new_ev)
print("Predicted class:", prediction[0])
probability = loaded_model.predict_proba(new_ev)
print("Probability [Low, High]:", probability[0])
label = "High Efficiency EV 🚗⚡" if prediction[0] == 1 else "Low Efficiency EV 🚙"
confidence = max(probability[0]) * 100

print(f"{label} (Confidence: {confidence:.2f}%)")
