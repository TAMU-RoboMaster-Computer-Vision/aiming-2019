import cv2
from serial import Serial
import time

tracker = cv2.TrackerMOSSE_create()
cam = cv2.VideoCapture(1)
if not cam.isOpened():
    print('Cannot open cam')
    exit()
port=Serial("/dev/ttyACM0",baudrate=115200,timeout=3.0)
ok, frame = cam.read()
bbox = cv2.selectROI(frame, False)
ok = tracker.init(frame, bbox)

frame_width=frame.shape[1]
frame_width_center=int(frame_width/2)
ignore_range_const=50
ignore_range=(frame_width_center-ignore_range_const,frame_width_center+ignore_range_const)
while True:
    ok, frame = cam.read()
    if not ok:
        break
    timer = cv2.getTickCount()
    ok, bbox = tracker.update(frame)
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
    command=3 #1:right 2:left 3:stop
    if ok:
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
        x_center=int(bbox[0]+bbox[2]/2)
        if x_center<ignore_range[0]:
            command=2
        elif x_center>ignore_range[1]:
            command=1
    else:
        cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
    cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2)
    cv2.putText(frame, "Mode : " + str(int(command)), (100,100), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2)
    cv2.imshow("Tracking", frame)
    port.write(command.encode())
    k = cv2.waitKey(1) & 0xff
    if k == 27 : break

