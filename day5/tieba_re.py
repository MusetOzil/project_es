
"""
分析网站

https://tieba.baidu.com/f?kw=%E7%BE%8E%E5%A5%B3
&ie=utf-8&pn=0
&pagelets=frs-list%2Fpagelet%2Fthread
&pagelets_stamp=1559111031299


https://tieba.baidu.com/f?kw=%E7%BE%8E%E5%A5%B3
&ie=utf-8&pn=0
&pagelets=frs-list%2Fpagelet%2Fthread
&pagelets_stamp=1559111240103

# https://tieba.baidu.com/f?kw=%E7%BE%8E%E5%A5%B3
# &ie=utf-8&pn=50
# &pagelets=frs-list%2Fpagelet%2Fthread
# &pagelets_stamp=1559111031299


https://tieba.baidu.com/f?kw=%E7%BE%8E%E5%A5%B3
&ie=utf-8&pn=100
&pagelets=frs-list%2Fpagelet%2Fthread
&pagelets_stamp=1559111124680
"""

import requests,re
from urllib import parse
from lxml import etree

class TiebaSpider(object):

    def __init__(self):
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
        }

    #获取帖子列表
    def get_page_data(self,url):

        html = self.send_request(url).replace('<!--','').replace('-->','')
        # print(html)
        #使用etree.html 构建一个xptah解析对象
        html_get = etree.HTML(html)
        get_element = html_get.xpath('//a[@class="j_th_tit "]')
        # print(get_element)
        for






        # post_lsit=





        # if html:
        #     # print(html)
        #     # with open('tieba.html','w') as file:
        #     #     file.write(html)
        #     print('解析列表数据，获取帖子详情的url地址')
        #     pattern = re.compile(
        #         '<div\sclass="threadlist_title pull_left j_th_tit ">'+
        #         '.*?<a.*?href="(.*?)"\stitle="(.*?)".*?>',
        #         re.S
        #     )
        #     articles = re.findall(pattern,html)
        #     # print(articles)
        #     for article in articles:
        #         # print(article)
        #         detail_url = article[0]
        #         #获取帖子详情完整的url地址
        #         detail_url = parse.urljoin(url,detail_url)
        #         title = article[1]
        #         print('正在发起',title,'帖子详情的请求')
        #         self.get_detail_data(detail_url)
        #
        #     #获取下一页
        #     if 'class="next pagination-item " >下一页' in html:
        #         #https://tieba.baidu.com/f?kw=%E7%BE%8E%E5%A5%B3&ie=utf-8&pn=0
        #         pattern = re.compile('pn=\d+')
        #         current_pn = int(re.search(pattern,url).group().replace('pn=',''))
        #         next_pn = current_pn + 50
        #         next_url = re.sub(pattern,'pn='+str(next_pn),url)
        #         self.get_page_data(next_url)

    #获取帖子详情
    def get_detail_data(self,url):
        """
        :param url: 贴子详情的url地址
        :return:
        """
        html = self.send_request(url)
        if html:
            print('帖子详情获取成功')
            # with open('detail.html','w') as file:
            #     file.write(html)
            pattern = re.compile(
                '<img\sclass="BDE_Image"'+
                '\ssrc="(.*?)".*?>',
                re.S
            )
            images = re.findall(pattern,html)
            print(images)
            for image in images:
                self.download_image(image)


    #根据图片的url地址下载图片
    def download_image(self,image_url):
        content = self.send_request(url=image_url,isImage=True)
        if content:
            #https://imgsa.baidu.com/forum/w%3D580/sign=131fda8234292df597c3ac1d8c335ce2/ca1b0ef41bd5ad6e5a357b478fcb39dbb7fd3c4a.jpg
            image_filename = image_url[-15:]
            with open('tiebaimage/'+image_filename,'wb') as file:
                file.write(content)


    #根据url地址发送请求
    def send_request(self,url,parmas=None,headers=None,isImage=False):
        """发送请求，返回页面html源码"""
        if not headers:
            headers = self.headers

        response = requests.get(url=url,params=parmas,headers=headers)

        if response.status_code == 200:
            if isImage:
                return response.content

            return response.text

if __name__ == '__main__':

    kw = input('请输入贴吧名称：')
    kw = parse.quote(kw)

    start_url = 'https://tieba.baidu.com/f?kw=%s&ie=utf-8&pn=0' % kw
    spider = TiebaSpider()
    spider.get_page_data(start_url)




