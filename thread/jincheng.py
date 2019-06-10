from concurrent.futures import ProcessPoolExecutor
import requests

def send_request(page):
    full_url = 'https://www.baidu.com/?page='+str(page)
    respones=requests.get(url=full_url)
    if respones.status_code==200:
        return respones.text

def done(futures):
    result = futures.result()
    print(len(result))


if __name__ == '__main__':
    process = ProcessPoolExecutor(max_workers = 4)
    for page in range(1,100):
        heade = process.submit(send_request,page)
        heade.add_done_callback(done)




# gevent能够在内部自己实现携程之间的切换

from gevent import monkey, pool
import gevent, requests
import lxml.etree as etree

# 有耗时操作时需要


