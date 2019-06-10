from bs4 import BeautifulSoup
import requests

def send_request(url,parmas = None,headers=None):
    """ 发送请求时调用这个方法"""
    if not  headers :
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
        }
    respons=requests.get(url=url,params=parmas,headers=headers)
    if respons.status_code ==200:
        return respons.text
def get_data(url):
    html = send_request(url)
    if html:
        soup=BeautifulSoup(html,'lxml')

