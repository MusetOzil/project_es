from selenium import webdriver
import time, pymysql, queue
from lxml import etree
from selenium.webdriver import ActionChains


class Qcc(object):
    def __init__(self):
        # opt = webdriver.ChromeOptions()
        # opt.set_headless()

        self.driver = webdriver.Chrome(
            executable_path='C:/Users/Mesut ozil/Desktop/new_moni/chromedriver.exe'
            # , options=opt
        )
        self.mysql_client = pymysql.Connect(
            user='root', password='123456',
            database='my_job',
            port=3306, charset='utf8'
        )
        self.cursor = self.mysql_client.cursor()

    def search(self, company):
        self.driver.get('https://www.qichacha.com/')
        self.driver.find_element_by_xpath('//input[@class="index-searchkey form-control input-lg"]').send_keys(company)
        self.driver.find_element_by_css_selector('.input-group-btn').click()
        time.sleep(2)
        ac = self.driver.find_element_by_xpath('//table[@class="m_srchList"]/tbody/tr[@class="frtrt"]/td[3]/a')
        ActionChains(self.driver).move_to_element(ac).click(ac).perform()
        self.get_data()



    def get_data(self):
        results = self.driver.page_source
        result = results
        if result:
            html = etree.HTML(result)
            list_job = {}
            list_job['company_name'] = html.xpath('//div[@class="row title jk-tip"]/h1/text()')
            list_job['company_state'] = html.xpath('//div[@class="row tags"]/span[1]/text()')
            list_job['company_phone'] = html.xpath('//div[@class="dcontent"]/div[1]/span[1]/span[2]/span/a/text()')
            list_job['company_URl'] = html.xpath('//div[@class="dcontent"]/div[1]/span[3]/a/text()')
            list_job['company_Address'] = html.xpath('//div[@class="dcontent"]/div[2]/span[3]/a[1]/text()')
            list_job['company_jianjie'] = html.xpath('//div[@class="dcontent"]/div[3]/span[2]/text()')
            list_job['company_logo'] = html.xpath('//div[@class="imgkuang"]/img/@src')
            list_job['company_registered'] = html.xpath('//section[@id="Cominfo"]/table[2]/tbody/tr[1]/td[2]/text()')
            list_job['company_manage_state'] = html.xpath('//section[@id="Cominfo"]/table[2]/tbody/tr[2]/td[2]/text()')
            list_job['company_Social_code'] = html.xpath('//section[@id="Cominfo"]/table[2]/tbody/tr[3]/td[2]/text()')
            list_job['company_rigist_code'] = html.xpath('//section[@id="Cominfo"]/table[2]/tbody/tr[4]/td[2]/text()')
            list_job['company_type_enterprise'] = html.xpath('//section[@id="Cominfo"]/table[2]/tbody/tr[5]/td[2]/text()')
            list_job['company_date_approval'] = html.xpath('//section[@id="Cominfo"]/table[2]/tbody/tr[6]/td[2]/text()')
            list_job['company_place_origin'] = html.xpath('//section[@id="Cominfo"]/table[2]/tbody/tr[7]/td[2]/text()')
            list_job['company_rename'] = html.xpath('//section[@id="Cominfo"]/table[2]/tbody/tr[8]/td[2]//span/text()')
            list_job['company_scale'] = html.xpath('//section[@id="Cominfo"]/table[2]/tbody/tr[9]/td[2]/text()')
            list_job['company_assessment'] = html.xpath('//section[@id="Cominfo"]/table[2]/tbody/tr[1]/td[4]/text()')
            list_job['company_date_establishment'] = html.xpath('//section[@id="Cominfo"]/table[2]/tbody/tr[2]/td[4]/text()')
            list_job['company_taxpayer_code'] = html.xpath('//section[@id="Cominfo"]/table[2]/tbody/tr[3]/td[4]/text()')
            list_job['company_organization_code'] = html.xpath('//section[@id="Cominfo"]/table[2]/tbody/tr[4]/td[4]/text()')
            list_job['company_industry_involved'] = html.xpath('//section[@id="Cominfo"]/table[2]/tbody/tr[5]/td[4]/text()')
            list_job['company_registration_authority'] = html.xpath('//section[@id="Cominfo"]/table[2]/tbody/tr[6]/td[4]/text()')
            list_job['company_English_name'] = html.xpath('//section[@id="Cominfo"]/table[2]/tbody/tr[7]/td[4]/text()')
            list_job['company_Contributors_in'] = html.xpath('//section[@id="Cominfo"]/table[2]/tbody/tr[8]/td[4]/text()')
            list_job['company_business_term '] = html.xpath('//section[@id="Cominfo"]/table[2]/tbody/tr[9]/td[4]/text()')
            list_job['company_Business_address '] = html.xpath('//section[@id="Cominfo"]/table[2]/tbody/tr[10]/td[2]/text()')
            list_job['company_business_scope'] = html.xpath('//section[@id="Cominfo"]/table[2]/tbody/tr[11]/td[2]/text()')
            list_job['company_legal_person'] = html.xpath('//div[@class="bpen"]/a[1]/h2/text()')
            print(list_job)
            self.Next_page()

    def Next_page(self):
        if not key_queue.empty():
            self.search(key_queue.get())
        else:
            print('数据获取完毕，退出浏览器')
            self.driver.quit()

    def save_mysql(self,list_job):
        insert_sql = """
                        INSERT INTO job_Qcc(%s)
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
    f = open('qcc.txt', 'r')
    conent = f.readlines()
    key_queue = queue.Queue()
    for emp in conent:
        key_queue.put(emp)
    qcc = Qcc()
    qcc.search(key_queue.get())
