import requests
from lxml import etree
def send():
    respones=  requests.get(url='https://movie.douban.com/subject_search?search_text=Liam+Neeson&cat=1002',
                            headers ={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'})
    if respones.status_code ==200:
        print(respones.status_code)
        html=respones.text
        print(html)
        html_get = etree.HTML(html)
        data = html_get.xpath('//div[@id="root"]/div[1]/div[2]/div[1]/div[1]')
        print(data)
        print(type(data))
send()