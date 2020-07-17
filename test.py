import base64
path = '1.jpg'
fp = open(path,'rb')
base64_image = base64.b64encode(fp.read())
print(base64_image)