from selenium import webdriver
from selenium.common.exceptions import TimeoutException,NoSuchElementException
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Douban(object):
    def __init__(self):
        self.dirver = webdriver.Chrome(
        executable_path="C:/Users/Mesut ozil/Desktop/new_moni/chromedriver.exe",

    )
    def open_web(self):
        self.dirver.get('https://movie.douban.com/')
        # time.sleep(3)
        self.dirver.find_element_by_id('inp-query').send_keys('Liam Neeson')
        self.dirver.find_element_by_css_selector('.inp-btn').click()
        self.Decomposition_data()
        self.dirver.page_source()

    def Decomposition_data(self):
        html = self.dirver.find_element_by_xpath('//div[@id="root"]/div[1]/div[2]/div[1]/div[1]')
        for one in html:
            list_job={}
            list_job['Billing'] = one.find_element_by_xpath('//div[@class="item-root"]/div[@class="detail"]/div[2]/span[1]/text()')+\
                                  one.find_element_by_xpath('//div[@class="item-root"]/div[@class="detail"]/div[2]/span[2]/text()')

            print(list_job)

if __name__ == '__main__':
    douban = Douban()
    douban.open_web()