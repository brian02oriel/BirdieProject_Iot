import cv2

bird_cascade = cv2.CascadeClassifier("bird_haar_cascade.xml")

cap = cv2.VideoCapture('funny_birds.mp4')

while True:
	_, img = cap.read()
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	birds = bird_cascade.detectMultiScale(gray, 1.3, 5)
	
	for(x, y, w, h) in birds:
		cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
	cv2.imshow('Image', img)
	if(cv2.waitKey(1) & 0xFF == ord('q')):
		break
cap.release()
cv2.destroyAllWindows()
