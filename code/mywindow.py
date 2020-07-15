
from mainwindow import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow,QApplication
import sys
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

#创建应用程序对象
app = QApplication(sys.argv)
#创建窗口
ui = mywindow()

ui.show()
#应用执行
app.exec_()

#退出
sys.exit(0)