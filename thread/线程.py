import queue, threading, requests
from lxml import etree


ID = 1
def crawl_task(task_queue, data_queue):
    print(threading.current_thread().name, '正在爬取', )

    while not task_queue.empty():
        page = task_queue.put
    full_url = 'https://www.readnovel.com/all?pageSize=10&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=' + str(page)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'

    }
    respons = requests.get(url=full_url, headers=headers)
    if respons.status_code == 200:
        data_queue(respons.text)
        print(page, '数据请请求成功')


def parse_task(data_queue):
    global ID
    while not data_queue.empty():
        text = data_queue.get()
        # print(threading.current_thread().name, '正在解析', len(text))
        html_text = etree.HTML(text)
        data_text = html_text.xpath('//div[@class="right-book-list"]/ul/li')
        for list_text in data_text:
            list_Book = {}

            list_Book['book_id'] = ID
            list_Book['book_Name'] = List_of_convenience(list_text.xpath('./div[2]/h3/a/text()'))
            list_Book['book_Author'] = List_of_convenience(list_text.xpath('./div[2]/h4/a/text()'))
            list_Book['book_type'] = List_of_convenience(list_text.xpath('./div[2]/p[1]/span[1]/text()'))
            list_Book['book_course'] = List_of_convenience(list_text.xpath('./div[2]/p[1]/span[2]/text()'))
            list_Book['book_words'] = List_of_convenience(list_text.xpath('./div[2]/p[1]/span[3]/text()'))
            list_Book['book_url'] = 'https:' + self.List_of_convenience(list_text.xpath('./div[1]/a/img/@src'))
            section_url = self.Root_url + List_of_convenience(
                list_text.xpath('./div[1]/a/@href')) + '#Catalog'
            list_Book['books_desc'] = section_url
            list_Book['book_intro '] = List_of_convenience(list_text.xpath('./div[2]/p[2]/text()'))
            ID += 1




def List_of_convenience(self, content=''):
    credits = content
    if credits:
        srt_credits = ''.join(credits).replace(' ', '').replace('\n', '').replace('\r', '').replace('\u3000', '')
        return srt_credits
    else:
        credits = 0
        return credits

if __name__ == '__main__':
    # 创建任务队列
    task_queue = queue.Queue()
    # 创建数据队列
    data_queue = queue.Queue()
    # 给任务队列中添加任务
    for page in range(1, 11):
        task_queue.put(page)

    crawl_theads = []
    crawl_theadnames = ['crawl1号', 'crawl2号', 'crawl3号', 'crawl4号']
    for name in crawl_theadnames:
        crawl_thead = threading.Thread(
            target=crawl_task, name=name, args=(task_queue, data_queue)
        )
        crawl_thead.start()
        crawl_theads.append(crawl_thead)
    for thread in crawl_theads:
        thread.join()

    parse_theads = []
    parse_theadnames = ['parse1号', 'parse2号', 'parse3号', 'parse4号']
    for name in crawl_theadnames:
        parse_thead = threading.Thread(
            target=parse_task,name=name,args=(data_queue,)

        )

        parse_thead.start()
