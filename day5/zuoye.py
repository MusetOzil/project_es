"""
'Request URL: https://s.weibo.com/weibo/%25E6%2588%2590%25E9%2583%25BD%25E4%25B8%2583%25E4%25B8%25AD%25E9%25A3%259F%25E5%2593%2581?topnav=1&wvr=6&b=1'

'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'

"""
from lxml import etree
import requests, re, pymysql


class Food_safety(object):
    def __init__(self):
        self.headres = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
        }
        self.client = pymysql.Connect(
            user='root',
            password='123456', database='microblog_project',
            port=3306, charset='utf8'
        )
        # 创建游标
        self.cursor = self.client.cursor()
        #创建id
        self.ID = 1



    def Get_page_info(self, url):
        html = self.request_send_to(url)
        # print(html)
        get_html = etree.HTML(html)
        set_html = get_html.xpath('.//div[@class="m-con-l"]//div/div[@class="card-wrap"]')
        for every in set_html:
            list_every = {}

            list_every['id'] =self.ID
            #用户名

            list_every['username'] = every.xpath('.//div/div/div[@class="content"]/div/div[2]/a/text()')[0]
            #内容
            list_every['content'] = self.List_of_convenience(
                every.xpath('.//div/div/div[@class="content"]/p[@class="txt"][last()]/text()')) \
                                    + self.List_of_convenience(
                every.xpath('.//div/div/div[@class="content"]/p/em/text()'))
            from1 = every.xpath('.//div/div/div[@class="content"]/p[@class="from"]/a[1]/text()')
            from2 = every.xpath('.//div/div/div[@class="content"]/p[@class="from"]/text()')
            from3 = every.xpath('.//div/div/div[@class="content"]/p[@class="from"]/a[2]/text()')
            #来自
            list_every['froms'] = self.List_of_convenience(from1 + from2 + from3)
            collects = every.xpath('//div[@class="card-act"]/ul/li[1]/a/text()')[0]
            collect_fill = self.determine_the_data(collects)
            #收藏
            list_every['collect'] = collect_fill
            transmits = every.xpath('.//div[@class="card-act"]/ul/li[2]/a/text()')[0]
            transmit = self.determine_the_data(transmits)
            #转发
            list_every['transmit'] = transmit
            comments = every.xpath('.//div[@class="card-act"]/ul/li[3]/a/text()')[0]
            comment = self.determine_the_data(comments)
            #评论
            list_every['comment'] = comment
            praises = every.xpath('.//div[@class="card-act"]/ul/li[4]/a/em/text()')
            praise = self.determine_the_data(self.List_of_convenience(praises))
            #点赞
            list_every['praise'] = praise
            self.ID += 1
            print(list_every)
            # self.save_data_to_mysql(list_every)

    def save_data_to_mysql(self,list_every):
        """插入数据"""
        insert_sql = """
            INSERT INTO microblog_list(%s)
            VALUES (%s)
            """%(
                ','.join(list_every.keys()),
                ','.join(['%s']*len(list_every)),
        )
        try:
            self.cursor.execute(insert_sql,list(list_every.values()))
            self.client.commit()
            print('插入成功')
        except Exception as err:
            self.client.rollback()
            print(err)
    def List_of_convenience(self, content=''):
        credits = content
        srt_credits = ''.join(credits).replace(' ', '').replace('\n', '')
        return srt_credits

    def determine_the_data(self, collecs):
        nuner = collecs
        num = re.findall('\d+', nuner)
        if not num:
            num = 0
            return num
        else:
            return num[0]


    def request_send_to(self, url, headers=None, parmas=None):
        if not headers:
            headers = self.headres
        respones = requests.get(url=url, headers=headers, params=parmas)
        if respones.status_code == 200:
            print('washile ')

        return respones.text


if __name__ == '__main__':
    url = 'https://s.weibo.com/weibo/%25E6%2588%2590%25E9%2583%25BD%25E4%25B8%2583%25E4%25B8%25AD%25E9%25A3%259F%25E5%2593%2581?topnav=1&wvr=6&b=1'
    food = Food_safety()
    food.Get_page_info(url)
