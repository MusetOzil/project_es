import requests

url = 'http://httpbin.org/get'
proxies = {
    'http': '60.13.42.203:9999',
    'https': '221.206.100.133:34073',
}
heanders = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
}
#    :param headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
#    :param proxies: (optional) Dictionary mapping protocol to the URL of the proxy.


response = requests.get(url=url, headers=heanders, proxies=proxies)
print(response.text)
