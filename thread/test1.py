# import requests, threading, re,pymysql
# from lxml import etree
#
# """
# 'http://book.zongheng.com/store/c0/c0/b0/u0/p999/v9/s9/t0/u0/i1/ALL.html
# 'http://book.zongheng.com/store/c0/c0/b0/u0/p1/v9/s9/t0/u0/i1/ALL.html
# """
#
# from concurrent.futures import ThreadPoolExecutor
#
#
# class get_fiction_data(object):
#     def __init__(self):
#         self.client = pymysql.Connect(
#             user='root',
#             password='123456', database='list_job',
#             port=3306, charset='utf8'
#         )
#         # 创建游标
#         self.cursor = self.client.cursor()
#         # 创建id
#         self.lock = threading.Lock()
#
#     def get_data_page(self,page):
#         # print('执行线程', threading.current_thread().name)
#
#         full_url = 'http://book.zongheng.com/store/c0/c0/b0/u0/p' + str(page) + '/v9/s9/t0/u0/i1/ALL.html'
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
#         }
#         respone = requests.get(url=full_url, headers=headers)
#         if respone.status_code == 200:
#             return respone.text
#
#     def done(self, futures):
#         text = futures.result()
#         if text:
#             text_data = re.compile('<div\sclass="bookimg">.*?<a\shref="(.*?)".*?'+
#
#                                    '<img\ssrc="(.*?)".*?<div\sclass="bookinfo">'+
#                                    '.*?<div\sclass="bookname">.*?<a.*?>(.*?)</a>' +
#                                     '.*?<div\sclass="bookilnk">'+
#                                    '.*?<a.*?>(.*?)</a>' +
#                                    '.*?<a.*?>(.*?)</a>' +
#                                    '.*?<span>(.*?)</span>.*?' +
#                                    '.*?<span>(.*?)</span>' +
#                                    '.*?<div\sclass="bookintro">(.*?)' +
#                                    '</div>.*?<div\sclass="bookupdate">.*?<a.*?>(.*?)</a>',re.S
#                                    )
#             list_data = re.findall(text_data, text)
#             for list1_data in  list_data:
#                 list_get_data={}
#                 list_get_data['title'] = list1_data[2].replace(' ','').replace('\n','').replace('\t','').replace('\r','')
#                 list_get_data['imgurl'] = list1_data[1].replace(' ','').replace('\n','').replace('\t','').replace('\r','')
#                 list_get_data['details_url'] = list1_data[0].replace(' ','').replace('\n','').replace('\t','').replace('\r','')
#                 list_get_data['author'] = list1_data[3].replace(' ','').replace('\n','').replace('\t','').replace('\r','')
#                 list_get_data['type'] = list1_data[4].replace(' ','').replace('\n','').replace('\t','').replace('\r','')
#                 list_get_data['state'] = list1_data[5].replace(' ','').replace('\n','').replace('\t','').replace('\r','')
#                 list_get_data['date'] = list1_data[6].replace(' ','').replace('\n','').replace('\t','').replace('\r','')
#                 list_get_data['updata'] = list1_data[8].replace(' ','').replace('\n','').replace('\t','').replace('\r','')
#                 list_get_data['new_data'] = list1_data[7].replace(' ','').replace('\n','').replace('\t','').replace('\r','')
#                 self.save_data_to_mysql(list_get_data)
#     def save_data_to_mysql(self, list_get_data):
#         """插入数据"""
#         insert_sql = """
#             INSERT INTO books_job(%s)
#             VALUES (%s)
#             """ % (
#             ','.join(list_get_data.keys()),
#             ','.join(['%s'] * len(list_get_data)),
#         )
#         self.lock.acquire()
#         try:
#             self.cursor.execute(insert_sql, list(list_get_data.values()))
#             self.client.commit()
#             print('插入成功')
#         except Exception as err:
#             self.client.rollback()
#             print(err)
#         self.lock.release()
#
# if __name__ == '__main__':
#     get_data = get_fiction_data()
#     # 创建 线程数量
#     thread_pool = ThreadPoolExecutor(max_workers=30)
#
#     for page in range(1, 1000):
#         handler = thread_pool.submit(
#             get_data.get_data_page, page
#
#         )
#         handler.add_done_callback(get_data.done)
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def task(url):
    print(url)
    r1 = requests.get(
        url=url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'
        }
    )

    # 查看下载下来的文本信息
    soup = BeautifulSoup(r1.text, 'html.parser')
    print(soup.text)
    content_list = soup.find('div',attrs={'id':'content-list'})
    for item in content_list.find_all('div',attrs={'class':'item'}):
        title = item.find('a').text.strip()
        target_url = item.find('a').get('href')
        print(title,target_url)


def run():
    pool = ThreadPoolExecutor(5)
    for i in range(1, 50):
        pool.submit(task, 'https://dig.chouti.com/all/hot/recent/%s' % i)


if __name__ == '__main__':
    run()