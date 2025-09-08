# server.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime

DB = "events.db"
STATIC_FOLDER = "website"  # put index.html here

app = Flask(__name__, static_folder=STATIC_FOLDER)
CORS(app)

def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            elephant_id TEXT NOT NULL,
            device_id TEXT,
            timestamp TEXT NOT NULL,
            lat REAL NOT NULL,
            lon REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route("/api/events", methods=["POST"])
def add_event():
    data = request.get_json()
    required = ("elephant_id","lat","lon","timestamp")
    if not data or not all(k in data for k in required):
        return jsonify({"error":"missing fields"}), 400

    elephant_id = data["elephant_id"]
    device_id = data.get("device_id")
    timestamp = data["timestamp"]
    lat = float(data["lat"])
    lon = float(data["lon"])

    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("INSERT INTO events (elephant_id, device_id, timestamp, lat, lon) VALUES (?,?,?,?,?)",
                (elephant_id, device_id, timestamp, lat, lon))
    conn.commit()
    conn.close()
    return jsonify({"status":"ok"}), 201

@app.route("/api/events", methods=["GET"])
def get_events():
    # optional query params: elephant, since
    elephant = request.args.get("elephant")
    since = request.args.get("since")  # ISO timestamp
    q = "SELECT elephant_id, device_id, timestamp, lat, lon FROM events"
    params = []
    if elephant and since:
        q += " WHERE elephant_id = ? AND timestamp >= ? ORDER BY timestamp ASC"
        params = [elephant, since]
    elif elephant:
        q += " WHERE elephant_id = ? ORDER BY timestamp ASC"
        params = [elephant]
    else:
        q += " ORDER BY timestamp ASC"
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(q, params)
    rows = cur.fetchall()
    conn.close()
    events = [{"elephant_id": r[0], "device_id": r[1], "timestamp": r[2], "lat": r[3], "lon": r[4]} for r in rows]
    return jsonify(events)

# Serve static files (map UI)
@app.route("/", defaults={"path": "index.html"})
@app.route("/<path:path>")
def serve(path):
    # serve files from website/ folder
    if os.path.exists(os.path.join(STATIC_FOLDER, path)):
        return send_from_directory(STATIC_FOLDER, path)
    return send_from_directory(STATIC_FOLDER, "index.html")

if __name__ == "__main__":
    init_db()
    print("Starting server on 0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)