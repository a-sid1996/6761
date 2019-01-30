import sys
import cv2          #Install OpenCV
import numpy as np  #Install NumPy

from PIL import Image
from PIL import ImageDraw
from collections import deque

axis = 0
BLUE = [0,0,0]
cap1 = cv2.VideoCapture("3.avi")
cap2 = cv2.VideoCapture("2.mp4")
w = 0
h = 0
r = 0
vid = []
c = 0
# resize image 
ret1,frame1 = cap2.read()
while True:
    ret,frame = cap1.read()
    if frame is None:
        break
    vid.append(frame)
print(len(vid))
