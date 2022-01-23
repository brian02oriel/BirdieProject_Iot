import threading
import cv2
import numpy as np
from threading import Thread, Event, local
import time
from mongo_atlas import MongoConnection 



def manageDetection(label, x, y, w, h, img, count):
    print(label + ": (" + str(x) + ', '+ str(y) + ', '+ str(w) + ', '+ str(h) + ')')
    crop = img[y:y+h, x:x+w]
    imdir = 'captures/'+str(count)+'.jpg'
    cv2.imwrite(imdir, crop)
    #MongoConnection(imdir)
    time.sleep(5)
    running.clear()



def run_camera():
    # Load the network
    net = cv2.dnn.readNet('config/ssd_mobilenet_v3_small_coco_2020_01_14/frozen_inference_graph.pb', 'config/ssd_mobilenet_v3_small_coco_2020_01_14/ssd_mobilenet_v3_small_coco_2020_01_14.pbtxt')
    classes = []

    # Load labels
    with open('config/ssd_mobilenet_v3_small_coco_2020_01_14/imagenet.names', 'r') as f:
        classes = f.read().splitlines()

    cap = cv2.VideoCapture('birds.mp4')

    count = 0

    while(True):
        _, img = cap.read()
        height, width, _ = img.shape

        blob = cv2.dnn.blobFromImage(img, 1/255, (320, 320), (0, 0, 0), swapRB=True, crop=False)
        net.setInput(blob)
        output = net.forward()

        boxes = []
        confidences = []
        class_ids = []

        for detection in output[0, 0, :, :]:
            confidence = detection[2]
            if confidence > 0.5:
                class_id = detection[1]
                x = detection[3] * width
                y = detection[4] * height
                w = detection[5] * width
                h = detection[6] * height
                boxes.append([x, y, w, h])
                confidences.append((float(confidence)))
                class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        font = cv2.FONT_HERSHEY_COMPLEX
        #colors = np.random.uniform(0, 255, size=(len(boxes), 3))
        if len(indexes)>0:
            for i in indexes.flatten():
                x, y, w, h = boxes[i]
                label = str(classes[int(class_ids[i])])
                print(label)
                confidence = str(round(confidences[i]))
                copy = img.copy()
                if(label == "bird" and not running.is_set()):
                    running.set()
                    thread1 = Thread(target=manageDetection, args=(label, x, y, w, h, copy, count))
                    thread1.start()
                    count += 1
                elif (not running.is_set()):
                    running.clear()
                color = (26, 233, 1)
                #cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
                #cv2.rectangle(img, (x, y), (x+w, y-20), color, -1)
                #cv2.putText(img, label + " " + confidence, (x + 5 , y - 5), font, 0.5, (255, 255, 255), 1)

        cv2.imshow('Image', img)
        if(cv2.waitKey(1) & 0xFF == ord('q')):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    running = threading.Event()
    run_camera()

