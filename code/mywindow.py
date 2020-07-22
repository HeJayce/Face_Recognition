# encoding:utf-8
from Ui_Mainwindows import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow,QApplication,QFileDialog,QMessageBox,QInputDialog
import sys
import cv2
from PyQt5.QtGui import QPixmap,QImage
from PyQt5.QtCore import QTimer,QDateTime,QDate,QTime,QThread,pyqtSignal,QDir
from cameravideo import camera
import requests,json
import base64
from detect import detect_thread
from adduserwindow import adduserwindow
from data_show import sign_data

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
    detect_data_signal = pyqtSignal(bytes)
    camera_status = False
    #存放签到数据
    sign_list = {}

    def __init__(self):         #初始化函数
        super(mywindow,self).__init__()
        self.setupUi(self)   #创建界面内容
        self.label_11.setScaledContents(True)
        self.label_11.setPixmap(QPixmap("./1.jpg"))
    
        self.plainTextEdit_2.clear()
        
        self.datetime = QTimer(self)
        self.datetime.start(500)
        self.get_accesstoken()
        #信号与槽的关联
        #self.actionopen：指定对象
        #triggered 信号
        #connect ：关联（槽函数）
        #self.on_actionopen  关联的函数
        self.actionopen.triggered.connect(self.on_actionopen)
        self.actionclose.triggered.connect(self.on_actionclose)

        self.actionadd.triggered.connect(self.add_group)
        self.actiondel.triggered.connect(self.del_group)
        self.actiongetlist.triggered.connect(self.getgrouplist)
        self.actionadduser.triggered.connect(self.adduser)
        self.actiondeluser.triggered.connect(self.deluser)

        #添加用户组信号槽
        # self.actionaddgroup.triggered.connect()
           
        self.datetime.timeout.connect(self.date_time)
        # self.pushButton.clicked.connect(self.get_face)
        # self.pushButton_2.clicked.connect(self.create_thread)

    #线程完成检测
    def create_thread(self):
        self.detectThread = detect_thread(self.access_token,self.sign_list)
        self.detectThread.start()
        # self.detect_data_signal.connect(self.detectThread.detect_face)

    def date_time(self):
        date = QDate.currentDate()
        self.label_9.setText(date.toString())

        time = QTime.currentTime()
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
        self.camera_status =True
        #启动定时器，进行定时，每隔多久进行一次获取摄像头数据进行显示
        self.timeshow = QTimer(self)
        self.timeshow.start(10)
        #创建窗口就应该完成令牌调用
 
        #50ms  定时器启动，每50ms就会产生一个信号timeout
        self.timeshow.timeout.connect(self.show_cameradata)

        self.create_thread()
        
        #当开启检测启动时，创建定时器，500ms， 用作检测
        self.facedetecttime = QTimer(self)
        self.facedetecttime.start(1000)
        self.facedetecttime.timeout.connect(self.get_cameradata)
        #关联一个窗口中的信号与创建的线程中的函数

        self.detect_data_signal.connect(self.detectThread.get_base64)
        self.detectThread.transmit_data.connect(self.get_detectdata)
        self.detectThread.seach_data.connect(self.get_search_data)

    def on_actionclose(self):
        self.facedetecttime.stop()
        self.camera_status = False
        self.facedetecttime.timeout.disconnect(self.get_cameradata)
        self.detect_data_signal.disconnect(self.detectThread.get_base64)
        self.detectThread.transmit_data.connect(self.get_detectdata)
        
        #关闭检测线程
        self.detectThread.OK = False

        self.detectThread.quit()
        self.detectThread.wait()

        # #关闭定时器
        self.timeshow.stop()
        self.timeshow.timeout.disconnect(self.show_cameradata)
        self.cameravideo.close_camera()
        
             
        
   
        #显示本次签到情况
        self.label_11.setPixmap(QPixmap("./1.jpg"))
        self.detectThread.sign_list
        self.signdata = sign_data(self.detectThread.sign_list,self)
        self.signdata.exec_()

        if self.timeshow.isActive() == False and self.facedetecttime.isActive() == False:
            self.label_11.setPixmap(QPixmap("./1.jpg"))
            self.plainTextEdit.clear()
            self.plainTextEdit_2.clear()
        else:
            print("关闭失败，存在部分关闭失败")



    def get_cameradata(self):
        camera_data = self.cameravideo.read_camera()
        _,enc = cv2.imencode('.jpg',camera_data)
        base64_image = base64.b64encode(enc.tobytes())
        self.detect_data_signal.emit(bytes(base64_image))

#是作为摄像头，获取数据，显示画面的功能
#只要能够不断重复调用这个两数，不断的从摄像头获收数据进行显示
#可以通过信号，信号关联当前函数，只要信号产生，函数就会被调用
#信号不断产生，可以通过定时器，定时实践达到就会产生信号

    def show_cameradata(self): 
        #获取摄像头数据，转换数据
        pic = self.cameravideo.camera_to_pic()
        #显示数据，显示画面
        self.label_11.setPixmap(pic)

    #获取网络请求的令牌
    def get_accesstoken(self):
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=gI2zuccf2cAuquXyOf8lWw3i&client_secret=zTBa0v0VUE7VpxfBLzbWXRyal9rI00yy'

        #发送网络请求
        #使用get函数发送网络清求，参数为网络清求的地址，执行时会产生返回结果，结果就是请求的结果
        response = requests.get(host)
        if response:
            data = response.json()
            self.access_token = data.get('access_token')

    def get_detectdata(self,data):
        if data['error_code'] != 0 :
            self.plainTextEdit_2.setPlainText(data['error_msg'])
            return

        elif data['error_msg']=='SUCCESS' :
            self.plainTextEdit_2.clear()
            #在data字典中健为'result'对应的值才是返回的检测结果
            face_num = data['result']['face_num']
            if face_num == 0:
                self.plainTextEdit_2.appendPlainText("当前没有人\n")
                return
            else:
                self.plainTextEdit_2.appendPlainText("当前有人\n")

            #人脸信息['result']['face_list'] ，是列表，每个数据就是一个人脸信息，需要取出每个列表
            #每个人脸信息字典data['result']['face_list'][0~i]
            for i in range(face_num):
                data['result']['face_list'][i]
                
            age = data['result']['face_list'][i]['age']
            beauty = data['result']['face_list'][i]['beauty']
            expression = data['result']['face_list'][i]['expression']['type']
            glasses = data['result']['face_list'][i]['glasses']['type']
            face_shape = data['result']['face_list'][i]['face_shape']['type']
            emotion = data['result']['face_list'][i]['emotion']['type']
            gender = data['result']['face_list'][i]['gender']['type']
            mask = data['result']['face_list'][i]['mask']['type']


            self. plainTextEdit_2.appendPlainText("学生人脸信息")
            self. plainTextEdit_2.appendPlainText("年龄:"+ str(age))
            self. plainTextEdit_2.appendPlainText("颜值分数:"+ str(beauty))
            self. plainTextEdit_2.appendPlainText("性别:"+ str(gender))
            self. plainTextEdit_2.appendPlainText("表情:"+ str(expression))
            self. plainTextEdit_2.appendPlainText("脸型:"+ str(face_shape))
            self. plainTextEdit_2.appendPlainText("是否带眼镜:"+ str(glasses))
            self. plainTextEdit_2.appendPlainText("情绪:"+ str(emotion))
            if mask == 0:
                mask = "否"
            else:
                mask = "是"
            self. plainTextEdit_2.appendPlainText("是否带口罩:"+ str(mask))

    def get_search_data(self,data):

        self.plainTextEdit.setPlainText(data)
 
    def add_group(self):
        group,ret = QInputDialog.getText(self,"添加用户组","请输入用户组（由字母、数字、下划线组成）")
        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/group/add"
        print(group)
        params = {
            "group_id":group
            }
        access_token = self.access_token
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/json'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            print (response.json())

    def del_group(self):
        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/group/delete"
        #删除需要知道存在哪些组
        list = self.get_list()
        group,ret = QInputDialog.getText(self,"存在的用户组","用户组信息\n"+str(list['result']['group_id_list']))
        
        params = {
            "group_id":group  #要删除的用户组id
            }
        access_token = self.access_token
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/json'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            data = response.json()
            if  data['error_code']== 0:
                print("success")

    def get_list(self):
        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/group/getlist"
        params = {"start":0,"length":100}
        access_token = self.access_token
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/json'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            return response.json()

    def getgrouplist(self):
        list =self.get_list()
        str = ''
        for i in list['result']['group_id_list']:
            str = str +'\n' + i
        QMessageBox.about(self,"用户组列表",str)

    def adduser(self):
        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/add"
        
        #创建一个窗口选择内容
        #请求参数中需要获取人脸，转换人脸编码，，添加组id，添加用户id，新用户id的信息
        if self.camera_status:
            QMessageBox.about(self,"摄像头状态","请关闭签到")
            return
        list = self.get_list()
        window = adduserwindow(list['result']['group_id_list'],self)
        # window = adduserwindow(self)
        #新创建的窗口，通过exec（）函数一直执行，阻塞执行，窗口不进行关闭，exec函数不会退出（才会结束）
        window_status = window.exec_()
        print(window_status)
        if window_status !=1:
            return 

        #判断是否点击确定

        params = {
            "image":window.base64_image,   #人脸图片
            "image_type":"BASE64",      #人脸的图片编码
            "group_id":window.group_id,      #组id
            "user_id":window.user_id,      #新用户id
            "user_info":"姓名" + window.msg_name +'\n'+"班级"+window.msg_class,      #用户信息
            }
        access_token = self.access_token
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/json'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            data = response.json()
            if data['error_code']==0:
                QMessageBox.information(self,"添加成功","信息已添加",QMessageBox.Yes)
            else :
                QMessageBox.information(self,"添加失败","信息未添加",QMessageBox.Yes)



    #删除用户中的一张人脸信息(face_token)

    def getuserlist(self,group):
        
            request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/group/getusers"

            params = {
                "group_id":group
            }
            access_token = self.access_token
            request_url = request_url + "?access_token=" + access_token
            headers = {'content-type': 'application/json'}
            response = requests.post(request_url, data=params, headers=headers)
            if response:
                return response.json()
                

        #获取用户人脸列表
    def user_face_list(self,group,user):
        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/face/getlist"

        params = {
            "user_id": user,
            "group_id": group
        }
        access_token = self.access_token
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/json'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            return response.json()
            #显示到界面中，要改为字符串
            # data = response.json
            # printstr((data['result']['face_list']))
           

            

    #删除用户中的一张人脸信息
    def del_face_token(self,group,user,facetoken):
        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/face/delete"

        params = {
            "user_id":user,
            "group_id":group,
            "face_token":facetoken

        }
        access_token = self.access_token
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/json'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            print(response.json())


    def deluser(self):
        #查询用户人脸信息（face_token）
        #获取用户组进行选择
        list = self.get_list()
        #print(list)
        group,ret=QInputDialog.getText(self,"用户组获取","用户组信息\n"+str(list['result']['group_id_list']))
        #获取用户，选择
        userlist=self.getuserlist(group)
        print(userlist)
        user, ret = QInputDialog.getText(self, "用户获取", "用户信息\n" + str(userlist['result']['user_id_list']))
        #print(user)
        #获取用户的人脸列表
        face_list=self.user_face_list(group,user)
        for i in face_list['result']['face_list']:
            self.del_face_token(group,user,i['face_token'])
 

#创建应用程序对象
app = QApplication(sys.argv)
#创建窗口
ui = mywindow()

ui.show()
#应用执行
app.exec_()

#退出
sys.exit(0)