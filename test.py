import numpy as np
import cv2
import filterpy as fp
import win32api
def hx(x):
   return np.array([x[0]])

F = np.array([[1., 1.],
              [0., 1.]])
def fx(x, dt):
    return np.dot(F, x)

x = np.array([0., 1.])
P = np.eye(2) * 100.
dt = 0.1
f = EnKF(x=x, P=P, dim_z=2, dt=dt, N=8,
         hx=hx, fx=fx)

std_noise = 3.
f.R *= std_noise**2
f.Q = Q_discrete_white_noise(2, dt, .01)

bg_image=np.zeros((500, 1000))
while True:
    x, y = win32api.GetCursorPos()
    z = np.array([x,y])
    x,y=f.predict()
    f.update(np.asarray([z]))