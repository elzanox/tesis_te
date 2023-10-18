import cv2
import numpy as np
import time
from waitress import serve
from flask import Flask, render_template, Response, stream_with_context, request, json, jsonify
# weights_path    = 'batch1/GUN_cnfg_v3tiny-416x416-2506_best.weights'
# config_path     = 'batch1/GUN_cnfg_v3tiny-416x416-2506.cfg'

# weights_path    = 'batch1/GUN_cnfg_v4tiny-416x416-2806_best.weights'
# config_path     = 'batch1/GUN_cnfg_v4tiny-416x416-2806.cfg'

# weights_path    = 'batch1/GUN_cnfg_v7tiny-416x416-2606_best.weights'
# config_path     = 'batch1/GUN_cnfg_v7tiny-416x416-2606.cfg'

weights_path    = 'batch2/GUN_cnfg_yoloq3-tiny-416x416-2806_best.weights'
config_path     = 'batch2/GUN_cnfg_yolov3-tiny-416x416-2806.cfg'

# weights_path    = 'batch2/GUN_cnfg_yolov4-tiny-416x416-2806_best.weights'
# config_path     = 'batch2/GUN_cnfg_yolov4-tiny-416x416-2806.cfg'

# weights_path    = 'batch2/GUN_cnfg_yolov7-tiny-416x416-2906_best.weights'
# config_path     = 'batch2/GUN_cnfg_yolov7-tiny-416x416-2906.cfg'

classes_path    = 'yolo_conf/classes-gun.txt'
testvid_path    = 'media/gun_test1.mp4'
imgsz = 416


# weights_path    = 'yolo_conf/yolov4-csp-s-mish.weights'
# config_path     = 'yolo_conf/yolov4-csp-s-mish.cfg'
# classes_path    = 'yolo_conf/coco.txt'
net = cv2.dnn.readNet(weights_path, config_path)

net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

# net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
# net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

classes = []
with open(classes_path, "r") as f:
    classes = f.read().splitlines()

font = cv2.FONT_HERSHEY_DUPLEX
font2 = cv2.FONT_HERSHEY_COMPLEX

# create a color random by numpy
colors = np.random.uniform(0, 255, size=(100, 3))

cap = cv2.VideoCapture('media/output_video.mp4')
# cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
# Inisialisasi objek VideoWriter untuk menyimpan video
rec_fps = 30
rec_format = ".mp4"
rec_fourcc = "mp4v"
rec_frame_width = int(cap.get(3))
rec_frame_height = int(cap.get(4))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Format kompresi MP4
out = cv2.VideoWriter('yolov3tiny_output.mp4', cv2.VideoWriter_fourcc(*rec_fourcc), rec_fps, (rec_frame_width, rec_frame_height))  # Ganti nama file, frame rate, dan resolusi sesuai kebutuhan

port = 5000

# create a variable name of Flask
app = Flask('__name__')
def video_stream():
    _, img = cap.read()
    # Inisialisasi variabel FPS
    fps_start_time = time.time()
    fps_frame_counter = 0
    while True:
        _, img = cap.read()
        if not _:
            break
        else:
            
            # _, img = cap.read()
            fps_frame_counter += 1
            height, width, _ = img.shape
            blob = cv2.dnn.blobFromImage(img, 1/255, (imgsz, imgsz), (0,0,0), swapRB=True, crop=False)
            net.setInput(blob)
            output_layers_names = net.getUnconnectedOutLayersNames()
            layerOutputs = net.forward(output_layers_names)
            boxes = []
            confidences = []
            class_ids = []
            
            for output in layerOutputs:
                for detection in output:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.3:
                        center_x = int(detection[0]*width)
                        center_y = int(detection[1]*height)
                        w = int(detection[2]*width)
                        h = int(detection[3]*height)
                        x = int(center_x - w/2)
                        y = int(center_y - h/2)
                        boxes.append([x, y, w, h])
                        confidences.append((float(confidence)))
                        class_ids.append(class_id)
            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.2, 0.4)
            daftar = []
            if len(indexes)>0:
                for i in indexes.flatten():
                    x, y, w, h = boxes[i]
                    confidence_round = round(confidences[i],2)*100
                    confidence_print = ("%.2f" % confidence_round)
                    label = str(classes[class_ids[i]])
                    color = colors[i]
                    daftar.append(label)
                    data = str(daftar)
                    center_rect = (center_x,center_y)
                    confidence = str(round(confidences[i],2)*100)
                    
                    # Mendapatkan ukuran teks label
                    (label_width, label_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
                    # Gambar background label
                    cv2.rectangle(img, (x, y - label_height - 20), (x + label_width + 70, y), color=(0,255,0), thickness = -1)
                    
                    cv2.rectangle(img, (x,y), (x+w, y+h), color=(0,255,0),thickness = 2)
                    cv2.putText(img,label, (x,y-10), font, 1, color = (255,255,255), thickness = 2)
                    cv2.putText(img,confidence_print, (x+135,y-10), font2, 1, color = (255,255,255), thickness = 2)
                    cv2.circle(img, center_rect, radius=1, color=(0,0,255), thickness=2)
            # Hitung FPS (Frame per Second)
            fps_end_time = time.time()
            fps = fps_frame_counter / (fps_end_time - fps_start_time)
            fps_text = f"FPS: {fps:.2f}"
            cv2.rectangle(img, (10, 5), (190,35), color=(0,255,0), thickness = -1)
            cv2.putText(img, fps_text, (10, 30), font, 1, (255, 255, 255), 2)
            cv2.imshow('Image', img)
            # Simpan frame ke dalam file MP4
            out.write(img)
            key = cv2.waitKey(1)
            if key==27:
                # break
                cap.release()
                cv2.destroyAllWindows()
                
            _, buffer = cv2.imencode('.jpg', img)
            # if not ret:
            #     continue

            # Menyediakan frame sebagai byte stream
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/')
def video_feed():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # app.run(host='0.0.0.0',port='5000', debug=False)
    print('Starting server in localhost:'+str(port))
    serve(app, host='0.0.0.0', port=port, threads=2)
