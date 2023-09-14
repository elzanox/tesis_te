from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

# Inisialisasi objek VideoCapture
cap = cv2.VideoCapture(0)

# Periksa apakah kamera telah terbuka dengan sukses
if not cap.isOpened():
    print("Kamera tidak dapat diakses")
    exit()

def generate_frames():
    while True:
        # Membaca frame dari kamera
        ret, frame = cap.read()

        # Periksa apakah operasi pembacaan berhasil
        if not ret:
            print("Gagal membaca frame")
            break

        # Konversi frame ke format JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue

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
    app.run(debug=True,host='0.0.0.0')
