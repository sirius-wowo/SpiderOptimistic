'''
    对指定网址发起requests搜索请求
'''
import traceback
import json
import time
import requests
import urllib as ul
from urllib.parse import quote, unquote
import pandas as pd
import SpiderClientConfigure as scc
from retrying import retry
from w3lib import html
from NormalityRandom import normalityRandom
from urllib.parse import quote, unquote

'''指定url 和 搜索的关键字'''
@retry(stop_max_attempt_number=3, wait_random_min = 3000, wait_random_max = 7000)
def searchPageRequests(urlSource, companyKey, page = 1):
    url, headers, payloads = scc.spiderClient(urlSource, companyKey, page)
    if urlSource == '人民网':
        req = requests.post(url, headers=headers, data=json.dumps(payloads))

    elif urlSource == '新华网':
        while True:
            # req = requests.get(url, headers=headers, data=json.dumps(payloads))
            print("到这儿")
            req = requests.get(url)
            if req.json()['content']['results'] is not None:  break
        # req = requests.get(url)
    # print(req.status_code)
    return req.json()

'''获取在指定网址中，对应关键字搜索的具体页数'''
def searchPageRange(urlSource, companyKey):
    reqTmp = searchPageRequests(urlSource, companyKey)

    if urlSource == '人民网':
        pageRange = reqTmp['data']['pages']
    elif urlSource == '新华网':
        pageRange = reqTmp['content']['pageCount']

    # url, headers, payloads = scc.spiderClient(urlSource, companyKey, 1)
    # req = requests.post(url, headers=headers, data=json.dumps(payloads))
    # reqTmp = req.json()
    # pageRange = reqTmp['data']['pages']
    print("本次爬取共{}页".format(pageRange))
    return pageRange


'''解析一次搜索请求页面内的有效明细信息'''
def extractValidSearchContent(urlSource, searchIndexJson):
    if urlSource == '人民网':
        content = searchIndexJson['data']['records']
    elif urlSource == '新华网':
        # print(searchIndexJson['content']['results'])
        content = searchIndexJson['content']['results']


    if content is None:
        print("控制")
        print(searchIndexJson)
    return content


'''获取指定网页内指定关键字的所有搜索记录的明细: 搜索页面的网址、概述。并保存至csv'''
def saveIndexInformation(urlSource, companyKey):
    # 构建保存csv的dataframe
    smdf = pd.DataFrame(
        columns=['id', 'titleName', 'participateCompany', 'publishTime', 'url', 'newsSegment']
    )
    # 获取获取搜索的分页范围: 例如人民网搜索百度，每页返回10条明细，最多有结果200页
    pageRange = searchPageRange(urlSource, companyKey)

    for page in range(1, pageRange):
        # 适当调整每次request请求间的休眠间隔时间，防止反爬
        if page%20 == 1:
            rr = normalityRandom(1, 0.4)
            time.sleep(rr)
            print("休眠{}秒".format(rr))

        # 每次request返回的所有请求信息
        retrievalResult = searchPageRequests(urlSource, companyKey, page)

        # 获取有效的返回信息
        content =  extractValidSearchContent(urlSource, retrievalResult)

        # 循环解析搜索返回的每一页的新闻概要的明细
        for elemContent in content:
            if urlSource == '人民网':
                id = elemContent['id']
                titleName = html.remove_tags(str(elemContent['title']))
                participateCompany = companyKey
                publishTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(elemContent['displayTime'] / 1000))
                url = elemContent['url']
                newsSegment = html.remove_tags(str(elemContent['content']))
            elif urlSource == '新华网':
                id = elemContent['contentId']
                titleName = elemContent['title']
                participateCompany = companyKey
                publishTime = elemContent['pubtime']
                url = elemContent['url']
                newsSegment = elemContent['des']

            # 解析的明细存到csv
            newdf = pd.DataFrame({
                'id': id,
                'titleName': titleName,
                'participateCompany': participateCompany,
                'publishTime': publishTime,
                'url': url,
                'newsSegment': newsSegment,
            }, index=[1])
            smdf = smdf.append(newdf)
            # print("解析成功")
        print("总{pageTotal}第{n}页完成".format(pageTotal=pageRange, n=page))
    smdf.to_csv("{url}_{company}_news.csv".format(url = urlSource, company = companyKey),encoding='utf_8_sig')


'''解析相关新闻的详细内容'''




if __name__ == "__main__":
    urlSource = "人民网"
    companyKey = "百度"
    try:
        saveIndexInformation(urlSource, companyKey)
    except Exception as e:
        traceback.print_exc()

    # 测试新华网的get方法
    # url = 'http://so.news.cn/getNews?keyword=%E4%BE%9D%E5%9B%BE&curPage=1&sortField=0&searchFields=0&lang=cn'
    # req = requests.get(url)
    # print(req.status_code)
    # print('依图'.encode("UTF-8"))
    # print(quote('依图'))

    # print(requests.get('http://so.news.cn/getNews?keyword=%E4%BE%9D%E5%9B%BE&curPage=1&sortField=0&searchFields=0&lang=cn').json())