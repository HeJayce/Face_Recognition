from Ui_Mainwindows import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow,QApplication
import sys
from PyQt5.QtCore import QTimer,QDateTime,QDate,QTime
from cameravideo import camera
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

        #信号与槽的关联
        #self.actionopen：指定对象
        #triggered 信号
        #connect ：关联（槽函数）
        #self.on_actionopen  关联的函数
        self.actionopen.triggered.connect(self.on_actionopen)
        self.actionclose.triggered.connect(self.on_actionclose)
        date = QDate.currentDate()
        print(date)
        self.dateEdit.setDate(date)

        time = QTime.currentTime()
        print(time)
        self.timeEdit.setTime(time)


    def show_time(self):

        date = QDate.currentDate()
        print(date)
        self.dateEdit.setDate(date)

        time = QTime.currentTime()
        print(time)
        self.timeEdit.setTime(time)



    '''
    信号槽功能：
    当某个组件设计了信号槽功能时，当信号产生，会主动调用槽函数，去完成对应的操作
    信号：当以某种特定的操作，操作这个组件时，就会主动产生对应操作的信号
    '''

    def on_actionopen(self):
        #print("on_actionopen")
        #启动摄像头
        time = QTime.currentTime()
        self.cameravideo = camera() 
        #启动定时器，进行定时，每隔多久进行一次获取摄像头数据进行显示
        self.timeshow = QTimer(self)
        self.timeshow.start(10)
        #50ms  定时器启动，每50ms就会产生一个信号timeout
        self.timeshow.timeout.connect(self.show_cameradata)
        self.timeshow.timeout.connect(self.show_time)

    def on_actionclose(self):
        self.cameravideo.close_camera()
        #关闭定时器
        self.timeshow.stop()
        self.label_3.setText("人脸显示区")
        self.label_6.setText(" ")
    

#是作为摄像头，获取数据，显示画面的功能
#只要能够不断重复调用这个两数，不断的从摄像头获收数据进行显示
#可以通过信号，信号关联当前函数，只要信号产生，函数就会被调用
#信号不断产生，可以通过定时器，定时实践达到就会产生信号

    def show_cameradata(self):
        #获取摄像头数据，转换数据
        pic = self.cameravideo.camera_to_pic()
        #显示数据，显示画面
        self.label_6.setPixmap(pic)








#创建应用程序对象
app = QApplication(sys.argv)
#创建窗口
ui = mywindow()

ui.show()
#应用执行
app.exec_()

#退出
sys.exit(0)