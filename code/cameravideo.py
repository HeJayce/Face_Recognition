import cv2
import numpy as np
from PyQt5.QtGui import QPixmap,QImage




'''
摄像头操作：创建类对象完成摄像头的操作，把打开摄像头与创建类对象操作合并
    __init__函数完成摄像头的配置打开
'''

class camera():
    def __init__(self):
        #创建摄像头。对视频或摄像头进行读取操作
        #参数fliename 、device（视频设备号，0默认，123多个）
        self.capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        #isOpened()两数返回一个 布尔值，米为断是否摄像义初始化成小

        if self.capture.isOpened():
            print("is opened")
        self.currentframe = np.array([])       #创建多维数组


    def read_camera(self):
        ret,data = self.capture.read()
        if not ret :
            print("获取摄像头失败")
            return None
        return data 

    def camera_to_pic(self):
        pic = self.read_camera()
        #摄像头是BGR方式在站，首先需要转换为RGB
        #调icvtColor完成后才是RGB悠式的画面数据
        self.currentframe = cv2.cvtColor(pic,cv2.COLOR_BGR2RGB)
        #设置宽高
        #self.currentframe = cv2.cvtColor(self.currentframe,(640,480))

        #转换格式（界面能够显示的格式）
        #获取画面的宽度和高度
        height,width = self.currentframe.shape[:2]
        #先转换成QImage类型的图片（画面）,创建Qimage类对象，使用摄像头的画面数据
        #QIMAGE（data，width，height，format）创建：数据，宽度，高度
        qimg = QImage(self.currentframe,width,height,QImage.Format_RGB888)
        qpixmap = QPixmap.fromImage(qimg)
        return qpixmap

    def close_camera(self):
        self.capture.release()