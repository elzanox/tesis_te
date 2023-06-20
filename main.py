import cv2
import numpy as np
import time

# Path ke file weight YOLOv4 Tiny
weight_path = "yolo_conf/GUN_cnfg_v4tiny-416x416-00506_best.weights"

# Path ke file konfigurasi YOLOv4 Tiny
config_path = "yolo_conf/GUN_cnfg_v4tiny-416x416-00506.cfg"

# Path ke file label objek
label_path = "yolo_conf/classes-gun.txt"

# Load model YOLOv4 Tiny
net = cv2.dnn.readNetFromDarknet(config_path, weight_path)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

# net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
# net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

# Load label objek
with open(label_path, 'r') as f:
    labels = f.read().rstrip('\n').split('\n')

# Inisialisasi webcam
cap = cv2.VideoCapture(0)

# Inisialisasi variabel FPS
fps_start_time = time.time()
fps_frame_counter = 0

while True:
    # Baca frame dari webcam
    ret, frame = cap.read()

    if not ret:
        break

    fps_frame_counter += 1

    height, width, _ = frame.shape

    # Membuat input blob
    blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)

    # Set input blob ke model
    net.setInput(blob)

    # Jalankan forward pass
    output_layers_names = net.getUnconnectedOutLayersNames()
    layer_outputs = net.forward(output_layers_names)

    # Loop melalui setiap output layer
    for output in layer_outputs:
        # Loop melalui setiap deteksi objek
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5:
                # Koordinat bounding box
                box = detection[0:4] * np.array([width, height, width, height])
                (centerX, centerY, bbox_width, bbox_height) = box.astype("int")

                # Koordinat pojok kiri atas
                x = int(centerX - (bbox_width / 2))
                y = int(centerY - (bbox_height / 2))

                # Gambar bounding box dan label
                cv2.rectangle(frame, (x, y), (x + bbox_width, y + bbox_height), (0, 255, 0), 2)
                label = f"{labels[class_id]}: {confidence:.2f}"
                cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Tampilkan frame dengan deteksi objek
    cv2.imshow("Object Detection", frame)

    # Hitung FPS (Frame per Second)
    fps_end_time = time.time()
    fps = fps_frame_counter / (fps_end_time - fps_start_time)
    fps_text = f"FPS: {fps:.2f}"
    cv2.putText(frame, fps_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Tampilkan frame dengan informasi FPS
    cv2.imshow("Object Detection", frame)

    # Jika tombol 'ESC' ditekan, keluar dari loop
    key = cv2.waitKey(1)
    if key==27:
        break
# Tutup webcam dan jendela
cap.release()
cv2.destroyAllWindows()
