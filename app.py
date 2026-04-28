from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import numpy as np
import joblib
import json
import os
from datetime import datetime
import random

app = Flask(__name__)
CORS(app)

# Load model if exists, else use dummy
MODEL_PATH = 'energy_model.pkl'
FEATURES_PATH = 'feature_columns.json'

try:
    model = joblib.load(MODEL_PATH)
    with open(FEATURES_PATH, 'r') as f:
        feature_columns = json.load(f)
    print("✅ Model loaded successfully!")
except:
    model = None
    feature_columns = []
    print("⚠️ Model not found, using simulation mode")


def simulate_energy(hour, temperature, humidity, occupancy, hvac, lighting, renewable, square_footage, holiday, month, day_of_week):
    energy = (
        20
        + 0.5 * temperature
        + 2.0 * occupancy
        + 15 * hvac
        + 5 * lighting
        - 0.3 * renewable
        + 0.005 * square_footage
        + 5 * (hour >= 17)
        + random.uniform(-2, 2)
    )
    return round(energy, 2)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        hour = int(data.get('hour', datetime.now().hour))
        temperature = float(data.get('temperature', 25))
        humidity = float(data.get('humidity', 50))
        occupancy = int(data.get('occupancy', 3))
        hvac = int(data.get('hvac', 1))
        lighting = int(data.get('lighting', 1))
        renewable = float(data.get('renewable', 10))
        square_footage = float(data.get('square_footage', 1500))
        holiday = int(data.get('holiday', 0))
        month = int(data.get('month', datetime.now().month))
        day_of_week = int(data.get('day_of_week', datetime.now().weekday()))

        if model:
            features = np.array([[hour, month, day_of_week, temperature, humidity,
                                   occupancy, hvac, lighting, renewable, square_footage, holiday]])
            prediction = float(model.predict(features)[0])
        else:
            prediction = simulate_energy(hour, temperature, humidity, occupancy,
                                         hvac, lighting, renewable, square_footage, holiday, month, day_of_week)

        prediction = round(prediction, 2)
        avg_energy = 65.0
        anomaly_result = bool(prediction > avg_energy * 1.3)
        savings = round(max(0, renewable * 0.3 * 0.12), 2)

        return jsonify({
            'prediction': prediction,
            'anomaly': anomaly_result,
            'savings': savings,
            'status': 'High Usage ⚠️' if anomaly_result else 'Normal ✅'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/live-data')
def live_data():
    now = datetime.now()
    hour = now.hour

    # Simulate 24 hours of data
    hourly = []
    for h in range(24):
        temp = 20 + 10 * np.sin(2 * np.pi * h / 24) + random.uniform(-1, 1)
        occ = 1 if 8 <= h <= 22 else 0
        hvac = 1 if temp > 28 or temp < 18 else 0
        light = 1 if h >= 18 or h <= 6 else 0
        renew = max(0, 20 * np.sin(2 * np.pi * h / 24) + random.uniform(0, 5))
        energy = simulate_energy(h, temp, 50, occ * 3, hvac, light, renew, 1500, 0, now.month, now.weekday())
        hourly.append({
            'hour': f'{h:02d}:00',
            'energy': round(energy, 2),
            'temperature': round(temp, 1),
            'renewable': round(renew, 1)
        })

    # Current sensor values
    current_temp = round(20 + 10 * np.sin(2 * np.pi * hour / 24) + random.uniform(-1, 1), 1)
    current_humidity = round(50 + random.uniform(-5, 5), 1)
    current_occupancy = random.randint(1, 5) if 8 <= hour <= 22 else 0
    current_energy = hourly[hour]['energy']
    total_today = round(sum(h['energy'] for h in hourly[:hour + 1]), 2)
    renewable_now = round(hourly[hour]['renewable'], 1)
    cost_saved = round(renewable_now * 0.12, 2)

    return jsonify({
        'hourly': hourly,
        'current': {
            'temperature': current_temp,
            'humidity': current_humidity,
            'occupancy': current_occupancy,
            'energy': current_energy,
            'total_today': total_today,
            'renewable': renewable_now,
            'cost_saved': cost_saved,
            'anomaly': bool(current_energy > 65 * 1.3)
        }
    })


@app.route('/api/stats')
def stats():
    # Weekly stats simulation
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    weekly = [round(random.uniform(400, 700), 1) for _ in days]
    total_week = sum(weekly)
    avg_day = round(total_week / 7, 1)
    peak_day = days[weekly.index(max(weekly))]
    savings_week = round(total_week * 0.15 * 0.12, 2)

    return jsonify({
        'days': days,
        'weekly': weekly,
        'total_week': total_week,
        'avg_day': avg_day,
        'peak_day': peak_day,
        'savings_week': savings_week
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)
