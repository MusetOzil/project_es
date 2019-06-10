from selenium import webdriver
from selenium.common.exceptions import  NoSuchElementException
import queue,pymysql

from lxml import etree


class Douban(object):
    def __init__(self):
        self.dirver = webdriver.Chrome(
            executable_path="C:/Users/Mesut ozil/Desktop/new_moni/chromedriver.exe",

        )
        self.mysql_client = pymysql.Connect(
            user='root',password='123456',
             database='my_job',
            port=3306, charset='utf8'
        )
        self.cursor = self.mysql_client.cursor()

    def open_web(self, keyword):
        self.dirver.get('https://movie.douban.com/')
        # time.sleep(3)
        self.dirver.find_element_by_id('inp-query').send_keys(keyword)
        self.dirver.find_element_by_css_selector('.inp-btn').click()
        self.Decomposition_data()

    def Decomposition_data(self, ):
        result = self.dirver.page_source
        html_data = etree.HTML(result)

        new_html = html_data.xpath('//div[@class="item-root"]')
        for one in new_html:
            list_job = {}
            list_job['title'] = one.xpath('.//a[@class="title-text"]/text()')[0].replace('\u200e', '')
            rating_nums = one.xpath('.//span[@class="rating_nums"]/text()')
            if len(rating_nums) > 0:
                rating_nums = rating_nums[0]
            else:
                rating_nums = 0.0
            list_job['grade'] = rating_nums
            list_job['cover'] = one.xpath('.//a[@class="cover-link"]/img[@class="cover"]/@src')[0]

            particulars = one.xpath('.//div[@class="detail"]/div[@class="meta abstract"]/text()')
            list_job['particulars'] = self.List_of_convenience(particulars)
            billing = one.xpath('.//div[@class="detail"]/div[@class="meta abstract_2"]/text()')
            list_job['Billing'] = self.List_of_convenience(billing)
            print(list_job)
            self.save_mysql(list_job)
        self.dirver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        try:
            next_html = self.dirver.find_element_by_xpath('//a[@class="next"]')
            isnext = True
        except NoSuchElementException as err:
            isnext = False
        print('正在获取下一页')
        if isnext:
            print('下一页存在，正在获取')
            self.dirver.find_element_by_xpath('//a[@class="next"]').click()
            self.Decomposition_data()
        else:
            print('没有下一页了', key_queue.empty())
            if not key_queue.empty():
                self.open_web(key_queue.get())
            else:
                print('数据获取完毕，退出浏览器')
                self.dirver.quit()

    def List_of_convenience(self, content=''):
        credits = content
        srt_credits = ''.join(credits).replace(' ', '')
        return srt_credits
    def save_mysql(self,list_job):
        insert_sql = """
                        INSERT INTO job_douban(%s)
                        VALUES (%s)
                        """ % (
            ','.join(list_job.keys()),
            ','.join(['%s'] * len(list_job))
        )

        try:
            self.cursor.execute(insert_sql, list(list_job.values()))
            self.mysql_client.commit()
        except Exception as err:
            print(err)
            self.mysql_client.rollback()

if __name__ == '__main__':
    keyword_str = input('请输入搜索关键字（关键字之间用,号隔开）：')
    keyword = keyword_str.split(',')
    key_queue = queue.Queue()
    for i in keyword:
        key_queue.put(i)
    douban = Douban()
    douban.open_web(key_queue.get())
