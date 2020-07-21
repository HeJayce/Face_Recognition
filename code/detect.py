from PyQt5.QtCore import QThread,QTimer,pyqtSignal,QDir
import PyQt5.QtCore
import cv2 
import base64
import requests
#QThread,就是PyQt5提供的线程类
#由于是一个已经完成了的类，功能已经写好，线程关线程的功能需要我们自己完成
#需要自己完成需要的线程类，创建一个新的线程类（功能就可以自己定义），继承QThread，新写的类就是线程类

#线程进行执行只会执行线程类中的run函数，如果有新的函数需要实现，重新写一个run函数完成
class detect_thread(QThread): 
    transmit_data = pyqtSignal(dict)
    seach_data = pyqtSignal(str)
    OK = True
    def __init__(self,token):
        super(detect_thread,self).__init__()
        self.access_token = token
        self.condition = False



    #run函数执行结束，代表线程结束
    def run(self):
        print("run")
        # self.timer = QTimer
        # self.timer.start(1000)
        # self.timer.timeout.connect(self.detect_face)
        while self.OK:
            if self.condition:
                self.detect_face(self.base64_image)  
                self.condition = False

    def get_base64(self,base64_image):
        #当窗口产生信号，调用这个槽函数，就把传递的数据存放在线程变量中
        self.base64_image = base64_image
        self.condition =True





    def detect_face(self,base64_image):
       
        #这是打开对话框获取,获取画面
 
        # path,ret = QFileDialog.getOpenFileName(self,"open picture",".","图片格式(*.jpg)")
        # print(path)
        # #把图片转换为base64编码
        # fp = open(path,'rb')
        # base64_image = base64.b64encode(fp.read())
        '''
        摄像头获取画面
        '''
        # camera_data = self.cameravideo.read_camera()
        # #转换图片,设置编码为base64
        # _,enc = cv2.imencode('.jpg',camera_data)
        # base64_image = base64.b64encode(enc.tobytes())

        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
        #请求参数，是一个字典在字典中存储了，百度AI要识别的图片信息，要识别的属性内容
        params = {
            "image":base64_image,  #图片信息字符串
            "image_type":"BASE64",  #图片信息的格式
            "face_field":"gender,age,beauty,expression,face_shape,glasses,emotion,mask",
            "max_face_num":10
            }  #清求识别人脸的属性，各个属性在字符串中用，逗号隔开
        #访问令牌
        access_token = self.access_token
        #把请求地址和访问令牌组成可用的网络请求
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/json'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            data = response.json()
            #data 是请求的结果数据，需要进行解析，单独拿出来需要的数据内容，分开
            if data['result']['face_num'] >  0:
                
                self.transmit_data.emit(dict(data))
                self.face_search()
            else:
                self.transmit_data.emit(dict(data))
                self.seach_data.emit("")
            
    #人脸识别检测，一人
    def face_search(self):
        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/search"
        params = {
            "image":self.base64_image,
            "image_type":"BASE64",
            "group_id_list":"class1"                    #从那些组中进行人脸识别
        } 
        access_token = self.access_token
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/json'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            data = response.json()        
            if data['error_code'] == 0 :
                if data['result']['user_list'][0]['score'] > 90:
                    #print("人脸识别成功（签到成功）")
                    self.seach_data.emit("学生签到成功\n学生信息是:\n"+data['result']['user_list'][0]['user_info'])