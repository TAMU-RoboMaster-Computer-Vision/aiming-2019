import win32api
import numpy as np
from filterpy.common import kinematic_kf
from filterpy.kalman import ExtendedKalmanFilter
import cv2
import time
import filterpy as fp
from filterpy.kalman import IMMEstimator
np.set_printoptions(suppress=True)
order=1
kf1 = kinematic_kf(dim=2, order=order)
kf2 = ExtendedKalmanFilter(4, 2)
# do some settings of x, R, P etc. here, I'll just use the defaults
kf2.Q *= 0   # no prediction error in second filter
filters = [kf1, kf2]
mu = [0.5, 0.5]  # each filter is equally likely at the start
trans = np.array([[0.97, 0.03], [0.03, 0.97]])
imm = IMMEstimator(filters, mu, trans)

bg_image = cv2.imread('bg.png')  # 500,1000
cv2.imshow('KalmanFilterDemo', bg_image)
cv2.moveWindow("KalmanFilterDemo", 0, 0)
window_ul = (8, 30)  # x,y
boxhsize = (20, 10)
lastul=(0,0)
lastbr=(0,0)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
videof=cv2.VideoWriter('video.avi',fourcc,1,(1000,500))

while True:
    start_time = time.time() # start time of the loop
    frame = bg_image.copy()
    x, y = win32api.GetCursorPos()
    x = x - window_ul[0]
    y = y - window_ul[1]
    cv2.rectangle(frame, (x - boxhsize[0], y - boxhsize[1]), (x + boxhsize[0], y + boxhsize[1]), (0, 255, 0), 3)

    z = np.array([[x], [y]])
    imm.update(z)
    imm.predict()

    print(imm.x.T)
    # if order==1:
    #     xp=imm.x_prior[0]
    #     yp=imm.x_prior[2]
    # elif order==2:
    #     xp=imm.x_prior[0]
    #     yp=imm.x_prior[3]
    new_vals=imm.x.T[0]
    if order==1:
        xp=int(new_vals[0])
        yp=int(new_vals[2])
    elif order==2:
        xp=int(new_vals[0])
        yp=int(new_vals[3])
    for item in imm.x_prior:
        print(item[0],' ',end='')
    #cv2.rectangle(frame, lastul, lastbr, (255, 0, 0), 1)

    print()
    lastul=(xp - boxhsize[0], yp - boxhsize[1])
    lastbr=(xp + boxhsize[0], yp + boxhsize[1])
    cv2.rectangle(frame, (xp - boxhsize[0], yp - boxhsize[1]), (xp + boxhsize[0], yp + boxhsize[1]), (255, 0, 0), 1)
    cv2.imshow('KalmanFilterDemo', frame)
    videof.write(frame)
    #print(x, ' ', y)
    k = cv2.waitKey(100) & 0xff
    if k == 27: break
    print("FPS: ", 1.0 / (time.time() - start_time)) # FPS = 1 / time to process loop