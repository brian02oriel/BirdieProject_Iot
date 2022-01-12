import cv2

bird_cascade = cv2.CascadeClassifier("bird_haar_cascade.xml")

cap = cv2.VideoCapture()

while True:
	_, img = cap.read()
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	birds = bird_cascade.detectMultiScale(gray, 1.3, 5)
	
	for(x, y, w, h) in birds:
		
