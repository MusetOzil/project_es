import requests

url = 'https://www.baidu.com/s?wd=%E5%BF%AB%E5%B8%A6%E7%90%86'

response = requests.get(url=url)
print(response.status_code)
parmas = {
    'wd': '快代理'
}
response = requests.get(url=url, params=parmas)
print(response.status_code)

heanders = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
}

response = requests.get(url=url, params=parmas, headers=heanders)
code = response.status_code
print(code)
content = response.content
# print(content.decode('utf-8'))

# 直接获取去页面html文本

text = response.text
# print(text)
# 主义有时候会有乱码 这时最好用content

# 获取响应头
response_headers = response.headers
# print(response_headers)

# 获取url地址
c_url = response.url
# print(c_url)
# 如果返回是一个json字符串，可以使用response.json()
# 将json字符串转为Python数据类型等价json.loads()方法相同
# response.json()
