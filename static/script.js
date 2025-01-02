const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const blinks = document.getElementById('blinks');
const frowns = document.getElementById('frowns');
const tooClose = document.getElementById('too_close');
const fps = document.getElementById('fps');
const latency = document.getElementById('latency');
const precision = document.getElementById('precision');
const recall = document.getElementById('recall');
const accuracy = document.getElementById('accuracy');
const startButton = document.getElementById('start');
const stopButton = document.getElementById('stop');
let capturing = false;

// Access the webcam
navigator.mediaDevices.getUserMedia({ video: true })
    .then((stream) => {
        video.srcObject = stream;
    })
    .catch((err) => {
        alert('Error accessing webcam: ' + err.message);
    });

// Start Capture
startButton.addEventListener('click', () => {
    fetch('/start_capture', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            capturing = true;
            captureFrames();
        });
});

// Stop Capture
stopButton.addEventListener('click', () => {
    fetch('/stop_capture', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            capturing = false;
            const results = data.results;
            blinks.textContent = `Blinks: ${results.blink_count}`;
            frowns.textContent = `Frowns: ${results.frown_count}`;
            tooClose.textContent = `Too Close: ${results.too_close_count}`;
            fps.textContent = `FPS: ${results.fps.toFixed(2)}`;
            latency.textContent = `Latency: ${results.total_latency.toFixed(2)} ms`;
            precision.textContent = `Precision: ${results.precision_blink.toFixed(2)}`;
            recall.textContent = `Recall: ${results.recall_blink.toFixed(2)}`;
            accuracy.textContent = `Accuracy: ${(results.accuracy || 0).toFixed(2)}`;
        });
});

function captureFrames() {
    if (!capturing) return;

    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    const frame = canvas.toDataURL('image/jpeg');

    fetch('/process_frame', {
        method: 'POST',
        body: dataURItoBlob(frame),
        headers: { 'Content-Type': 'application/octet-stream' }
    })
    .then(response => response.json())
    .then(data => {
        blinks.textContent = `Blinks: ${data.results.blink_count}`;
        frowns.textContent = `Frowns: ${data.results.frown_count}`;
        tooClose.textContent = `Too Close: ${data.results.too_close_count}`;
        fps.textContent = `FPS: ${data.results.fps.toFixed(2)}`;
        latency.textContent = `Latency: ${data.results.total_latency.toFixed(2)} ms`;
    });

    setTimeout(captureFrames, 100);
}

function dataURItoBlob(dataURI) {
    const byteString = atob(dataURI.split(',')[1]);
    const arrayBuffer = new ArrayBuffer(byteString.length);
    const uint8Array = new Uint8Array(arrayBuffer);
    for (let i = 0; i < byteString.length; i++) {
        uint8Array[i] = byteString.charCodeAt(i);
    }
    return new Blob([uint8Array], { type: 'image/jpeg' });
}
