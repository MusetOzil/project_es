# 自定义一个类,可以设置任意京东商品url地址，获取该商品的全部评论信息，将评论信息数据分别保存至csv文件和mysql数据库，要求使用进程池来完成



from gevent import monkey, pool
monkey.patch_all()
import requests, re, json, gevent,pymysql

class jd_data(object):
    def __init__(self, url):
        self.url = url
        self.ID = re.search('\d+', self.url).group()
        self.client = pymysql.Connect(
            user='root',host='127.0.0.1',
            password='123456', database='project_pl',
            port=3306, charset='utf8'
        )
        # 创建游标
        self.cursor = self.client.cursor()

    def send_request(self, page=None):

        id = self.ID
        headesr = {
            'Referer': self.url,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
        }
        if not page:
            url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv1334&productId=%s&score=0&sortType=5&page=%s&pageSize=10&isShadowSku=0&fold=1' % (
                id, 0)
        else:
            url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv1334&productId=%s&score=0&sortType=5&page=%s&pageSize=10&isShadowSku=0&fold=1' % (
                id, page)

        print(url)
        print(page)
        respones = requests.get(url=url, headers=headesr)
        if respones.status_code == 200:
            html = respones.text
            self.storage_data(html)
            return html

    def get_data(self):
        html = self.send_request(page=None)
        if html:
            text = re.findall('.*?\((.*?)\);', html)[0].replace(')', '')
            json_data = json.loads(text)
            max_page = json_data['maxPage']

            for page in range(1, int(max_page) + 1):
                self.send_request(page=page)

    def storage_data(self, html):
        heml = html
        text = re.findall('.*?\((.*?)\);', heml)[0]
        json_data = json.loads(text)
        list_data = json_data['comments']
        for data in list_data:
            list_job = {}
            list_job['name'] = data['nickname']
            list_job['uptime'] = data['creationTime']
            list_job['content'] = data['content']
            self.save_mysql(list_job)
            # print(list_job)
    def save_mysql(self,list_job):
        """插入数据"""
        insert_sql = """
            INSERT INTO pi_job(%s)
            VALUES (%s)
            """ % (
            ','.join(list_job.keys()),
            ','.join(['%s'] * len(list_job)),
        )
        try:
            self.cursor.execute(insert_sql, list(list_job.values()))
            self.client.commit()
            print('插入成功')
        except Exception as err:
            self.client.rollback()
            print(err)

if __name__ == '__main__':
    jd = jd_data('https://item.jd.com/100001860773.html')
    pool = pool.Pool(8)
    gevent.joinall(
        [
            pool.spawn(jd.send_request),
            pool.spawn(jd.get_data),
            pool.spawn(jd.save_mysql)
        ]
    )
