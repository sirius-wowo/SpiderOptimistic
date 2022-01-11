'''
    定义获取的网站等等自定义信息: headers url payload
'''

from urllib.parse import quote, unquote
def spiderClient(urlSource, companyKey, pageKey = 1):

    # 选择爬取的网页源
    # 人民网
    if urlSource == '人民网':
        url = 'http://search.people.cn/search-platform/front/search'
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '133',
            'Content-Type': 'application/json',
            'Host': 'search.people.cn',
            'Origin': 'http://search.people.cn',
            'Referer': 'http://search.people.cn/s?keyword=%E6%B7%98%E5%AE%9D&st=0&_=1639417440181',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
        }
        payloads = {
            'endTime': 0,
            'hasContent': True,
            'hasTitle': True,
            'isFuzzy': False,
            'key': companyKey,
            # 'key': '"百度"',
            'limit': 100,
            'page': pageKey,
            'sortType': 2,
            'startTime': 0,
            'type': 0
        }
    elif urlSource == '新华网':
        url = 'http://so.news.cn/getNews?keyword={company}&curPage={curPage}&sortField=0&searchFields=0&lang=cn'.format(company = quote(companyKey), curPage = pageKey)
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '133',
            'Content-Type': 'application/json',
            'Host': 'so.news.cn',
            'Origin': 'http://search.people.cn',
            'Referer': 'http://so.news.cn/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
        }
        payloads = {
            'keyword': companyKey,
            'curPage': pageKey,
            'sortField': 0,
            'searchFields': 1,
            'lang': 'cn'
        }

    return url, headers, payloads

if __name__ == "__main__":
    url, headers, payloads = spiderClient("新华网", '依图', 1)
    print(url)