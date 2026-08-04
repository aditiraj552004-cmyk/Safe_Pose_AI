import os
import csv
import time
from datetime import datetime

from flask import Flask, render_template, Response, jsonify

import realtime_detection

# ===============================
# FLASK APP
# ===============================

app = Flask(__name__)

# ===============================
# GLOBAL ALARM STATUS
# ===============================

alarm_status = {
    "fall_detected": False,
    "confidence": 0,
    "time": 0
}

# ===============================
# CREATE LOG FOLDER
# ===============================

os.makedirs("logs", exist_ok=True)

LOG_FILE = "logs/fall_history.csv"

# ===============================
# SAVE FALL EVENT
# ===============================

def save_fall_event(confidence):

    file_exists = os.path.exists(LOG_FILE)

    with open(LOG_FILE, "a", newline="") as file:

        writer = csv.writer(file)

        if not file_exists:

            writer.writerow([
                "Time",
                "Prediction",
                "Confidence (%)",
                "Status"
            ])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Fall Detected",
            round(confidence, 2),
            "Alert Sent"
        ])

# ===============================
# HOME PAGE
# ===============================

@app.route("/")
def home():
    return render_template("index.html")

# ===============================
# LIVE VIDEO
# ===============================

@app.route("/video_feed")
def video_feed():

    return Response(
        realtime_detection.generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

# ===============================
# STATUS API
# ===============================

@app.route("/status")
def status():

    prediction = realtime_detection.latest_prediction
    confidence = realtime_detection.latest_confidence * 100

    if prediction == "FALL DETECTED":

        if not alarm_status["fall_detected"]:

            alarm_status["fall_detected"] = True
            alarm_status["confidence"] = round(confidence, 2)
            alarm_status["time"] = time.time()

            save_fall_event(confidence)

    else:

        alarm_status["fall_detected"] = False

    if alarm_status["fall_detected"]:

        elapsed = time.time() - alarm_status["time"]

        if elapsed >= 10:

            alarm_status["fall_detected"] = False

    return jsonify({

        "prediction": prediction,

        "confidence": round(confidence, 2),

        "alarm": alarm_status["fall_detected"]

    })

# ===============================
# RESET ALARM
# ===============================

@app.route("/reset_alarm")
def reset_alarm():

    alarm_status["fall_detected"] = False
    alarm_status["confidence"] = 0
    alarm_status["time"] = 0

    return jsonify({
        "message": "Alarm Reset Successfully"
    })

# ===============================
# FALL HISTORY
# ===============================

@app.route("/history")
def history():

    events = []

    if os.path.exists(LOG_FILE):

        with open(LOG_FILE, "r") as file:

            reader = csv.DictReader(file)

            for row in reader:

                events.append(row)

    return jsonify(events)

# ===============================
# HEALTH CHECK
# ===============================

@app.route("/health")
def health():

    return jsonify({
        "status": "running",
        "prediction": realtime_detection.latest_prediction
    })

# ===============================
# RUN APP
# ===============================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
        threaded=True
    )