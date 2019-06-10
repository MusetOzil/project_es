from selenium import webdriver
import time, pymysql,json


class Github(object):
    def __init__(self):
        self.driver = webdriver.Chrome(
            executable_path='C:/Users/Mesut ozil/Desktop/new_moni/chromedriver.exe'

        )
        self.mysql_client = pymysql.Connect(
            user='root',password='123456',
             database='my_job',
            port=3306, charset='utf8'
        )
        self.cursor = self.mysql_client.cursor()

    def Github_login(self, username, password):
        self.driver.get('https://github.com/login?return_to=%2Fjoin%3Fsource%3Dheader')
        time.sleep(5)
        self.driver.find_element_by_xpath('//input[@id="login_field"]').send_keys(username)

        self.driver.find_element_by_xpath('//input[@id="password"]').send_keys(password)


        self.driver.find_element_by_xpath(
            '//input[@class="btn btn-primary btn-block"]').click()
        cookie_obj = self.driver.get_cookies()
        cookies_dict = {cookie['name']: cookie['value'] for cookie in cookie_obj}
        cookies = json.dumps(cookies_dict,ensure_ascii=False)
        print(cookies)

        list_job = {}
        list_job['name'] = username
        list_job['password'] = password
        list_job['cookies'] = cookies
        # print(list_job)
        self.save_mysql(list_job)

        self.driver.quit()

    def save_mysql(self,list_job):

        insert_sql = """
                INSERT INTO job_github(%s)
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
    git = Github()
    git.Github_login('musetozil@163.com', 'saonianduiphone6')
