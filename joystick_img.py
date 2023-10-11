
import cv2
import time
from flask import jsonify
from waitress import serve
from flask import Flask, render_template, Response, stream_with_context, request, json, jsonify
import paho.mqtt.client as mqtt

mqtt_broker = "103.150.93.184"  # Ganti dengan alamat broker MQTT Anda
mqtt_port = 1883  # Ganti dengan port broker MQTT Anda
mqtt_topic = "CONTROL"  # Ganti dengan topik MQTT yang Anda inginkan

def on_connect(client, userdata, flags, rc):
    print("Terhubung dengan MQTT Broker dengan kode:", rc)
    client.subscribe(mqtt_topic)

def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    print("Menerima pesan MQTT:", payload)
    # Tambahkan logika untuk menangani pesan MQTT sesuai kebutuhan Anda


# Inisialisasi objek VideoCapture
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
app = Flask(__name__)
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(mqtt_broker, mqtt_port, keepalive=60)
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
    mqtt_client.loop_start()
    serve(app, host='0.0.0.0', port=5000, threads=2)