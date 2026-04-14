import requests
response = requests.get("https://img2.huashi6.com/images/resource/2020/10/05/8482h2764p0.jpg?imageMogr2/quality/100/interlace/1/thumbnail/2000x%3E")
print(response.content)   # 字节数据
 #怎么保存成图片
with open("8482h2764p0.jpg", "wb") as f:
     f.write(response.content)
