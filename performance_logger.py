import time
import psutil
import csv
import threading
from datetime import datetime

class PerformanceLogger:
    """
    A lightweight logger that records CPU, memory usage, and additional metrics
    at regular intervals.
    """
    def __init__(self, log_filename=None, interval=1.0):
        """
        :param log_filename: Path for the output CSV file.
        :param interval: Time (in seconds) between each sampling of
                         CPU/memory usage.
        """
        # Use a timestamped log file name if none is provided
        if log_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_filename = f"performance_log_{timestamp}.csv"
        self.log_filename = log_filename
        self.interval = interval
        self._stop_flag = False
        self._thread = None
        self._process = psutil.Process()  # Track the current process
        self.metrics = {
            "blink_count": 0,
            "frown_count": 0,
            "too_close_count": 0,
            "fps": 0,
            "latency": 0
        }

    def start(self):
        """Start logging in a background thread."""
        self._stop_flag = False
        self._thread = threading.Thread(target=self._log_loop, daemon=True)
        self._thread.start()

    def stop(self):
        """Signal the logger to stop and wait for the thread to finish."""
        self._stop_flag = True
        if self._thread and self._thread.is_alive():
            self._thread.join()

    def update_metrics(self, blink_count, frown_count, too_close_count, fps, latency):
        """
        Update the custom metrics for logging.
        """
        self.metrics["blink_count"] = blink_count
        self.metrics["frown_count"] = frown_count
        self.metrics["too_close_count"] = too_close_count
        self.metrics["fps"] = fps
        self.metrics["latency"] = latency

    def _log_loop(self):
        """Internal loop that writes CPU, memory, and metrics to CSV at each interval."""
        with open(self.log_filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Write the header row
            writer.writerow(["timestamp", "cpu_percent", "memory_mb",
                             "blink_count", "frown_count", "too_close_count",
                             "fps", "latency"])
            # Prime the CPU percent measurement
            self._process.cpu_percent(interval=None)

            while not self._stop_flag:
                timestamp = time.time()
                cpu_percent = self._process.cpu_percent(interval=None)
                mem_info = self._process.memory_info()
                memory_mb = mem_info.rss / (1024 * 1024)  # Resident Set Size (RSS) in MB
                writer.writerow([
                    timestamp, cpu_percent, memory_mb,
                    self.metrics["blink_count"],
                    self.metrics["frown_count"],
                    self.metrics["too_close_count"],
                    self.metrics["fps"],
                    self.metrics["latency"]
                ])
                time.sleep(self.interval)
