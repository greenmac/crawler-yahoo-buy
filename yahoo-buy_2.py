import requests
from pyquery import PyQuery as pq
import pymongo
import pymysql
from pymongo import MongoClient
import datetime
import time

dataSet = []
now_start_time = datetime.datetime.now()

today = datetime.datetime.today().strftime('%Y-%m-%d')
item_name = 'item_%s' % today

try:
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='curry30', charset='utf8')
    cursor = db.cursor()
    db_name = 'runrun'
    db_create = "CREATE DATABASE IF NOT EXISTS `%s`" % (db_name)

    exe_sql_create = cursor.execute(db_create)
    cursor.execute("ALTER DATABASE `%s` CHARACTER SET 'utf8' COLLATE 'utf8_unicode_ci'" % db_name)

    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='curry30',db=db_name, charset='utf8', autocommit=True)
    cursor = db.cursor()
    sql_create = 'CREATE TABLE IF NOT EXISTS `%s` (id int(11) NOT NULL AUTO_INCREMENT, number int(20), title varchar(100), price varchar(32), add_time varchar(32), PRIMARY KEY (id))' % item_name
    exe_sql_create = cursor.execute(sql_create)
except Exception as e:
    pass

def index_page(index_url):
    start_time = time.time()
    try:
        res = requests.get(index_url)
        res.encoding = 'big5' # res.encoding看文字編碼, 然後更改到big5(要看原網頁設定)
        doc = pq(res.text)
        doc.make_links_absolute(base_url=res.url) # 變成絕對路徑
        site_list1 = doc('.content .site-list').items()
        for eachLv1Doc in site_list1:
            lv1_Doc = eachLv1Doc('a').attr('href')
            lv1_page(lv1_Doc)
        print('All items were insert')
        now_stop_time = datetime.datetime.now()
        print('All items insert now_start_time:', now_start_time)
        print('All items insert now_stop_time:', now_stop_time)

    except Exception as e:
        print(e)
        error_stop_time = datetime.datetime.now()
        print('error_stop_time:', error_stop_time)
    end_time  = time.time()
    cost_time = end_time - start_time
    m, s = divmod(cost_time, 60)
    h, m = divmod(m, 60)
    print("It cost %f sec" % (cost_time))
    print("All time cost %d:%02d:%02d" % (h, m, s))


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
        sql = "insert into `%s` (number, title, price, add_time) values (%s, '%s', '%s', '%s')"  % (item_name, number, itemDict['title'], itemDict['price'], add_time)
        cursor.execute(sql)
        # db.commit()
        print (sql)

index_page('https://tw.buy.yahoo.com/help/helper.asp?p=sitemap')
# for eachDataSet in dataSet:
#     print(eachDataSet)