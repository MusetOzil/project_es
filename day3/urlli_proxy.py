# handler处理器
# 自定义opener
from urllib import request

# 按照之前的方方式请求不了
url = 'http://httpbin.org/get'

proxies = {
    'http': '112. 85.171.40:9999',
    'https': '221.206.100.133:3473'
}
proxy_hendler = request.ProxyHandler(
    proxies=proxies
)
opener = request.build_opener(proxy_hendler)
# 使用自定义opener发送请求
response = opener.open(fullurl=url)
print(response.status)
# ----------------------------私密代理使用方法-------------------
# 代理服务器
proxy = "59.38.241.25:23916"

# 用户名和密码(私密代理/独享代理)
username = "myusername"
password = "mypassword"

headers = {"Accept-Encoding": "Gzip"}  # 使用gzip压缩传输数据让访问更快

proxy_values = "http://%(user)s:%(pwd)s@%(ip)s/" \
               % {'user': username, 'pwd': password, 'ip': proxy}

proxies = {"http": proxy_values, "https": proxy_values, }

handler = request.ProxyHandler(proxies)
opener = request.build_opener(handler)
req = request.Request(url=page_url, headers=headers)

result = opener.open(req)
