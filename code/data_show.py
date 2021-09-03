from  Ui_sign_indata  import Ui_Dialog
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QAbstractItemView, QFileDialog
class sign_data(Ui_Dialog,QDialog):
    def __init__(self,signdata,parent=None):
        super(sign_data,self).__init__(parent)
        self.setupUi(self) #创建界面内容
        #设置窗口的内容不能被修改
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        print(signdata.values())
        for i in signdata.values():
            info = i['user_info'].split('\n')
            info_name = info[0].split("名")
            info_id = info[1].split("级")
            rowcount=self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowcount)
            self.tableWidget.setItem(rowcount,0,QTableWidgetItem(info_name[1]))
            self.tableWidget.setItem(rowcount,1, QTableWidgetItem(info_id[1]))
            self.tableWidget.setItem(rowcount,2, QTableWidgetItem(i['datetime']))
        # self.pushButton.clicked.connect(self.save_data)
        # self.pushButton_2.clicked.connect()
        
    def save_data(self):
        filename,ret = QFileDialog.getSaveFileName(self,"导出数据",".","TXT(*.txt)")
        print(filename)
        self.accept()   #关闭对话框