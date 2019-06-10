


# URLError:来自urllib库的error模块，继承自OSError,由request模块产生的异常都可以通过捕捉这个类来处理．
# 产生的原因主要有：
# 没有网络连接
# 服务器连接失败
# 找不到指定的服务器
# 它具有一个属性reason,返回错误的原因
# HTTPError
# HTTPError是URLError的子类，我们发出一个请求时，服务器上都会对应一个response应答对象，其中它包含一个数字"响应状态码"。
# 专门用来处理ＨTTP请求错误，比如未认证，页面不存在等
# 有三个属性：
# code:返回HTTP的状态码
# reason:返回错误原因
# headers:返回请求头


from urllib import error,request
import ssl
def error_test(url):
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'

    }
    ssl_contex = ssl._create_default_https_context()
    req = request.Request(url = url,headers = headers)
    try:
        response = request.urlopen(req,context=ssl_contex,timeout=90)
        print(response.status)
    except error.HTTPError as err :
        print(err.code,err.reason)
    except error.URLError as err:
        print(err.reason)


if __name__ == '__main__':
    error_test('https://www.baidu.com/')