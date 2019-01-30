import sys
import cv2          #Install OpenCV
import numpy as np  #Install NumPy

from PIL import Image
from PIL import ImageDraw
from collections import deque
choice = 3
cap1 = cv2.VideoCapture("1.mp4")
cap2 = cv2.VideoCapture("2.mp4")
print(type(cap1))
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter("3.avi", fourcc , 30, (640, 480),1)
queue = deque([])
queue1 = deque([])
i = 0
BLUE = [0,0,0]
j = 0
k = 0
r = 640
l = 0
c = 480
axi = 0
al = 1
pipr = 0
pipc = 0
w=0
h=0

def choice3():
     k = 0
     r = 0
     c = 0
     
     if k < 15:
         k = k + 1
         r = int(r + 576/15)
         c = int(c + 432/15)
         nframe = cv2.resize(frame,(r,c))
         constant= cv2.copyMakeBorder(nframe,int((480-c)/2),int((480-c)/2),int((640-r)/2),int((640-r)/2),cv2.BORDER_CONSTANT,value=BLUE)
         cv2.imshow('fr',constant)
         print("1")
         out.write(constant)
         print(k)
     else:
         out.write(frame)


while True:
     ret, frame = cap1.read()
     if frame is None:
        break
     queue.append(frame)
     if i >= 30:
         out.write(queue.popleft())
     if cv2.waitKey(1) & 0xFF == ord('q'):
          break
     i = i + 1
cap1.release()
      
while True:
    ret, frame = cap2.read()

    if frame is None:
        break
    if choice == 2:
        while j < 30:
            out.write(queue.popleft())
            j = j + 1
        out.write(frame)
    elif choice == 1:
        if j < 30:
            j = j + 1
            print("here")
            image = queue.popleft()
#                    print(type(image))
#            cv2.imshow('im' ,image)
            newframe1 = image * al + frame * (1 - al)
#            cv2.imshow('new', newframe)
#                    print(type(newframe))
            newframe = newframe1.astype('uint8')
            al = al - (1/30)
            out.write(newframe)
#                    del newframe
#                    print(al)
        else:
            out.write(frame)
     
    elif choice == 3:
        while l < 15:
             l = l + 1
             image = queue.popleft()
             out.write(image)
        while j < 15:
            j = j + 1
            image = queue.popleft()
            r = int(r - 576/15)
            c = int(c - 432/15)
            nframe = cv2.resize(image,(r,c))
            constant= cv2.copyMakeBorder(nframe,int((480-c)/2),int((480-c)/2),int((640-r)/2),int((640-r)/2),cv2.BORDER_CONSTANT,value=BLUE)
            out.write(constant)
        choice3()



    elif choice == 4:
          if j < 30:
               j = j + 1
               image = queue.popleft()
               w = w + 480/30
               h = h + 640/30
               nframe = cv2.resize(frame,(int(h),int(w)))
               image[0:int(w),0:int(h)] = nframe
               out.write(image)
          else:
               out.write(frame)
               
      
    if cv2.waitKey(1) & 0xFF == ord('q'):
         break
print(len(queue))
cap2.release()
out.release()
cv2.destroyAllWindows()
