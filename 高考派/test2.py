from urllib import error, request, parse
import ssl, json, pymysql


class Getting_data(object):
    def __init__(self):
        #设置数据库连接
        self.client = pymysql.Connect(
            host='localhost',
            port=3306,
            database='list_job',
            user='root',
            password='123456',
            charset='utf8'
        )
        #创建游标
        self.cusor = self.client.cursor()
        #添加排行数据
        self.rank = 1


    def end_request(self, form=None, headers=None):
        #发起请求，获取数据
        form_data = parse.urlencode(form).encode('utf-8')
        if not headers:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'

            }
        url = 'http://www.gaokaopai.com/rank-index.html'
        req = request.Request(url=url, headers=headers, data=form_data)
        ssl_context = ssl._create_unverified_context()
        response = request.urlopen(req,context=ssl_context)
        html = response.read().decode('utf-8')
        is_next = self.Get_end(html)
        # is_next :判断是否有下一页 继续请求下一页
        if is_next:
            form['start'] = form['start'] + 25
            self.end_request(form=form)
        else:
            print('数据获取完毕')

    def Get_end(self, html):
        if '全部展示完了！！' in html:
            return False
        json_data = json.loads(html)
        list_list = json_data['data']['ranks']
        for job in list_list:
            job_list = {}
            job_list['id'] = self.rank
            job_list['category'] = self.rank
            job_list['name'] = job['uni_name']
            job_list['score'] = self.get_default_num(job['xiao_total'],isFloat=True)
            job_list['city'] = job['city_code']
            job_list['batch'] = job['batch_type']
            job_list['type'] = '本科一批'
            self.rank+=1
            # print(job_list)
            self.save_data_to_mysql(job_list)
        if len(list_list) > 0:
            return True
        elif len(list_list) == 0:
            return False

    def get_default_num(self, data=None, default=0, isFloat=False):
        if data:
            if isFloat:
                return float(data)
            else:
                return int(data)
        else:
            if isFloat:
                return float(default)
            else:
                return default
    def save_data_to_mysql(self, job_list):
        insert_sql = """
            INSERT INTO job_info(%s)
            VALUE (%s)
        """ % (
            ','.join(job_list.keys()),
            ','.join(['%s'] * len(job_list))
        )
        try:
            self.cusor.execute(insert_sql, list(job_list.values()))
            self.client.commit()
            print('插入成功')
        except Exception as err:
            self.client.rollback()
            print(err)




if __name__ == '__main__':
    data_set = Getting_data()
    form = {
        'otype': 2,
        'city': 0,
        'cate': 0,
        'batch_type': 0,
        'start': 1,
        'amount': 25,
    }

    data_set.end_request(form=form)





