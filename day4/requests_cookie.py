import requests


def kuaidailiLogin():


    """
    next:
    kf5_return_to:
    username: 626026976@qq.com
    passwd: lrf123123
    :return:
    """
    url = 'https://www.kuaidaili.com/login/'
    form = {
        'next': '',
        'kf5_return_to': '',
        'username': '626026976@qq.com',
        'passwd': 'lrf123123',
    }
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',

    }
    response = requests.post(url=url, data=form, headers=headers,allow_redirects = False)

    res = response.status_code
    if res == 302:
        cookies = response.cookies

        print(cookies)
        print(type(cookies))
        cookies_dict = requests.utils.cookiejar_from_dict(cookies)
        print(cookies_dict)
