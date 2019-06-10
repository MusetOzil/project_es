from selenium import webdriver
from lxml import etree
import time,pymysql

class Douyu(object):
    def __init__(self):
        # opt = webdriver.ChromeOptions()
        # opt.set_headless()

        self.driver = webdriver.Chrome(
            executable_path='C:/Users/Mesut ozil/Desktop/new_moni/chromedriver.exe',
            # options=opt
        )
        self.mysql_client = pymysql.Connect(
            user='root', password='123456',
            database='my_job',
            port=3306, charset='utf8'
        )
        self.cursor = self.mysql_client.cursor()
        self.driver.get('https://www.douyu.com/g_LOL')
        self.get_html()



    def get_html(self):

        self.driver.set_window_size(width=1920, height=1080)

        result = self.driver.page_source
        html_data = etree.HTML(result)
        get_html = html_data.xpath('//div[@class="layout-Module-container layout-Cover ListContent"]/ul/li')
        for one in get_html:
            list_job ={}
            list_job['cover']=one.xpath('.//div/a/div[1]//img/@src')[0]
            list_job['title']=one.xpath('.//div[@class="DyListCover-content"]/div[1]/h3/text()')[0]
            list_job['types']=one.xpath('.//div[@class="DyListCover-content"]/div[1]/span/text()')[0]
            list_job['anchor'] = one.xpath('.//div[@class="DyListCover-content"]/div[2]/h2/text()')[0]
            list_job['the_United_States'] = one.xpath('.//div[@class="DyListCover-content"]/div[2]/span/text()')[0]

            honor = one.xpath('./div[@class="DyListCover HeaderCell is-href"]/a[1]/div[@class="DyListCover-content"]/span/text()')
            honors= self.List_of_convenience(honor)
            if honors:
                honors = honors
            else:
                comment=one.xpath('./div[@class="DyListCover HeaderCell is-href"]/a[1]/div[@class="DyListCover-content"]/span//span/text()')
                honors = self.List_of_convenience(comment)
            list_job['honor'] = honors


            print(list_job)
            self.save_mysql(list_job)

        self.Next_html()
    def List_of_convenience(self, content=''):
        credits = content
        srt_credits = ''.join(credits).replace(' ', '')
        return srt_credits
    def Next_html(self):
        self.driver.implicitly_wait(5)
        self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        next_html = self.driver.find_element_by_class_name('dy-Pagination-next')

        print('正在获取下一页')

        if next_html:
            print('有下一页正在获取')
            next_html.click()
            self.get_html()
        else:
            print('没有下一页了，浏览器即将关闭')
            time.sleep(2)
            self.driver.quit()
    def save_mysql(self,list_job):
        insert_sql = """
                        INSERT INTO job_douyu(%s)
                        VALUES (%s)
                        """ % (
            ','.join(list_job.keys()),
            ','.join(['%s'] * len(list_job))
        )

        try:
            self.cursor.execute(insert_sql, list(list_job.values()))
            # self.mysql_client.commit()
        except Exception as err:
            print(err)
            self.mysql_client.rollback()





if __name__ == '__main__':
    douyu = Douyu()
    douyu.get_html()