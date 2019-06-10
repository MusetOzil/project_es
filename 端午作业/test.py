from selenium import webdriver
from lxml import etree
import time

class DouYUSprid(object):
    def __init__(self):
        self.driver = webdriver.Chrome(
            executable_path='C:/Users/Mesut ozil/Desktop/new_moni/chromedriver.exe',
        )

    def cikie_button(self):
        self.driver.get('https://www.douyu.com/g_LOL')
        self.parse_get_data()

    def parse_get_data(self):
        html = self.driver.page_source
        element_html = etree.HTML(html)
        page_data = element_html.xpath('//ul[@class="layout-Cover-list"]/li')
        # print(len(page_data))
        for data in page_data:
            print('解析中')

            data_list = {}
            data_list['cover'] = data.xpath('.//div/a/div[1]//img/@src')[0]
            data_list['gametype'] = data.xpath('.//div/a/div[2]/div/span/text()')[0]
            data_list['title'] = data.xpath('.//div/a/div[2]//h3/text()')[0]
            data_list['popularity'] = data.xpath('.//div/a/div[2]/div/span/text()')[1]
            data_list['anchor'] = data.xpath('.//div/a/div[2]//h2/text()')[0]

            print(data_list)

            self.driver.implicitly_wait(2)
            self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            nextpage = self.driver.find_element_by_class_name('dy-Pagination-next')

            if nextpage:
                nextpage.click()
                self.parse_get_data()
            else:
                print('没有下一页了')
                self.driver.quit()

if __name__ == '__main__':
    spride = DouYUSprid()
    spride.cikie_button()
