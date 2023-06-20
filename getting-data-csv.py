import cv2
import numpy as np

file_name = 'hasil_data.csv'
my_file = open(file_name, 'w', encoding='utf-8')
#f = open("test.txt", "w")

# net = cv2.dnn.readNet('yolo_conf/weights/gun_v3tiny-2502_best.weights', 'yolo_conf/gun_v3tiny-2502.cfg')
net = cv2.dnn.readNet('yolo_conf/weights/gun_v4tiny-0603_best.weights', 'yolo_conf/gun_v4tiny-0603.cfg')
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
classes = []
with open("yolo_conf/classes-gun.txt", "r") as f:
    classes = f.read().splitlines()

cap = cv2.VideoCapture('media/gun_test1.mp4')
font = cv2.FONT_HERSHEY_PLAIN
colors = np.random.uniform(0, 255, size=(100, 3))

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
   
size = (frame_width, frame_height)
result = cv2.VideoWriter('result.avi', 
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         10, size)

while True:
    _, img = cap.read()
        
    height, width, _ = img.shape

    blob = cv2.dnn.blobFromImage(img, 1/255, (312, 312), (0,0,0), swapRB=True, crop=False)
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
            if confidence > 0.2:
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
            daftar.append(label)
            data = str(daftar)
            center_rect = (center_x,center_y)
            #confidence = str(round(confidences[i],2)*100)
            color = colors[i]
            cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
            cv2.putText(img,label, (x,y), font, 1, (0,255,0), 2)
            cv2.putText(img,confidence_print, (x+50,y), font, 1, (0,255,0), 2)
            cv2.circle(img, center_rect, radius=1, color=(0, 0, 255), thickness=2)
            #with open(filename, 'w', encoding='utf-8') as my_file:
            my_file.write(label+","+confidence_print+","+str(center_x)+","+str(+center_y) +'\n')
                #print(my_file.closed)  # 👉️ False
    result.write(img)	                    
    print(daftar)
    cv2.imshow('Image', img)
    
    key = cv2.waitKey(1)
    if key==27:
        break
my_file.close()
result.release()
cap.release()
cv2.destroyAllWindows()
