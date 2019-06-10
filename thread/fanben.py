# 线程池:我们只需要告诉这个池子,你需要创建截个线程
# 我们不需要管理这些线程,只要往线程池中添加任务,线程池
# 中的线程会自动做任务分配,线程池中的线程可以复用

from concurrent.futures import ThreadPoolExecutor
import threading, requests, pymysql
from lxml import etree


def crawl_task(page):
    print('执行线程', threading.current_thread().name)
    print(page)
    full_url = 'https://www.readnovel.com/all?pageSize=10&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=' + str(
        page)

    # 构建请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    }

    # 发送请求，获取响应结果
    response = requests.get(url=full_url, headers=headers)

    if response.status_code == 200:
        return response.text


def done(futures):
    # print(futures)
    # print('=========',futures.result())
    # 获取html页面源码
    text = futures.result()
    if text:
        # 使用xpath做数据解析
        html_element = etree.HTML(text)

        li_elements = html_element.xpath('//div[@class="right-book-list"]/ul/li')

        chpater_pool = ThreadPoolExecutor(max_workers=5)
        for li in li_elements:
            """获取每一本书籍的信息"""
            book = {}
            # 标题
            book['title'] = li.xpath('./div[@class="book-info"]/h3/a/text()')[0]
            # 详情地址
            book['detailhref'] = li.xpath('./div[@class="book-info"]/h3/a/@href')[0]
            # 作者
            book['author'] = li.xpath('.//a[@class="default"]/text()')[0]
            # 内容
            book['content'] = li.xpath('.//p[@class="intro"]/text()')[0].replace(' ', '').replace('\r', '')

            handler = chpater_pool.submit(chpater_task, book['detailhref'])
            handler.add_done_callback(chpater_done)
            # print('====',book)

            save_data_to_db(book)


def chpater_task(url):
    # 获取章节详情的页面源码
    response = ''

    return response.text


def chpater_done(futures):
    print(futures.result())


def save_data_to_db(book):
    insert_sql = """
    INSERT INTO  xsyd (%s)
    VALUES (%s)
    """ % (
        ','.join(book.keys()),
        ','.join(['%s'] * len(book))
    )

    lock.acquire()
    try:
        print(insert_sql, list(book.values()))
        cursor.execute(insert_sql, list(book.values()))
        mysql_client.commit()
        print('插入成功')
    except Exception as err:
        print(err)
        mysql_client.rollback()
    lock.release()


if __name__ == '__main__':

    # 数据库连接
    """
    host=None, user=None, password="",
    database=None, port=0,charset=''
    """
    mysql_client = pymysql.Connect(
        host='127.0.0.1', user='root',
        password='ljh1314', database='calss1811',
        port=3306, charset='utf8'
    )
    # 创建游标
    cursor = mysql_client.cursor()

    lock = threading.Lock()

    print('开启', threading.current_thread().name)
    # 创建线程池
    # max_workers:表示要创建线程的数量
    # 第一步
    thread_pool = ThreadPoolExecutor(max_workers=5)

    # 第二步
    for page in range(1, 11):
        #  往线程池中添加任务
        handler = thread_pool.submit(
            crawl_task, page
        )
        # 第三步 如果线程任务中有返回值添加回调函数
        handler.add_done_callback(done)
    # 第四步：子线程阻塞操作
    # thread_pool.shutdown(wait=True) #相当于为每个线程执行了join方法
    """
     if wait:
        for t in self._threads:
            t.join()
    """

    print('结束', threading.current_thread().name)



