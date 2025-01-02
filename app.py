from flask import Flask, render_template, request, jsonify
import cv2
import mediapipe as mp
import numpy as np
import time
from performance_logger import PerformanceLogger

app = Flask(__name__)

# Mediapipe initialization
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True, min_detection_confidence=0.5)

# Global variables
capture_active = False
start_time = None
frame_count = 0
results = {
    "blink_count": 0,
    "frown_count": 0,
    "too_close_count": 0,
    "frames_processed": 0,
    "total_latency": 0,
    "fps": 0,
    "precision_blink": 0.0,
    "recall_blink": 0.0,
    "precision_frown": 0.0,
    "recall_frown": 0.0,
    "precision_too_close": 0.0,
    "recall_too_close": 0.0
}
ground_truth = {
    "blinks": 5,  # Simulated ground truth for blinks
    "frowns": 2,  # Simulated ground truth for frowns
    "too_close": 3  # Simulated ground truth for too-close events
}
logger = None  # Performance logger instance

# Blink detection
def calculate_ear(eye_landmarks):
    p1, p2, p3, p4, p5, p6 = eye_landmarks
    vertical1 = np.linalg.norm(p2 - p6)
    vertical2 = np.linalg.norm(p3 - p5)
    horizontal = np.linalg.norm(p1 - p4)
    return (vertical1 + vertical2) / (2.0 * horizontal)

# Frown detection
def detect_frown(face_landmarks):
    left_eyebrow = np.array([[p.x, p.y] for p in face_landmarks.landmark[70:94]])
    left_eye = np.array([[p.x, p.y] for p in face_landmarks.landmark[33:42]])
    avg_eyebrow_height = np.mean(left_eyebrow[:, 1])
    avg_eye_height = np.mean(left_eye[:, 1])
    return avg_eyebrow_height - avg_eye_height < 0.04



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_capture', methods=['POST'])
def start_capture():
    """Start the monitoring pipeline."""
    global capture_active, start_time, frame_count, results, logger
    capture_active = True
    start_time = time.time()
    frame_count = 0
    results = {
        "blink_count": 0,
        "frown_count": 0,
        "too_close_count": 0,
        "frames_processed": 0,
        "total_latency": 0,
        "fps": 0,
        "precision_blink": 0.0,
        "recall_blink": 0.0,
        "precision_frown": 0.0,
        "recall_frown": 0.0,
        "precision_too_close": 0.0,
        "recall_too_close": 0.0
    }
    logger = PerformanceLogger()  # Automatically creates a timestamped log file
    logger.start()
    return jsonify({"message": "Capture started"})

@app.route('/stop_capture', methods=['POST'])
def stop_capture():
    """Stop the monitoring pipeline."""
    global capture_active, logger
    capture_active = False
    if logger:
        logger.stop()

    # Calculate precision and recall for each sub-problem
    results["precision_blink"] = (
        results["blink_count"] / (results["blink_count"] + (ground_truth["blinks"] - results["blink_count"]))
        if results["blink_count"] else 0
    )
    results["recall_blink"] = (
        results["blink_count"] / ground_truth["blinks"]
        if ground_truth["blinks"] else 0
    )
    results["precision_frown"] = (
        results["frown_count"] / (results["frown_count"] + (ground_truth["frowns"] - results["frown_count"]))
        if results["frown_count"] else 0
    )
    results["recall_frown"] = (
        results["frown_count"] / ground_truth["frowns"]
        if ground_truth["frowns"] else 0
    )
    results["precision_too_close"] = (
        results["too_close_count"] / (results["too_close_count"] + (ground_truth["too_close"] - results["too_close_count"]))
        if results["too_close_count"] else 0
    )
    results["recall_too_close"] = (
        results["too_close_count"] / ground_truth["too_close"]
        if ground_truth["too_close"] else 0
    )

    elapsed_time = time.time() - start_time
    results["fps"] = frame_count / elapsed_time if elapsed_time > 0 else 0

    # Log summary in performance log
    with open(logger.log_filename, 'a') as log_file:
        log_file.write("\nSummary:\n")
        log_file.write(f"Blinks Detected: {results['blink_count']}\n")
        log_file.write(f"Frowns Detected: {results['frown_count']}\n")
        log_file.write(f"Too Close Count: {results['too_close_count']}\n")
        log_file.write(f"Precision (Blink): {results['precision_blink']:.2f}\n")
        log_file.write(f"Recall (Blink): {results['recall_blink']:.2f}\n")
        log_file.write(f"Precision (Frown): {results['precision_frown']:.2f}\n")
        log_file.write(f"Recall (Frown): {results['recall_frown']:.2f}\n")
        log_file.write(f"Precision (Too Close): {results['precision_too_close']:.2f}\n")
        log_file.write(f"Recall (Too Close): {results['recall_too_close']:.2f}\n")
        log_file.write(f"Average FPS: {results['fps']:.2f}\n")
        log_file.write(f"Total Latency: {results['total_latency']:.2f} ms\n")

    return jsonify({"message": "Capture stopped", "results": results})

@app.route('/process_frame', methods=['POST'])
def process_frame():
    """Process a single frame."""
    global capture_active, results, frame_count

    if not capture_active:
        return jsonify({"message": "Capture not active", "results": results})

    start_processing_time = time.time()
    frame_count += 1

    # Read the frame from the request
    frame_data = request.data
    frame = np.frombuffer(frame_data, np.uint8)
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process with Mediapipe
    results["frames_processed"] += 1
    processed_results = face_mesh.process(rgb_frame)

    if processed_results.multi_face_landmarks:
        for face_landmarks in processed_results.multi_face_landmarks:
            # Blink detection
            left_eye_indices = [362, 385, 387, 263, 373, 380]
            right_eye_indices = [33, 160, 158, 133, 153, 144]
            left_eye = np.array([[face_landmarks.landmark[i].x, face_landmarks.landmark[i].y] for i in left_eye_indices])
            right_eye = np.array([[face_landmarks.landmark[i].x, face_landmarks.landmark[i].y] for i in right_eye_indices])

            left_ear = calculate_ear(left_eye)
            right_ear = calculate_ear(right_eye)
            if left_ear < 0.2 and right_ear < 0.2:
                results["blink_count"] += 1

            # Frown detection
            if detect_frown(face_landmarks):
                results["frown_count"] += 1

            # Distance estimation
            face_width = np.linalg.norm(
                np.array([face_landmarks.landmark[454].x, face_landmarks.landmark[454].y]) -
                np.array([face_landmarks.landmark[234].x, face_landmarks.landmark[234].y])
            )
            distance = 1 / face_width * 10
            if distance < 20:  # Too close
                results["too_close_count"] += 1

    # Calculate latency
    frame_latency = (time.time() - start_processing_time) * 1000
    results["total_latency"] += frame_latency

    # Stop after 2 minutes or 3,600 frames
    elapsed_time = time.time() - start_time
    if elapsed_time >= 120 or frame_count >= 3600:
        stop_capture()
        return jsonify({"message": "Processing complete", "results": results})

    return jsonify({"message": "Frame processed", "results": results})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)