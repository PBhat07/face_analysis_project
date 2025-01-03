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

### 5. System Configuration

- **CPU Model**: Intel(R) Core(TM) i7-12700H, 2.30 GHz (12th Gen)
- **CPU Core Count**: 14 cores (6 performance cores and 8 efficiency cores)
- **OS**: Windows 11 Home, Version 23H2 (OS build 22631.4460)
- **RAM**: 16.0 GB (15.6 GB usable)

# Face Analysis Project

## Overview
The Face Analysis project aims to monitor real-time metrics such as blink count, frown detection, and proximity to the camera (too close detection). The solution uses **MediaPipe** for facial landmark detection and **OpenCV** for video capture and frame processing. The goal is to provide an efficient, real-time solution while optimizing for **CPU usage**, **memory consumption**, **latency**, and **accuracy**.

## Optimization Techniques and Trade-offs

To ensure the smooth performance of the Face Analysis application, various optimization techniques were employed. Below are the key optimizations, trade-offs made, and potential future improvements.

### 1. **Use of Lightweight Models and Frameworks**
   - **Optimization**: The project utilizes **MediaPipe** for facial landmark detection and **OpenCV** for real-time video capture. MediaPipe is a fast, optimized framework for real-time computer vision tasks.
   - **Reason**: MediaPipe provides pre-trained models optimized for **real-time performance**, reducing the need for building and training complex models from scratch.
   - **Trade-off**: While MediaPipe is highly efficient, it may not always provide the highest accuracy compared to custom-trained models. For example, fine-tuned models might detect subtle blinks or frowns more effectively.
   - **Future Improvement**: In the future, one could explore more sophisticated models like **YOLO** or **SSD** that offer better precision in detecting fast or subtle movements, although they may require more resources.


### 2. **Performance Monitoring and Logging**
   - **Optimization**: A **Performance Logger** was implemented to track **CPU** and **memory usage** at regular intervals using **psutil**. This allows real-time monitoring to ensure the system remains within acceptable resource limits.
   - **Reason**: Continuous performance tracking helps us optimize resource allocation and detect any potential bottlenecks during runtime.
   - **Trade-off**: Frequent performance logging introduces a minimal CPU overhead, especially if the logging frequency is set too high.
   - **Future Improvement**: Implementing **dynamic resource management**, where the system adjusts frame processing dynamically based on available resources (CPU, memory), could optimize resource usage further.

### 3. **Efficient Data Processing and Memory Management**
   - **Optimization**: We used memory-efficient techniques by reading and processing frames in chunks rather than processing all frames at once.
   - **Reason**: Video input can be large and memory-intensive. Processing in smaller chunks reduces the overall memory load.
   - **Trade-off**: Reducing memory usage can sometimes lead to a slight delay in processing if the system needs to buffer frames or reload data.
   - **Future Improvement**: **Frame caching** techniques could be used to store frames for future processing, reducing the need to reprocess frames and minimizing I/O latency.

### 4. **Latency Reduction through Optimized Algorithms**
   - **Optimization**: The algorithms used for **blink detection** and **distance estimation** were optimized for speed by using efficient operations like **Euclidean distance** for face width measurement and **numpy vectorization**.
   - **Reason**: Minimizing unnecessary operations and using vectorized functions speeds up frame processing and reduces overall latency.
   - **Trade-off**: Simplified algorithms may not detect every minute detail, potentially affecting precision in certain scenarios.
   - **Future Improvement**: Using **custom hardware accelerators** (e.g., **FPGA**) or more advanced algorithms could further reduce latency while improving detection accuracy.

### 5. **Accuracy vs. Performance Trade-offs**
   - **Optimization**: We carefully balanced **accuracy** and **performance** by using simplified models for real-time tasks. **MediaPipe**, while efficient, might not always detect all behaviors with the highest accuracy.
   - **Reason**: Real-time applications must strike a balance between **speed** and **accuracy**. Using heavy models can increase latency, while lighter models may sacrifice some accuracy.
   - **Trade-off**: A trade-off between **accuracy** (more complex models) and **real-time performance** (simpler models) was made, focusing on the latter to keep the application running efficiently.
   - **Future Improvement**: Advanced **neural networks** like **YOLO** or lightweight **CNNs** could be adopted to improve **accuracy** without compromising too much on **real-time performance**.

## **Further Improvements and Future Steps**
   - **Efficient Frame Processing Optimization**: Frame rate processing was adjusted to process every nth frame to reduce computational load.
   - **GPU Acceleration for Inference (Optional)**: GPU acceleration can be used with frameworks like **TensorFlow Lite** to speed up real-time inference.
   - **Custom AI Models**: In the future, we could develop **custom models** specifically tuned to our needs (e.g., blinking, frown detection), improving accuracy while maintaining performance.
   - **Advanced Profiling Tools**: Implementing more detailed **profiling tools** could provide deeper insights into system bottlenecks, helping to optimize the performance further based on the exact areas of inefficiency.

---






