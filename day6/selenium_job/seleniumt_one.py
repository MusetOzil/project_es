from selenium import webdriver
import time
from selenium.common.exceptions import TimeoutException


dirver = webdriver.Chrome(
    executable_path="C:/Users/Mesut ozil/Desktop/new_moni/chromedriver.exe",

)

dirver.get('https://www.douyu.com/directory/columnRoom/PCgame')
time.sleep(3)
dirver.save_screenshot('baidu.png')
dirver.execute_script('window.scrollTo(0,document.body.scrollHeight)')

dirver.find_element_by_class_name('dy-Pagination-item-custom').click()

