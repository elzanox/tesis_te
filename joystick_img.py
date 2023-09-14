
import cv2
import numpy as np

import time
import requests
from flask import jsonify
from collections import Counter
from datetime import datetime
from waitress import serve
from flask import Flask, render_template, Response, stream_with_context, request, json, jsonify


# Inisialisasi objek VideoCapture
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
app = Flask(__name__)

# Periksa apakah kamera telah terbuka dengan sukses
if not cap.isOpened():
    print("Kamera tidak dapat diakses")
    exit()

def generate_frames():
    ret, frame = cap.read()
    while True:
        # Membaca frame dari kamera
        ret, frame = cap.read()
        # Periksa apakah operasi pembacaan berhasil
        if not ret:
            print("Gagal membaca frame")
            break
        else:
            time.sleep(0.1)
            # Konversi frame ke format JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            # if not ret:
            #     continue

            # Menyediakan frame sebagai byte stream
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # app.run(debug=True,host='0.0.0.0')
    serve(app, host='0.0.0.0', port=5000, threads=2)