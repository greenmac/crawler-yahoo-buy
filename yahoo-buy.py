import requests
from pyquery import PyQuery as pq
import pymongo
from pymongo import MongoClient
import datetime

dataSet = []
now_time = datetime.datetime.now()
def index_page(index_url):
    try:
        res = requests.get(index_url)
        res.encoding = 'big5' # res.encoding看文字編碼, 然後更改到big5(要看原網頁設定)
        doc = pq(res.text)
        doc.make_links_absolute(base_url=res.url) # 變成絕對路徑
        site_list1 = doc('.content .site-list').items()
        for eachLv1Doc in site_list1:
            lv1_Doc = eachLv1Doc('a').attr('href')
            lv1_page(lv1_Doc)
    except:
        print('stop time:', now_time)


def lv1_page(url):
        lv1Doc = pq(url)
        lv1Doc.make_links_absolute()  # 變成絕對路徑
        list1 = lv1Doc('#cl-menucate .sitelist:nth-child(1) .stitle').text()
        if '活動' in list1:
            list1_1 = lv1Doc('#cl-menucate .sitelist:nth-child(n+2) .list').items() # nth-child(n+2) 從第二個開始選(不選第一個促銷區的標題)
            for eachLv2Doc in list1_1:
                lv2Doc = eachLv2Doc('a').attr('href')
                lv2_page(lv2Doc)
        else:
            list1_2 = lv1Doc('#cl-menucate .sitelist .list').items()
            for eachLv2Doc in list1_2:
                lv2Doc = eachLv2Doc('a').attr('href')
                lv2_page(lv2Doc)

def lv2_page(url):
    # now_time = datetime.datetime.now()
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    client = MongoClient('127.0.0.1', 27017)
    db = client['yahoo_buy']
    item_name = 'item_%s' % today
    collect = db[item_name]
    # collect = db['item']
    lv2Doc = pq(url)
    item1 = lv2Doc('#srp_result_list .item').items()
    add_time = datetime.datetime.now()
    number = 0
    for eachItem in item1:
        itemDict = {}
        itemDict['title'] = eachItem('.srp-pdtitle').text()
        itemDict['price'] = eachItem('.srp-listprice').text()
        dataSet.append(itemDict)
        number += 1
        item_dict = {
            'number' : number,
            'title' : itemDict['title'],
            'price' : itemDict['price'],
            'add_time' : add_time,
        }
        rs = collect.insert_one(item_dict)
        object_id = rs.inserted_id
        # return ('object_id: ' + str(object_id))
        print (str(item_dict))
    print('All items were insert')

index_page('https://tw.buy.yahoo.com/help/helper.asp?p=sitemap')
# for eachDataSet in dataSet:
#     print(eachDataSet)