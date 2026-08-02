import time
from flask import Flask, render_template, Response, jsonify
import realtime_detection

from datetime import datetime
import csv
import os


app = Flask(__name__)


# -------------------------------
# Global Alarm Status
# -------------------------------

alarm_status = {

    "fall_detected": False,
    "confidence": 0,
    "time": 0

}


# -------------------------------
# Save Fall Event Log
# -------------------------------

def save_fall_event(confidence):

    file_path = "logs/fall_history.csv"


    # create logs folder if not exists
    os.makedirs("logs", exist_ok=True)


    file_exists = os.path.isfile(file_path)


    with open(
        file_path,
        "a",
        newline=""
    ) as file:


        writer = csv.writer(file)


        if not file_exists:

            writer.writerow(
                [
                    "Time",
                    "Prediction",
                    "Confidence",
                    "Status"
                ]
            )


        writer.writerow(
            [
                datetime.now(),
                "Fall",
                confidence,
                "Alert Sent"
            ]
        )



# -------------------------------
# Home Dashboard
# -------------------------------

@app.route("/")
def home():

    return render_template(
        "index.html"
    )



# -------------------------------
# Live Video Feed
# -------------------------------

@app.route("/video_feed")
def video_feed():

    return Response(

        realtime_detection.generate_frames(),

        mimetype=
        "multipart/x-mixed-replace; boundary=frame"

    )



# -------------------------------
# Prediction Status API
# -------------------------------

@app.route("/status")
def status():

    prediction = realtime_detection.latest_prediction
    confidence = realtime_detection.latest_confidence * 100

    # ---------------------------
    # Fall Detected
    # ---------------------------
    if prediction == "FALL DETECTED":

        # Trigger only once for each new fall
        if not alarm_status["fall_detected"]:

            alarm_status["fall_detected"] = True
            alarm_status["confidence"] = round(confidence, 2)

            # Store current timestamp (seconds)
            alarm_status["time"] = time.time()

            save_fall_event(round(confidence, 2))

    # ---------------------------
    # Normal Condition
    # ---------------------------
    else:

        # Stop alarm automatically when person is normal
        alarm_status["fall_detected"] = False

    # ---------------------------
    # Auto Reset After 10 Seconds
    # ---------------------------
    if alarm_status["fall_detected"]:

        elapsed = time.time() - alarm_status["time"]

        if elapsed >= 10:

            alarm_status["fall_detected"] = False

    # ---------------------------
    # Return Status
    # ---------------------------
    return jsonify({

        "prediction": prediction,

        "confidence": round(confidence, 2),

        "alarm": alarm_status["fall_detected"]

    })

# -------------------------------
# Reset Alarm
# -------------------------------

@app.route("/reset_alarm")
def reset_alarm():

    alarm_status["fall_detected"] = False
    alarm_status["confidence"] = 0
    alarm_status["time"] = 0

    return jsonify({
        "message": "Alarm Reset"
    })



# -------------------------------
# Fall History API
# -------------------------------

@app.route("/history")
def history():

    events = []


    file_path = (
        "logs/fall_history.csv"
    )


    if os.path.exists(file_path):


        with open(
            file_path,
            "r"
        ) as file:


            reader = csv.DictReader(
                file
            )


            for row in reader:

                events.append(row)



    return jsonify(events)



# -------------------------------
# Run Flask
# -------------------------------

if __name__ == "__main__":

    app.run(
        debug=True
    )