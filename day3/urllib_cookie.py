# 获取cookie的第一种方式

from urllib import request

# url = 'https://www.kuaidaili.com/usercenter/'
# headers = {
#     'User - Agent': 'channelid=0; sid=1559056449345575; _ga=GA1.2.119970946.1559056451; _gid=GA1.2.830409303.1559056451; Hm_lvt_7ed65b1cc4b810e9fd37959c9bb51b31=1559056451; _gat=1; sessionid=9e642a252e2709213e17542974caf129; Hm_lpvt_7ed65b1cc4b810e9fd37959c9bb51b31=1559057264',
#
#     'Cookie': 'channelid=0; sid=1559056449345575; _ga=GA1.2.119970946.1559056451; _gid=GA1.2.830409303.1559056451; Hm_lvt_7ed65b1cc4b810e9fd37959c9bb51b31=1559056451; _gat=1; sessionid=9e642a252e2709213e17542974caf129; Hm_lpvt_7ed65b1cc4b810e9fd37959c9bb51b31=1559057264',
#
# }
# req = request.Request(url=url, headers=headers)
# response = request.urlopen(req)
# if response.status == 200:
#     html = response.read().decode('utf-8')
#     if '626026976@qq.com'in html:
#         print('模拟用户请求成功')


# ——————————发送请求自动登陆————————————

from http.cookiejar import CookieJar
from urllib import parse

cookie_jar = CookieJar()
cookie_heandler = request.HTTPCookieProcessor(cookie_jar)

# 自定义opener
opener = request.build_opener(cookie_heandler)

url = 'https://www.kuaidaili.com/login/'
handrs = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
}
# req = request.Request(url=url, headers=handrs)
# response = opener.open(req)
# print(response.status)
# print(cookie_jar)
# print({cookie.name: cookie.value for cookie in cookie_jar})
# ___________上半部分为了获取用户登陆所需要的cookies信息————————
#
form = {
    'next': '',
    'kf5_return_to': '',
    'username': '626026976@qq.com',
    'passwd': 'lrf123123',
}
from_data = parse.urlencode(form).encode('utf-8')
req = request.Request(url=url, data=from_data, headers=handrs)
res = opener.open(req)
if res.status == 200:
    html = res.read().decode('utf-8')
    # print(html)
    if '626026976@qq.com' in html:
        print('模拟用户请求成功')
        cookies = {cookie.name: cookie.value for cookie in cookie_jar}
        print(cookies)
