"""
url1:http://blog.jobbole.com/all-posts/
url2:http://blog.jobbole.com/all-posts/page/2/


"""
##多线程
import requests,re
from concurrent.futures import ThreadPoolExecutor
from lxml import etree



class Bole_job(object):
    def __init__(self):
        pass

    def send_request(self, url):
        full_url = url
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
        }
        respones = requests.get(url=full_url, headers=headers)
        # print(respones.text)
        return respones.text

    def page_get(self):
        pool = ThreadPoolExecutor(10)
        for page in range(0, 566):
            url = 'http://blog.jobbole.com/all-posts/page/%s/' % (page)
            result = pool.submit(self.send_request, url)
            result.add_done_callback(self.get_data)
        pool.shutdown()
    def get_data(self, future):
        html = future.result()

        if html :
            get_html  = etree.HTML(html)
            new_url = get_html.xpath('//a[@class="archive-title"]/@href')
            pool = ThreadPoolExecutor(10)
            for all_url in new_url:
                result = pool.submit(self.send_request,all_url)
                result.add_done_callback(self.archive_data)

    def archive_data(self,future):
        result = future.result()
        if result:
            html = etree.HTML(result)
            # re.match('')
            list_job={}

            list_job['title'] = html.xpath('//div[@class="breadcrumb-wrapper"]/text()')[4].replace('>','').replace(' ','')
            list_job['time'] = html.xpath('//div[@class="entry-meta"]/p/text()')[0].replace('\r','').replace(' ','').replace('\n','')
            list_job['type'] = html.xpath('//p[@class="entry-meta-hide-on-mobile"]/a[1]/text()')[0]+html.xpath('//p[@class="entry-meta-hide-on-mobile"]/a[2]/text()')[0]
            print(list_job)
if __name__ == '__main__':
    bole = Bole_job()
    bole.page_get()
