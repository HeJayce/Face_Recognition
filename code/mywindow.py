# encoding:utf-8
from Ui_Mainwindows import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow,QApplication
import sys
from PyQt5.QtCore import QTimer,QDateTime,QDate,QTime
from cameravideo import camera
import requests
'''
子类，维承UI_MainWindow与QMainWindow
Ui_ MainWindow:
    包含是界面的设计，窗口中的窗口部件
QMainWindow:
    包含是整个界面窗口，窗口的操作
mywindow:
    完整的窗口类
'''
class mywindow(Ui_MainWindow,QMainWindow):
    def __init__(self):         #初始化函数
        super(mywindow,self).__init__()
        self.setupUi(self)   #创建界面内容
        self.datetime = QTimer(self)
        self.datetime.start(500)
        #信号与槽的关联
        #self.actionopen：指定对象
        #triggered 信号
        #connect ：关联（槽函数）
        #self.on_actionopen  关联的函数
        self.actionopen.triggered.connect(self.on_actionopen)
        self.actionclose.triggered.connect(self.on_actionclose)
        self.datetime.timeout.connect(self.date_time)
        self.pushButton_2.clicked.connect(self.get_accesstoken)

    def date_time(self):

        date = QDate.currentDate()
        self.dateEdit.setDate(date)
        self.label_9.setText(date.toString())

        time = QTime.currentTime()
        self.timeEdit.setTime(time)
        self.label_10.setText(time.toString())
        


    '''
    信号槽功能：
    当某个组件设计了信号槽功能时，当信号产生，会主动调用槽函数，去完成对应的操作
    信号：当以某种特定的操作，操作这个组件时，就会主动产生对应操作的信号
    '''

    def on_actionopen(self):
        #print("on_actionopen")
        #启动摄像头

        self.cameravideo = camera() 
        #启动定时器，进行定时，每隔多久进行一次获取摄像头数据进行显示
        self.timeshow = QTimer(self)
        self.timeshow.start(500)
        #50ms  定时器启动，每50ms就会产生一个信号timeout
        self.timeshow.timeout.connect(self.show_cameradata)


    def on_actionclose(self):
        self.cameravideo.close_camera()
        #关闭定时器
        self.timeshow.stop()

        self.label_11.setText(" ")
    

#是作为摄像头，获取数据，显示画面的功能
#只要能够不断重复调用这个两数，不断的从摄像头获收数据进行显示
#可以通过信号，信号关联当前函数，只要信号产生，函数就会被调用
#信号不断产生，可以通过定时器，定时实践达到就会产生信号

    def show_cameradata(self):
        #获取摄像头数据，转换数据
        pic = self.cameravideo.camera_to_pic()
        #显示数据，显示画面
        self.label_11.setPixmap(pic)



    def get_accesstoken(self):
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=gI2zuccf2cAuquXyOf8lWw3i&client_secret=zTBa0v0VUE7VpxfBLzbWXRyal9rI00yy'

        #发送网络请求
        #使用get函数发送网络清求，参数为网络清求的地址，执行时会产生返回结果，结果就是请求的结果
        response = requests.get(host)
        if response:
            data = response.json()
            self.access_token = data.get('access_token')
            print(data)
            


    def get_face():
        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
        #请求参数，是一个字典在字典中存储了，百度AI要识别的图片信息，要识别的属性内容
        params = {
            "image":"",  #图片信息字符串
            "image_type":"BASE64",  #图片信息的格式
            "face_field":"gender,age"}  #清求识别人脸的属性，各个属性在字符串中用，逗号隔开
        #访问令牌
        access_token = self.access_token
        #把请求地址和访问令牌组成可用的网络请求
        request_url = request_url + "?access_token=" + access_token
        #
        headers = {'content-type': 'application/json'}
        #
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            print (response.json())







            
#创建应用程序对象
app = QApplication(sys.argv)
#创建窗口
ui = mywindow()

ui.show()
#应用执行
app.exec_()

#退出
sys.exit(0)