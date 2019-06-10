import requests, pymysql, re


class Get_xpath(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
        }
        self.Root_url = 'https://www.readnovel.com/'
        self.client = pymysql.Connect(
            user='root',
            password='123456', database='microblog_project',
            port=3306, charset='utf8'
        )
        # 创建游标
        self.cursor = self.client.cursor()
        # 创建id
        self.ID = 1

    def request_send_to(self, url, headers=None, params=None):
        if not headers:
            headers = self.headers

        reponse = requests.get(url=url, params=params, headers=headers)
        if reponse.status_code == 200:
            return reponse.text
        elif reponse.status_code == 400:
            print('该网页没有可用数据')
        else:
            print('获取完毕')

    def get_books_data(self, url, Num):

        full_url = url + str(Num)  # 拼接新的url 发请求
        html = self.request_send_to(full_url)
        if html:
            porren = re.compile('<div\sclass="book-img">.*?' +
                                'href="(.*?)".*?src="(.*?)"' +
                                '.*?<h3><a.*?>(.*?)</a>' +
                                '.*?<h4><a.*?>(.*?)</a>.*?' +
                                '<span.*?>(.*?)</span>' +
                                '<span.*?>(.*?)</span>' +
                                '<span.*?>(.*?)</span>' +
                                '.*?<p.*?>(.*?)</p>', re.S)
            results = re.findall(porren, html)

            # print(results)
            for res in results:
                list_Book = {}
                list_Book['book_id'] = self.ID
                list_Book['book_Name'] = self.List_of_convenience(res[2])
                list_Book['book_Author'] = self.List_of_convenience(res[3])
                list_Book['book_type'] = self.List_of_convenience(res[4])
                list_Book['book_course'] = self.List_of_convenience(res[5])
                list_Book['book_words'] = self.List_of_convenience(res[6])
                list_Book['book_url'] = 'https:' + self.List_of_convenience(res[1])
                section_url = self.Root_url + self.List_of_convenience(
                    res[0]) + '#Catalog'
                list_Book['books_desc'] = section_url
                list_Book['book_intro '] = self.List_of_convenience(res[7])
                self.ID += 1
                # print(list_Book)
                # 获取详情URL 发起请求
                # print(section_url)

                Details_of_data = self.request_send_to(url=section_url, headers=self.headers)
                self.get_Details_of_the_data(Details_of_data)
            # 获取下页数据
            Num += 1
            self.get_books_data(url, Num)

    # 将列表内容变成字符串
    def List_of_convenience(self, content=''):
        credits = content
        if credits:
            srt_credits = ''.join(credits).replace(' ', '').replace('\n', '').replace('\r', '').replace('\u3000', '')
            return srt_credits
        else:
            credits = 0
            return credits

    # 拿到详情的html再获取章节的url
    def get_Details_of_the_data(self, html):
        html_data = html
        # print(html_data)
        if html:
            porren = re.compile('<div\sclass="volume">.*?<div class="cover"></div>.*?' +
                                '<h3>.*?<span\sclass="free">' +
                                '.*?<ul\sclass="cf">.*?</ul></div>', re.S)

            result = re.findall(porren, html_data)
            print(result)
            # s_id = 0
            # for list_data in The_data:
            #     s_id += 1
            #     id = 0
            #     # 拿到内容区url
            #     list_data_son = list_data.xpath('./div[@class="volume"][1]/ul[@class="cf"]/li/a/@href')
            #     for list_new_url in list_data_son:
            #         new_url = 'https:' + list_new_url
            #         # 发起请求 获取章节内容信息
            #         new_html = self.request_send_to(new_url)
            #         get_html = etree.HTML(new_html)
            #         list_new_dict = {}
            #         id += 1
            #         list_new_dict['id'] = id
            #         list_new_dict['Name'] = get_html.xpath(
            #             '//div[@class="main-text-wrap"][1]/div[@class="text-head"]/h3/text()')[0]
            #         list_new_dict['num_words'] = \
            #             get_html.xpath(
            #                 '//div[@class="main-text-wrap"][1]/div[@class="text-head"]/div/div/i[1]/span/text()')[0] \
            #             + \
            #             get_html.xpath('//div[@class="main-text-wrap"][1]/div[@class="text-head"]/div/div/i[1]/text()')[
            #                 0]
            #         list_new_dict['date'] = get_html.xpath(
            #             '//div[@class="main-text-wrap"][1]/div[@class="text-head"]/div/div/i[2]/span/text()')[0]
            #         list_text = get_html.xpath(
            #             '//div[@class="main-text-wrap"][1]/div[2]/p/text()')
            #         content = self.List_of_convenience(list_text)
            #         list_new_dict['s_id'] = s_id
            #         list_new_dict['content'] = content
            #         self.save_data_to_two_mysql(list_new_dict)
            #         print(list_new_dict)
            #
            #         print(s_id)

    def save_data_to_mysql(self, list_Book):
        """插入数据"""
        insert_sql = """
            INSERT INTO books_job(%s)
            VALUES (%s)
            """ % (
            ','.join(list_Book.keys()),
            ','.join(['%s'] * len(list_Book)),
        )
        try:
            self.cursor.execute(insert_sql, list(list_Book.values()))
            # self.client.commit()
            print('插入成功')
        except Exception as err:
            self.client.rollback()
            print(err)

    def save_data_to_two_mysql(self, list_new_dict):
        """插入数据"""
        insert_sql = """
            INSERT INTO books_content(%s)
            VALUES (%s)
            """ % (
            ','.join(list_new_dict.keys()),
            ','.join(['%s'] * len(list_new_dict)),
        )
        try:
            self.cursor.execute(insert_sql, list(list_new_dict.values()))
            # self.client.commit()
            print('插入成功')
        except Exception as err:
            self.client.rollback()
            print(err)


if __name__ == '__main__':
    Num = 1
    beg_url = 'https://www.readnovel.com/all?pageSize=10&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum='
    get_xpath = Get_xpath()
    get_xpath.get_books_data(beg_url, Num)
