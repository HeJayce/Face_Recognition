from  Ui_sign_indata  import Ui_Dialog
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QAbstractItemView, QFileDialog
class sign_data(Ui_Dialog,QDialog):
    def __init__(self,signdata,parent=None):
        super(sign_data,self).__init__(parent)
        self.setupUi(self) #创建界面内容
        #设置窗口的内容不能被修改
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # #print(signdata.values())
        for i in signdata.values():
            info = i['user_info'].split('\n')
            rowcount=self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowcount)
            self.tableWidget.setItem(rowcount,0,QTableWidgetItem(info[0]))
            self.tableWidget.setItem(rowcount,1, QTableWidgetItem(info[1]))
            self.tableWidget.setItem(rowcount,2, QTableWidgetItem(i['datetime']))
        #     info[0]
        #     info[1]
        #     i['datetime']