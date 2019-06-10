"""
https://tieba.baidu.com/f?kw=%E7%BE%8E%E5%A5%B3&ie=utf-8&pn=0&pagelets=frs-list%2Fpagelet%2Fthread&pagelets_stamp=1559111233322
https://tieba.baidu.com/f?kw=%E7%BE%8E%E5%A5%B3&ie=utf-8&pn=50&pagelets=frs-list%2Fpagelet%2Fthread&pagelets_stamp=1559111034364
https://tieba.baidu.com/f?kw=%E7%BE%8E%E5%A5%B3&ie=utf-8&pn=100&pagelets=frs-list%2Fpagelet%2Fthread&pagelets_stamp=1559111175125
"""

import requests,re


class Tieba_spider(object):
    def __init__(self):
        self.headres = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
        }

    def get_page_data(self, url):
        html = self.end_request(url)
        if html:
            with open('tiba.html', 'w') as file:
                file.write(html)

    def end_request(self, url=None, parmas=None, headres=None):
        if not headres:
            headres = self.headres
        response = requests.get(url=url, params=parmas, headers=headres)
        if response.status_code == 200:
            return response.text


if __name__ == '__main__':
    start_url = 'https://tieba.baidu.com/f?kw=%E7%BE%8E%E5%A5%B3&ie=utf-8&pn=0&pagelets=frs-list%2Fpagelet%2Fthread&pagelets_stamp=1559111233322'
    tiba = Tieba_spider()
    tiba.get_page_data(start_url)
