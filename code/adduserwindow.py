from Ui_adduser import Ui_Dialog
from PyQt5.QtWidgets import QDialog
from cameravideo import camera
from PyQt5.QtCore import QTimer
import cv2
import base64
import pymysql
import pandas as pd

from sqlalchemy import create_engine

# db = pymysql.connect(host='rm-bp1kkk2w6swi10b45ho.mysql.rds.aliyuncs.com', user='nbjbcy', password='NBchengyun12!@', port=3306) 
# cursor = db.cursor()
# data = cursor.execute("SELECT * FROM practice2.classes")
# data = list(cursor.fetchall())# 获取单条数据
# print(data)
# db.close()# 关闭数据库连接



class adduserwindow(Ui_Dialog,QDialog):

    def __init__(self,list,parent=None):
        super(adduserwindow,self).__init__(parent)
        self.setupUi(self)
        self.label.setScaledContents(True)
        self.cameravideo = camera()
        self.show_list(list)
        self.time = QTimer()
        self.time.timeout.connect(self.show_cameradata)
        self.time.start(50)
        self.pushButton.clicked.connect(self.get_cameradata)
        self.pushButton_2.clicked.connect(self.get_data_close)
        self.pushButton_3.clicked.connect(self.close_window)

        print(list)

    def show_list(self,list):
        for l in list :
            self.listWidget.addItem(l)




    def show_cameradata(self):
        # print("ok")
        pic = self.cameravideo.camera_to_pic()
        #显示数据，显示画面
        self.label.setPixmap(pic) 

    def get_cameradata(self):
        camera_data = self.cameravideo.read_camera()
        _,enc = cv2.imencode('.jpg',camera_data)
        self.base64_image = base64.b64encode(enc.tobytes())
        # print(self.base64_image)
        self.time.stop()
        self.cameravideo.close_camera()

        
    def get_data_close(self):
        self.group_id = self.listWidget.currentItem().text()
        self.user_id = self.lineEdit.text()
        self.msg_name = self.lineEdit_2.text()
        self.msg_class = self.lineEdit_3.text()
        print(type(self.msg_class))
        #关闭对话框
        self.accept()
        def sql_connect(host="rm-bp1kkk2w6swi10b45ho.mysql.rds.aliyuncs.com",port=3306,user='nbjbcy',passwd='',db='humaninfo',charset='utf8'):
            connect = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
            cur = connect.cursor()
            return connect,cur
        connect,cur = sql_connect()
        # df1 = "insert into info values (group_id, user_id, msg_name, msg_class)"
        cur.execute("INSERT INTO info(group_id, user_id, msg_name, msg_class) VALUES ('%s','%s','%s','%s');" %(self.group_id, self.user_id, self.msg_name, self.msg_class))
        conn.commit()



    def close_window(self):
        self.close()