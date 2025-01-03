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
  ```

### 2. Setup virtual environment
 ```bash
# Create virtual environment
python3 -m venv venv
 

# Activate virtual environment (Linux/Mac)
source venv/bin/activate
 ```

### 3.Install Required Dependencies
 ```bash
pip install opencv-python mediapipe numpy flask psutil
 ```

### 4. Run the application
 ```bash
python app.py
 ```

## 5. System Configuration

- **CPU Model**: Intel(R) Core(TM) i7-12700H, 2.30 GHz (12th Gen)
- **CPU Core Count**: 14 cores (6 performance cores and 8 efficiency cores)
- **OS**: Windows 11 Home, Version 23H2 (OS build 22631.4460)
- **RAM**: 16.0 GB (15.6 GB usable)




