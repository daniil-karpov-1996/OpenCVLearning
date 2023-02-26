import cv2
import numpy as np


def preProcessing(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgCanny = cv2.Canny(imgBlur, 200, 200)
    kernel = np.ones((5, 5))
    imgDial = cv2.dilate(imgCanny, kernel, iterations=2)
    imgThres = cv2.erode(imgDial, kernel, iterations=1)
    return imgThres


def getContours(img, coord):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) # получаем контуры
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 5000:#рассматриваем только контуры с площадью больше 5000
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)# находим координаты прямоугольника вокруг контура
            x, y, w, h = cv2.boundingRect(approx)
            coords.append([x, y, w, h])
            flag = 0
            for i in range(4):
                if abs(coord[1][i] - coord[0][i]) < 3:# проверяем изменение координатов контура, чтобы не выделять объекты в движении
                    flag += 1
            if flag == 4:#если все 4 координаты неизмены обводим предмет как забытый
                cv2.rectangle(imgCopy, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(imgCopy, 'Забытый предмет',
                            (x + (w // 2) - 60, y + (h // 2) - 10), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                            (255, 255, 255), 1)
            coord.pop(0)  # заменяем сравниваемый кадр на текущий
    return coords

for i in range(1, 5):#проходимся по всем 4 роликам
    cap = cv2.VideoCapture('Resources/video{}.mp4'.format(i))
    writer = cv2.VideoWriter('result{}.mp4'.format(i), cv2.VideoWriter_fourcc(*'DIVX'), 10, (int(cap.get(3)), int(cap.get(4))))
    # записываем результат в виде видео result.mp4
    ret, FirstFrame = cap.read()  # запоминаем 1 кадр
    coords = [[0, 0, 0, 0]]
    while True:
        success, img = cap.read()  # считываем текущий кадр
        if success:
            imgCopy = img.copy()  # создаём копию неизменённого кадра для вывода результата
            img = cv2.subtract(FirstFrame, img)  # вычитаем из 1 кадра текущий, чтобы сравнить их
            imgThres = preProcessing(img)  # подготавливаем изображение для поиска контуртов
            coord = getContours(imgThres, coords)  # находим контуры
            writer.write(imgCopy)  # запись в файл
            cv2.imshow('Video', imgCopy)  # вывод на экран
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            cap.set(1, cap.get(1) + 5)  # просматриваем каждый 5 кадр чтобы лучше отслеживать движение
        else:
            break
