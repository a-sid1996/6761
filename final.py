# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 23:35:38 2019

@author: yashas
"""

import sys
from collections import deque

import cv2          #Install OpenCV
import numpy as np  #Install NumPy
from PIL import Image     #Install PILLOW (PIL)
from PyQt5.QtCore import QTimer  #Install PyQt5
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi

class mainwindow(QMainWindow):
    
    vid1 = []
    vid2 = []
    x0 = 0
    x1 = 0
    x2 = 0
    l2 = 0


    def updateVid3(self):
        self.capture2 = cv2.VideoCapture('3.avi')
        self.vid3 = []
        while True:
            self.ret, self.image2 = self.capture2.read()
            if self.image2 is None:
                break
            self.vid3.append(self.image2)
        self.x2 = 0
        self.capture2 = None
        self.l2=len(self.vid3)
        #self.display2(self.vid3[0],1)
        window.update()

    
    def __init__(self):
        super(mainwindow, self).__init__()
        loadUi('main.ui', self)   #Load the GUI
        
        self.cap = cv2.VideoCapture(firstvid)
        self.cap1 = cv2.VideoCapture(secondvid)
        self.success, self.i0 = self.cap.read()
        self.a, self.i1 = self.cap1.read()
        
        while self.success:
            self.success, self.i0 = self.cap.read()
            self.vid1.append(self.i0)
        while self.a:
            self.a, self.i1 = self.cap1.read()
            self.vid2.append(self.i1)
    
        self.l0=len(self.vid1)
        self.l1=len(self.vid2)
        
        self.display(self.vid1[0], 1)        
        self.display1(self.vid2[0], 1) 
        self.display2(self.vid1[0], 1)
        self.stop1 = True
        self.stop2 = True
        self.stopc = True
        self.play1.clicked.connect(self.getVideo1)
        self.pause1.clicked.connect(self.pauseVideo1)
        self.play2.clicked.connect(self.getVideo2)
        self.pause2.clicked.connect(self.pauseVideo2)
        self.playc.clicked.connect(self.getVideo3)
        self.pausec.clicked.connect(self.pauseVideoC)
        self.convert.clicked.connect(self.convert1)
        self.fade.setChecked(True)

    def convert1(self):

        if self.fade.isChecked():
            choice = 1
        elif self.cut.isChecked():
            choice = 2
        elif self.wipe.isChecked():
            choice = 3
        elif self.scale.isChecked():
            choice = 4
        elif self.picInPic.isChecked():
            choice = 5
        cap1 = cv2.VideoCapture(firstvid)
        cap2 = cv2.VideoCapture(secondvid)
        fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        out = cv2.VideoWriter("3.avi", fourcc , 30, (640, 480),1)
        queue = deque([])
        i = 0
        j = 0
        k = 0
        l = 0
        h = 0
        w = 0
        r = 640
        c = 480
        al = 1
        axi = 0
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
            rows = 480
            cols = 640
            if frame is None:
                break

            if choice == 1:
                if j < 30:
                    j = j + 1
                    image = queue.popleft()
                    newframe1 = image * al + frame * (1 - al)
                    newframe = newframe1.astype('uint8')
                    al = al - (1/30)
                    out.write(newframe)
                else:
                    out.write(frame)


            elif choice == 2:
                while j < 30:
                    out.write(queue.popleft())
                    j = j + 1
                out.write(frame)
            

            elif choice == 3:
                if j < 30:
                    j = j + 1
                    image = queue.popleft()
                    vis = np.concatenate((image, frame), axis=1)
                    newframe = vis[0:480 , axi:640+axi]
                    axi = axi + round(640/30)
                    out.write(newframe)
                else:
                    out.write(frame)


            elif choice == 4:
                if len(queue) != 0:
                    while l < 15:
                        l = l + 1
                        image = queue.popleft()
                        out.write(image)
                    blank = np.zeros((480,640,3), np.uint8)
                    while j < 15:
                        j = j + 1
                        image = queue.popleft()
                        r = int(r - 576/15)
                        c = int(c - 432/15)
                        bx = int(blank.shape[0]/2)
                        by = int(blank.shape[1]/2)
                        nframe = cv2.resize(image,(r,c))
                        blank = np.zeros((480,640,3), np.uint8)
                        blank[bx - int(nframe.shape[0]/2):bx - int(nframe.shape[0]/2)+nframe.shape[0],by - int(nframe.shape[1]/2):by - int(nframe.shape[1]/2)+ nframe.shape[1]] = nframe
                        out.write(blank)
                else:
                    blank = np.zeros((480,640,3), np.uint8)
                    if k < 15:
                        k = k + 1
                        nframe = cv2.resize(frame,(r,c))
                        bx = int(blank.shape[0]/2)
                        by = int(blank.shape[1]/2)
                        blank[bx - int(nframe.shape[0]/2):bx - int(nframe.shape[0]/2)+nframe.shape[0],by - int(nframe.shape[1]/2):by - int(nframe.shape[1]/2)+ nframe.shape[1]] = nframe
                        r = int(r + 576/15)
                        c = int(c + 432/15)
                        out.write(blank)
                    else:
                        out.write(frame)

            elif choice == 5:
                    if j < 30:
                       j = j + 1
                       image = queue.popleft()
                       h = int(h + 480/30)
                       w = int(w + 640/30)
                       nframe = cv2.resize(frame,(int(w),int(h)))
                       image[0:nframe.shape[0],640 - w:640 - w+ nframe.shape[1]] = nframe
                       out.write(image)
                    else:
                       out.write(frame)

                        
            if cv2.waitKey(1) & 0xFF == ord('q'):
                 break
        cap2.release()
        cv2.destroyAllWindows()
        out.release()
        out = None
        self.updateVid3()
                        
    def getVideo1(self):                #Playing Video 1
        if self.stop1:
            self.timer0 = QTimer(self)       
            self.timer0.timeout.connect(self.update_frame)
            self.timer0.start(33.34)
            self.stop1 = False
    def getVideo2(self):                #Playing Video 2
        if self.stop2:
            self.timer1 = QTimer(self)
            self.timer1.timeout.connect(self.update_frame1)
            self.timer1.start(33.34)
            self.stop2 = False
    def getVideo3(self):                #Playing Converted Video  
        if self.stopc:  
            self.timer2 = QTimer(self)
            self.timer2.timeout.connect(self.update_frame2)
            self.timer2.start(33.34)
            self.stopc = False
    def pauseVideo1(self):
        self.timer0.stop()
        self.stop1 = True
    def pauseVideo2(self):
        self.timer1.stop()
        self.stop2 = True
    def pauseVideoC(self):
        self.timer2.stop()
        self.stopc = True
    
    
    def update_frame(self):
        if self.x0 < self.l0:
            self.display(self.vid1[self.x0], 1)   
            self.x0 += 1
        else:
            self.x0 = 0
    def update_frame1(self):
        if self.x1 < self.l1:
            self.display1(self.vid2[self.x1], 1)        
            self.x1 += 1
        else:
            self.x1 = 0
    def update_frame2(self):
        if self.x2 < self.l2:
            self.display2(self.vid3[self.x2], 1)
            self.x2 += 1
        else:
            self.x2 = 0
        
    def display(self, img, window = 1):
        qformat = QImage.Format_Indexed8
        qformat=QImage.Format_RGB888
        outImage=QImage(img, 640, 480, qformat)
        outImage = outImage.rgbSwapped()
        if window == 1:
            self.video1.setPixmap(QPixmap.fromImage(outImage))
            self.video1.setScaledContents(True)
    def display1(self, img, window = 1):
        qformat = QImage.Format_Indexed8
        qformat=QImage.Format_RGB888
        outImage=QImage(img, 640, 480, qformat)
        outImage = outImage.rgbSwapped()
        if window == 1:
            self.video2.setPixmap(QPixmap.fromImage(outImage))
            self.video2.setScaledContents(True)
    def display2(self, img, window = 1):
        qformat = QImage.Format_Indexed8
        qformat=QImage.Format_RGB888
        outImage=QImage(img, 640, 480, qformat)
        outImage = outImage.rgbSwapped()
        if window == 1:
            self.convertedVideo.setPixmap(QPixmap.fromImage(outImage))
            self.convertedVideo.setScaledContents(True)
        
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    print("Enter name of first video")
    firstvid = input()
    print("\n\n\n\nEnter name of second video")
    secondvid = input()
    window = mainwindow()
    window.setWindowTitle('Assignment1 SOEN6761')
    window.show()
#    sys.exit(app.exec_())
