from Ui_adduser import Ui_Dialog
from PyQt5.QtWidgets import QDialog
from cameravideo import camera
from PyQt5.QtCore import QTimer
import cv2
import base64

class adduserwindow(Ui_Dialog,QDialog):
    def __init__(self, parent=None):
        super(adduserwindow,self).__init__(parent)
        self.setupUi(self)
        self.label.setScaledContents(True)
        self.cameravideo = camera()
        
        self.time = QTimer()
        self.time.timeout.connect(self.show_cameradata)
        self.time.start(50)
        self.pushButton.clicked.connect(self.get_cameradata)

    def show_cameradata(self):
        # print("ok")
        pic = self.cameravideo.camera_to_pic()
        #显示数据，显示画面
        self.label.setPixmap(pic) 

    def get_cameradata(self):
        camera_data = self.cameravideo.read_camera()
        _,enc = cv2.imencode('.jpg',camera_data)
        self.base64_image = base64.b64encode(enc.tobytes())
        print(self.base64_image)
        self.time.stop()
        self.cameravideo.close_camera()
        
