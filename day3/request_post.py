import requests


"""
url :目标地址
data = None :表单数据，字典类型



"""

url = 'http://www.gaokaopai.com/rank-index.html'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
}
form = {
        'otype': 2,
        'city': 0,
        'cate': 0,
        'batch_type': 0,
        'start': 1,
        'amount': 25,
    }
response = requests.post(url=url,data=form,headers=headers)
text = response.text
# print(text)
data = response.json()
# print(data)
# print(type(data))
"""
response.text 返回解码后的字符串
respones.content 以字节形式（二进制）返回。
response.status_code　 响应状态码
response.request.headers　 请求的请求头
response.headers　 响应头
response.encoding = 'utf-8' 可以设置编码类型
response.encoding 获取当前的编码
response.json() 内置的JSON解码器，以json形式返回,前提返回的内容确保是json格式的，不然解析出错会抛异常
"""

url = 'https://httpbin.org/post'
files = {'file': open('image.png', 'rb')}
response = requests.post(url, files=files)
# print(response.text)


#___________________web认证
url = 'https://223.72.45.206:8000/'
auth = ('ljh','123456')
response =requests.get(url=url,auth = auth)
# print(response.text)

#______设置代理参数


