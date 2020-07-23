from Ui_deluser import Ui_Dialog
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QTimer

class deluserwindow(Ui_Dialog,QDialog):
    def __init__(self,list,parent=None):
        super(deluserwindow,self).__init__(parent)
        self.setupUi(self)
        self.show_list(list)
        # group = self.group_id = self.listWidget.currentItem().text()
        # self.show_userlist(user_list,group)
        self.pushButton.clicked.connect(self.get_group)
        print(list)

    def show_list(self,list):
        for l in list :
            self.listWidget.addItem(l)

    # def show_userlist(self,user_list,group):
    #     for l in user_list :
    #         self.listWidget_2.addItem(l)


            
    def get_group(self):
        self.group = self.listWidget.currentItem().text()
        self.accept()
        
