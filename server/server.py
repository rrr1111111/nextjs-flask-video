from flask import Flask, Response, request
import cv2
import csv
import math
from pyzbar.pyzbar import decode
from ultralytics import YOLO
from detection import BarcodeDetector, QRCodeDetector

app = Flask(__name__)

# Initialize detectors
barcode_detector = BarcodeDetector()
qrcode_detector = QRCodeDetector()
model = YOLO('best.pt')  # Your custom-trained model
classNames = ['barcode', 'qrcode']

# Initialize webcam
cap = cv2.VideoCapture(0)

# Helper to initialize CSV

def generate_frames(detection_mode):
    while True:
        success, img = cap.read()
        if not success:
            break

        results = model(img, stream=True)
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cls = int(box.cls[0])
                classname = classNames[cls]
                confidence = math.ceil(box.conf[0] * 100)

                color = (0, 255, 0)
                if classname == 'barcode':
                    color = (255, 0, 0)
                    if detection_mode == 'barcode':
                        padding = 10
                        roi = img[max(0, y1-padding):min(img.shape[0], y2+padding),
                            max(0, x1-padding):min(img.shape[1], x2+padding)]
                        barcode_detector.decode_barcodes(img, roi)

                elif classname == 'qrcode':
                    color = (0, 0, 255)
                    if detection_mode == 'qrcode':
                        padding = 20
                        roi = img[max(0, y1-padding):min(img.shape[0], y2+padding),
                            max(0, x1-padding):min(img.shape[1], x2+padding)]
                        qrcode_detector.decode_qrcodes(img, roi)

                cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)
                cv2.putText(img, f"{classname} {confidence:.2f}%", (x1, y1-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return '''
    <h1>Choose Detection Mode:</h1>
    <a href="/video_feed?detection_mode=barcode">Barcode Detection</a><br>
    <a href="/video_feed?detection_mode=qrcode">QR Code Detection</a>
    '''

@app.route('/video_feed')
def video_feed():
    detection_mode = request.args.get('detection_mode', 'barcode')  # default barcode if not provided
    return Response(generate_frames(detection_mode),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True, port=5001)
