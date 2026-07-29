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

# ==========================
# VIDEO STREAM FUNCTION
# ==========================

def generate_frames():

    global latest_prediction
    global latest_confidence

    pose = mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    cap = cv2.VideoCapture(0)

    sequence = deque(maxlen=30)

    while True:

        success, frame = cap.read()

        if not success:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = pose.process(rgb)

        image = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

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

            X = np.expand_dims(sequence, axis=0)

            prediction = model.predict(X, verbose=0)[0][0]

            latest_confidence = float(prediction)

            if prediction > 0.5:

                latest_prediction = "FALL DETECTED"

                color = (0, 0, 255)

            else:

                latest_prediction = "NORMAL"

                color = (0, 255, 0)

            cv2.putText(
                image,
                f"{latest_prediction} ({prediction:.2f})",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                color,
                2
            )

        ret, buffer = cv2.imencode(".jpg", image)

        frame = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            frame +
            b'\r\n'
        )

    cap.release()
    pose.close()