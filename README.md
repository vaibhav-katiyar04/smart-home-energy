# Smart Home Energy Conservation System
### Final Year Project | IoT + ML

## Project Structure
```
smart_home/
├── app.py                  # Flask backend + ML API
├── templates/
│   └── index.html          # Dashboard UI
├── requirements.txt        # Python dependencies
├── Procfile               # For Render.com deployment
├── energy_model.pkl        # Your trained ML model (copy from Colab)
└── feature_columns.json    # Feature names (copy from Colab)
```

## How to Run Locally

### Step 1 - Install dependencies
```bash
pip install -r requirements.txt
```

### Step 2 - Copy model files from Colab
Download these from Colab and put in this folder:
- energy_model.pkl
- feature_columns.json

### Step 3 - Run the app
```bash
python app.py
```

### Step 4 - Open in browser
```
http://localhost:5000
```

## How to Deploy on Render.com
1. Push this folder to GitHub
2. Go to render.com → New Web Service
3. Connect your GitHub repo
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `gunicorn app:app`
6. Click Deploy!

## Tech Stack
- Backend: Python Flask
- ML Model: XGBoost (R² = 0.90+)
- Frontend: HTML, CSS, Chart.js
- Deployment: Render.com
- IoT Simulation: Python data generation

## Features
- Real-time sensor monitoring (Temperature, Humidity, Occupancy)
- ML-based energy consumption prediction
- Anomaly detection alerts
- 24-hour energy usage chart
- Weekly energy overview
- Smart automation rules display
- Renewable energy tracking
- Cost savings calculator
