from mywindow import mywindow
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == '__main__':

    #创建应用程序对象
    app = QApplication(sys.argv)
    #创建窗口
    ui = mywindow()

    ui.show()
    #应用执行
    app.exec_()

    #退出
    sys.exit(0)