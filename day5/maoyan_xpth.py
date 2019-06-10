import re, requests, csv, json
from lxml import etree


class Cat_eye(object):
    def __init__(self):
        self.headres = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
        }

        self.file = open('test.csv', 'a+')
        self.fieldnames = ['ranking', 'picture_URL', 'Name', 'Billing', 'release_date', 'grade']
        self.writer = csv.DictWriter(self.file, fieldnames=self.fieldnames)
        self.writer.writeheader()

    def get_page_content(self, url):
        html = self.send_request(url)
        # if html:
        # 生产页面源码，使用正则匹配使用数据
        # porren = re.compile(
        #     '<i\sclass="board-index board-index-\d+">(.*?)</i>'
        #     '+.*?data-src="(.*?)".*?}"' +
        #     '>(.*?)</a>' +
        #     '.*?<p.*?>(.*?)</p>' +
        #     '.*?<p.*?>(.*?)</p>' +
        #     '.*?<i.*?>(.*?)</i>' +
        #     '.*?<i.*?>(.*?)</i>'
        #     , re.S
        # )
        # results = re.findall(porren, html)
        #
        # for res in results:
        #     list_job = {}
        #     # for res in result:
        #     list_job['ranking'] = res[0]
        #     list_job['picture_URL'] = res[1]
        #     list_job['Name'] = res[2]
        #     list_job['Billing'] = res[3].replace('\n', '')
        #     list_job['release_date'] = res[4]
        #     list_job['grade'] = res[5] + res[6]
        #     print(list_job)
        #     self.Save_file(list_job)
        #     self.Json_file(list_job)
        html_transform = etree.HTML
        all_dd = html_transform.xpath('//dl[@class="board=wrapper"]/dd')
        print(len(all_dd))
        print(all_dd)

        # if '下一页' in html:
        #     pattern = re.compile('offset=\d+')
        #     current_pn = int(re.search(pattern, url).group().replace('offset=', ''))
        #     next_pn = current_pn + 10
        #     next_url = re.sub(pattern, 'offset=' + str(next_pn), url)
        #     if next_url:
        #         self.get_page_content(next_url)

    def send_request(self, url, parmas=None, headres=None):
        # 发送请求的到页面源码
        if not headres:
            headres = self.headres
        response = requests.get(url=url, params=parmas, headers=headres)
        if response.status_code == 200:
            return response.text

    def Save_file(self, list_job):

        self.writer.writerow(list_job)

    def Json_file(self, list_job):
        wenjian = json.dumps(list_job, ensure_ascii=False)
        with open('test.json', 'a+', encoding='utf-8') as file:
            file.write(wenjian)
            print('ok')


if __name__ == '__main__':
    url = 'https://maoyan.com/board/4?offset=0'
    cat = Cat_eye()
    cat.get_page_content(url)
