import threading
import cv2
import numpy as np
from threading import Thread, Event, local
import time
from mongo_atlas import MongoConnection 



def manageDetection(label, x, y, w, h, img, count):
    print(label + ": (" + str(x) + ', '+ str(y) + ', '+ str(w) + ', '+ str(h) + ')')
    crop = img[x: x+w, y: y+h]
    imdir = 'captures/'+str(count)+'.jpg'
    cv2.imwrite(imdir, crop)
    MongoConnection(imdir)
    time.sleep(5)
    running.clear()



def run_camera():
    # Load the network
    net = cv2.dnn.readNet('config/yolo/yolov3-tiny.weights', 'config/yolo/yolov3-tiny.cfg')
    classes = []

    # Load labels
    with open('config/yolo/coco.names', 'r') as f:
        classes = f.read().splitlines()

    cap = cv2.VideoCapture('birds.mp4')

    count = 0

    while(True):
        _, img = cap.read()
        height, width, _ = img.shape

        blob = cv2.dnn.blobFromImage(img, 1/255, (416, 416), (0, 0, 0), swapRB=True, crop=False)
        net.setInput(blob)
        output_layers_names = net.getUnconnectedOutLayersNames()
        layer_outputs = net.forward(output_layers_names)

        boxes = []
        confidences = []
        class_ids = []

        for output in layer_outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0]*width)
                    center_y = int(detection[1]*height)
                    w = int(detection[2]*width)
                    h = int(detection[3]*height)

                    x = int(center_x - w/2)
                    y = int(center_y - h/2)

                    boxes.append([x, y, w, h])
                    confidences.append((float(confidence)))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        font = cv2.FONT_HERSHEY_COMPLEX
        #colors = np.random.uniform(0, 255, size=(len(boxes), 3))
        if len(indexes)>0:
            for i in indexes.flatten():
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                confidence = str(round(confidences[i]))
                copy = img.copy()
                if(label == "person" and not running.is_set()):
                    running.set()
                    thread1 = Thread(target=manageDetection, args=(label, x, y, w, h, copy, count))
                    thread1.start()
                    count += 1
                elif (not running.is_set()):
                    running.clear()
                color = (26, 233, 1)
                cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
                cv2.rectangle(img, (x, y), (x+w, y-20), color, -1)
                cv2.putText(img, label + " " + confidence, (x + 5 , y - 5), font, 0.5, (255, 255, 255), 1)
                


        cv2.imshow('Image', img)
        if(cv2.waitKey(1) & 0xFF == ord('q')):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    running = threading.Event()
    run_camera()

