from Ui_userwindow import Ui_Dialog
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QTimer



class userwindow(Ui_Dialog,QDialog):
    def __init__(self,userlist,parent=None):
        super(userwindow,self).__init__(parent)
        self.setupUi(self)
        self.show_user(userlist)
        self.pushButton.clicked.connect(self.get_user)
        print(userlist)





    def show_user(self,userlist):
        for l in userlist :
            self.listWidget.addItem(l)

    def get_user(self):
        self.user = self.listWidget.currentItem().text()
        self.accept()
        