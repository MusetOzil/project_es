import requests
from lxml import etree

"""
url = 'https://www.qidian.com/all'
headers = 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
"""


class Get_Chinese_website(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
        }

    def The_page_content(self, url):
        html = self.request_to_send(url)
        # print(html)
        html_get = etree.HTML(html)
        get_element = html_get.xpath('//ul[@class="all-img-list cf"]/li')
        # get_element=
        print(get_element)
        for section in get_element:
            Article_lis = {}
            Article_lis['URL'] = section.xpath('./div[@class="book-img-box"]/a/@herf')
            Article_lis['imgUrl'] = section.xpath('./div[@class="book-img-box"]/a/img/@src')
            Article_lis['Name'] = section.xpath('./div[@class="book-mid-info"]//a/text()')[0]
            Article_lis['zuozhe'] = section.xpath('.//p[@class="author"]/a[1]/text()')[0]
            Article_lis['genre2'] = section.xpath('.//p[@class="author"]/a[2]/text()')[0] +'~'+section.xpath('//p[@class="author"]/a[3]/text()')[0]
            Article_lis['tai'] = section.xpath('.//p[@class="author"]/span/text()')[0]
            Article_lis['genre3'] = section.xpath('//p[@class="author"]/a[4]/text()')[0]
            Article_lis['explain'] = section.xpath('//div[@class="book-mid-info"]/p[@class="intro"]/text()')[0].replace('\r','').replace(' ','')


            print(Article_lis)

    def request_to_send(self, url, parmas=None, headers=None):
        '''发送请求 返回页面源码'''
        if not headers:
            headers = self.headers
        response = requests.get(url=url, params=parmas, headers=headers)
        if response.status_code == 200:
            print('请求成功')
            return response.text


if __name__ == '__main__':
    url = 'https://www.qidian.com/all'
    get_chanese = Get_Chinese_website()
    get_chanese.The_page_content(url)
