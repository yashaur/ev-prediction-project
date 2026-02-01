🚀 Live Features

🔮 Predict EV efficiency (High / Low)

⚡ Uses battery, range, charging, speed & safety data

🌐 Interactive web UI

📊 ML model trained with Scikit-learn

🚀 FastAPI backend with Swagger docs

🐳 Fully Dockerized & deployment-ready

🛠 Tech Stack

GitHub: https://github.com/mohd-musheer

Docker Hub: https://hub.docker.com/r/mohdmusheer/ev-efficiency-predictor


Machine Learning: Scikit-learn, Pandas, Joblib

Frontend: HTML, CSS, JavaScript

Server: Uvicorn

Containerization: Docker

Python: 3.11

📦 Docker Repository

🔗 Docker Hub Image:
👉 https://hub.docker.com/r/musheer/ev-efficiency-predictor

Pull Image
docker pull musheer/ev-efficiency-predictor

Run Container
docker run -d -p 8000:8000 musheer/ev-efficiency-predictor

Open in Browser

Web App: http://localhost:8000

Swagger API Docs: http://localhost:8000/docs

📂 Project Structure
.
├── api/
│   └── api.py          # FastAPI backend
├── model/
│   └── ev_efficiency_classifier.pkl
├── UI/
│   └── index.html      # Frontend UI
├── requirements.txt
├── Dockerfile
└── README.md

🔗 API Usage
Endpoint
POST /predict

Sample Request
{
  "manufacturer": "Tesla",
  "model": "Model 3",
  "type": "Sedan",
  "drive_type": "RWD",
  "fuel_type": "Electric",
  "color": "White",
  "fast_charging": "Yes",
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
}

Response
{
  "prediction": 1
}


1 → High Efficiency

0 → Low Efficiency

🐳 Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "api.api:app", "--host", "0.0.0.0", "--port", "8000"]

🎯 Use Cases

ML & FastAPI portfolio project

Internship & placement interviews

Docker & DevOps practice

EV data analysis demos

College & capstone projects

👨‍💻 Author

Mohd Musheer

