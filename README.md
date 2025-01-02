# Face Analysis Project 

This project uses **Computer Vision**  to analyze the user's face in real-time. It performs tasks such as **blink detection**, **distance estimation from the camera**, and **frown detection**.

## Features

- **Blink Detection**: The system detects blinks by measuring the Eye Aspect Ratio (EAR).
- **Distance Estimation**: Estimates the user's distance from the camera using face landmarks.
- **Frown Detection**: Detects frowns based on eyebrow and eye movements.
- **Performance Metrics**: Logs performance data including CPU usage, memory usage, FPS, and latency.
- **Accuracy Calculation**: Calculates precision, recall, and accuracy for blink count, distance, and frown detection.

## Project Setup

To get started with the project, follow these steps:

### 1. Clone the Repository
Clone this repository to your local machine:
 ```bash
git clone https://github.com/PBhat07/face_analysis_project.git
cd face_analysis_project

### 2. Setup virtual environment
# Create virtual environment
python3 -m venv venv

# Activate virtual environment (Linux/Mac)
source venv/bin/activate

### 3.Install Required Dependencies
pip install opencv-python mediapipe numpy flask psutil

### 4. Run the application
python app.py



