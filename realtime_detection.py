import cv2
import mediapipe as mp
import numpy as np
from collections import deque
from tensorflow.keras.models import load_model

# ==========================
# LOAD MODEL
# ==========================

model = load_model("models/fall_model.keras")

# ==========================
# MEDIAPIPE
# ==========================

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

# ==========================
# GLOBAL VARIABLES
# ==========================

latest_prediction = "Loading..."
latest_confidence = 0.0

# Number of consecutive fall predictions required
fall_counter = 0
FALL_THRESHOLD = 5

# ==========================
# VIDEO STREAM FUNCTION
# ==========================

def generate_frames():

    global latest_prediction
    global latest_confidence
    global fall_counter

    pose = mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Cannot open webcam")
        return

    sequence = deque(maxlen=30)

    while True:

        success, frame = cap.read()

        if not success:
            break

        frame = cv2.flip(frame, 1)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = pose.process(rgb)

        image = frame.copy()

        landmarks = []

        if results.pose_landmarks:

            mp_draw.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )

            for lm in results.pose_landmarks.landmark:

                landmarks.extend([
                    lm.x,
                    lm.y,
                    lm.z,
                    lm.visibility
                ])

        else:

            landmarks = [0] * 132

        sequence.append(landmarks)

        if len(sequence) == 30:

            X = np.array(sequence, dtype=np.float32)
            X = np.expand_dims(X, axis=0)

            prediction = model.predict(X, verbose=0)[0][0]

            latest_confidence = float(prediction)

            if prediction >= 0.85:

                fall_counter += 1

            else:

                fall_counter = 0

            if fall_counter >= FALL_THRESHOLD:

                latest_prediction = "FALL DETECTED"

                color = (0, 0, 255)

            else:

                latest_prediction = "NORMAL"

                color = (0, 255, 0)

            cv2.putText(
                image,
                latest_prediction,
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                color,
                2
            )

            cv2.putText(
                image,
                f"Confidence : {prediction:.2f}",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255,255,255),
                2
            )

        ret, buffer = cv2.imencode(".jpg", image)

        frame = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n'
            + frame +
            b'\r\n'
        )

    cap.release()
    pose.close()