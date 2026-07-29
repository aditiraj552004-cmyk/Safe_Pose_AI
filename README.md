# 🩺 SafePose AI – Intelligent Real-Time Patient Fall Detection System

## 📌 Overview

SafePose AI is an AI-powered real-time patient monitoring system that detects human falls using computer vision and deep learning. The system utilizes **MediaPipe Pose** to extract human body landmarks and a **Long Short-Term Memory (LSTM)** deep learning model to classify activities as **Normal** or **Fall**. When a fall is detected, the system instantly triggers an emergency alarm, updates the web dashboard, and stores the event for future analysis.

The project is designed to improve patient safety in hospitals, elderly care centers, rehabilitation facilities, and home healthcare by enabling quick fall detection and timely caregiver response.

---

## ✨ Features

- 🎥 Real-time webcam monitoring
- 🤖 AI-powered fall detection using LSTM
- 🦴 Human pose estimation using MediaPipe
- 🚨 Instant emergency alarm on fall detection
- 📊 Live prediction confidence score
- 📝 Automatic fall event logging
- 🌐 Interactive Flask-based dashboard
- 📈 Fall history monitoring
- ⚡ Real-time video streaming
- 💻 Responsive HTML, CSS, and JavaScript interface

---

## 🛠️ Tech Stack

### Backend
- Python
- Flask

### AI & Machine Learning
- TensorFlow / Keras
- LSTM Neural Network
- MediaPipe Pose

### Computer Vision
- OpenCV
- NumPy

### Frontend
- HTML5
- CSS3
- JavaScript

### Data Handling
- CSV
- Pandas

---

## 📂 Project Structure

```text
SafePose_AI/
│
├── app.py
├── realtime_detection.py
├── preprocess.ipynb
├── train_Model.ipynb
│
├── models/
│   └── fall_model.keras
│
├── processed_data/
│
├── logs/
│   └── fall_history.csv
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   ├── js/
│   │   ├── app.js
│   │   ├── alarm.js
│   │   └── history.js
│   │
│   └── alarm.mp3
│
├── templates/
│   └── index.html
│
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/SafePose-AI.git
cd SafePose-AI
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows**

```bash
.venv\Scripts\activate
```

**Linux/macOS**

```bash
source .venv/bin/activate
```

### 4. Install the required libraries

```bash
pip install flask opencv-python mediapipe tensorflow numpy pandas scikit-learn
```

Or install using:

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Project

Start the Flask application:

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

## 🔄 Workflow

```text
Webcam
   │
   ▼
OpenCV Video Capture
   │
   ▼
MediaPipe Pose Detection
   │
   ▼
33 Pose Landmark Extraction
   │
   ▼
Feature Sequence Generation
   │
   ▼
LSTM Deep Learning Model
   │
   ▼
Normal / Fall Classification
   │
   ▼
Emergency Alarm Trigger
   │
   ▼
Dashboard Status Update
   │
   ▼
Fall Event Logging
```

---

## 📸 Dashboard Features

- Live camera feed
- Real-time fall prediction
- Confidence percentage
- Emergency alarm notification
- Reset alarm button
- Fall detection history table
- Clean and responsive user interface

---

## 📦 Required Libraries

- Flask
- OpenCV
- TensorFlow
- MediaPipe
- NumPy
- Pandas
- Scikit-learn

Install all dependencies using:

```bash
pip install flask opencv-python mediapipe tensorflow numpy pandas scikit-learn
```

---

## 🚀 Future Enhancements

- SMS alerts using Twilio
- Email notifications
- Cloud database integration
- Patient profile management
- Multi-camera monitoring
- Android application
- IoT healthcare integration
- Analytics dashboard with graphs and reports
- Doctor and caregiver portal
- Cloud deployment

---

## 👨‍💻 Author

**Aditi Raj**

B.Tech Computer Science Engineering (AI & ML)

---

## 📄 License

This project is developed for educational, research, and academic purposes. You are free to use, modify, and enhance the project with proper attribution.