'''
  爬虫：爬取大工教务本科生通知
'''
import requests
from bs4 import BeautifulSoup
URL = 'http://ssdut.dlut.edu.cn/bkspy/benkeshengjiaoxue.htm'
RES = requests.get(URL)
RES.encoding = 'utf-8'
SOUP = BeautifulSoup(RES.text, 'lxml')
INFORS = SOUP.select('.mt_10 a')
for infor in INFORS:
    print(infor['title'], end=':')
    arctile = 'http://ssdut.dlut.edu.cn'+infor['href'].strip('..')
    print(arctile)
    res1 = requests.get(arctile)
    res1.encoding = 'utf-8'
    soup1 = BeautifulSoup(res1.text, 'lxml')
    print(soup1.select('#vsb_content p')[0].text)
    print()

#http://ssdut.dlut.edu.cn/bkspy/benkeshengjiaoxue.htm
#http://ssdut.dlut.edu.cn/info/1120/12070.htm
#http://ssdut.dlut.edu.cn//info/1120/12061.htm
