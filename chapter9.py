import cv2

faceCascade = cv2.CascadeClassifier('Resources/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
while True:
    #img = cv2.imread('Resources/Face.png')
    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(imgGray, 1.1, 4)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    cv2.imshow('Result', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break