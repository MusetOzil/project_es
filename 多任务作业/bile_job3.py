"""
url1:http://blog.jobbole.com/all-posts/
url2:http://blog.jobbole.com/all-posts/page/2/


"""
##协程
from gevent import monkey, pool
import gevent
monkey.patch_all()
import requests, re,time,random
from lxml import etree



class Bole_job(object):
    def __init__(self):
      pass


    def page_get(self):
        gevent_pool = pool.Pool(10)
        print('woxianlai')
        transfer = []
        for page in range(0, 20):
            new_url = 'http://blog.jobbole.com/all-posts/page/%s/' % (page)
            transfer.append(gevent_pool.spawn(self.send_request,url=new_url,isexit=False))
        pool.joinall(transfer)


    def get_data(self,html):
        result = html

        if result:
            get_html = etree.HTML(result)
            new_url = get_html.xpath('//a[@class="archive-title"]/@href')
            gevent_pool = pool.Pool(10)
            transport = []
            for all_url in new_url:
                transport.append(gevent_pool.spawn(self.send_request, full_url=all_url,isexit=True))
            pool.joinall(transport,timeout=10)

    def send_request(self, new_url,isexit=False):
        if isexit==False:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
            }
            respones = requests.get(url=new_url, headers=headers,)
            html= respones.text
            self.get_data(html)
        elif isexit==True:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
            }
            respones = requests.get(url=new_url, headers=headers,)
            html = respones.text
            self.archive_data(html)
        else:
            print('没有数据')

    def archive_data(self,html):
        result = html
        if result:
            html_data = etree.HTML(result)
            list_job = {}
            list_job['title'] = html_data.xpath('//div[@class="breadcrumb-wrapper"]/text()')[4].replace('>', '').replace(' ',
                                                                                                                    '')
            list_job['time'] = html_data.xpath('//div[@class="entry-meta"]/p/text()')[0].replace('\r', '').replace(' ',
                                                                                                              '').replace(
                '\n', '')
            list_job['type'] = html_data.xpath('//p[@class="entry-meta-hide-on-mobile"]/a[1]/text()')[0] + \
                               html_data.xpath('//p[@class="entry-meta-hide-on-mobile"]/a[2]/text()')[0]
            print(list_job)


if __name__ == '__main__':
    bole = Bole_job()
    bole.page_get()

