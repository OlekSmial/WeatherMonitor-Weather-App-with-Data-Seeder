import os
import csv
import random
from flask import Flask, render_template, request, redirect, url_for, send_file
from pymongo import MongoClient
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Konfiguracja MongoDB
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASS = os.getenv("MONGO_PASS")
API_KEY = os.getenv("WEATHER_API_KEY")

MONGO_URL = f"mongodb://{MONGO_USER}:{MONGO_PASS}@mongodb:27017/"
client = MongoClient(MONGO_URL)
db = client.weather_database
collection = db.weather_forecasts

@app.route("/")
def index():
    # Pobieramy ostatnio wybrane miasto do wykresu
    last_entry = collection.find_one(sort=[("_id", -1)])
    if last_entry:
        current_city = last_entry['name']
        chart_data_cursor = list(collection.find({"name": current_city}).sort("_id", -1).limit(100))
        chart_data = chart_data_cursor[::-1]
    else:
        current_city = "Brak danych"
        chart_data = []

    all_data = list(collection.find().sort("_id", -1).limit(10))
    labels = [d['timestamp'] for d in chart_data]
    temps = [d['main']['temp'] for d in chart_data]
    
    return render_template("index.html", data=all_data, labels=labels, temps=temps, city_name=current_city)

@app.route("/fetch", methods=["POST"])
def fetch_weather():
    city = request.form.get("city")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        weather_data = response.json()
        weather_data["timestamp"] = datetime.now().strftime("%H:%M:%S")
        collection.insert_one(weather_data)
    return redirect(url_for('index'))

# --- FUNKCJA: SEEDER ---
@app.route("/seed", methods=["POST"])
def seed_data():
    city = request.form.get("city", "Warszawa (Symulacja)")
    hours = 100
    start_time = datetime.now() - timedelta(hours=hours)
    simulated_list = []
    base_temp = 10.0

    # Generowanie 100 pomiarów
    for i in range(hours):
        time_point = start_time + timedelta(hours=i)
        # Symulacja realistycznego trendu (lekki wzrost + szum)
        temp = round(base_temp + (i * 0.05) + random.uniform(-1.5, 1.5), 1)
        
        record = {
            "name": city,
            "main": {"temp": temp, "humidity": random.randint(40, 90)},
            "weather": [{"description": "symulacja historyczna"}],
            "timestamp": time_point.strftime("%H:%M:%S"),
            "full_date": time_point.strftime("%Y-%m-%d %H:%M:%S")
        }
        simulated_list.append(record)

    # Zapis do MongoDB
    collection.insert_many(simulated_list)

    # Zapis do pliku CSV
    csv_file = "weather_dataset.csv"
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Data", "Miasto", "Temperatura", "Wilgotność"])
        for r in simulated_list:
            writer.writerow([r["full_date"], r["name"], r["main"]["temp"], r["main"]["humidity"]])

    return redirect(url_for('index'))

@app.route("/download")
def download():
    # Ścieżka do wygenerowanego pliku CSV
    return send_file("weather_dataset.csv", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)