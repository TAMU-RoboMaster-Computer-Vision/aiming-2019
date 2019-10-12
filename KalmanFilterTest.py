import win32api
import numpy as np
import cv2

bg_image = cv2.imread('bg.png')  # 500,1000
cv2.imshow('KalmanFilterDemo', bg_image)
cv2.moveWindow("KalmanFilterDemo", 0, 0)
window_ul = (8, 30)  # x,y
boxhsize = (20, 10)
while True:
    frame = bg_image.copy()
    x, y = win32api.GetCursorPos()
    x = x - window_ul[0]
    y = y - window_ul[1]
    cv2.rectangle(frame, (x - boxhsize[0], y - boxhsize[1]), (x + boxhsize[0], y + boxhsize[1]), (0, 255, 0), 3)

    xp, yp = predict(x, y)
    cv2.rectangle(frame, (xp - boxhsize[0], y - boxhsize[1]), (x + boxhsize[0], y + boxhsize[1]), (255, 0, 0), 1)
    cv2.imshow('KalmanFilterDemo', frame)
    print(x, ' ', y)
    k = cv2.waitKey(1) & 0xff
    if k == 27: break
