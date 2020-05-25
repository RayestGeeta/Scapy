import requests
from bs4 import BeautifulSoup
import pandas


headers = {
        'Connection': 'close',
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "accept-encoding": "gzip, deflate, br",
        "cache-control": "no-cache",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "cookie" : "global_cookie=cvgwqloe7oksvtftupwmtsn1o20jztnjsd5; city=sz; Integrateactivity=notincludemc; integratecover=1; SKHRecordssz=%252c%25e5%25b1%2585%25e5%25ae%25b6%25e4%25b8%2589%25e6%2588%25bf%252c%25e7%2589%25a9%25e4%25b8%259a%252c%25e4%25b8%259a%25e4%25b8%25bb%25e8%25af%259a%25e5%25bf%2583%25e5%2587%25ba%25e5%2594%25ae%257c%255e2019%252f8%252f27%2b19%253a56%253a33%257c%255e0%257c%2523%25e5%25a4%25a7%25e8%25bf%2590%25e6%2596%25b0%25e5%259f%258e%2b%25e5%258e%2585%25e5%2587%25ba%25e9%2598%25b3%25e5%258f%25b0%2b%25e7%25b2%25be%25e8%25a3%2585%25e4%25b8%2589%25e6%2588%25bf%2b%25e6%25bb%25a1%25e4%25b8%25a4%25e5%25b9%25b4%257c%255e2019%252f8%252f27%2b19%253a56%253a41%257c%255e0; __utma=147393320.1831537449.1566899575.1566905739.1566993019.4; __utmz=147393320.1566993019.4.4.utmcsr=search.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/captcha-c342d934c8/; g_sourcepage=ehlist; __utmc=147393320; logGuid=a4782b6a-96fe-4bbf-90e4-395577d22851; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; __utmb=147393320.18.10.1566993019; unique_cookie=U_klome40gpefgacg4y0p3st5ko1sjzv86iuc*6",
        "pragma": "no-cache",
        "referer": "https://sz.esf.fang.com/",
        "sec - fetch - mode": "navigate",
        "sec - fetch - site" : "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests" : "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
    }

data = []

for i in range(1, 9):
    url = 'https://data.eastmoney.com/cjsj/consumerpriceindex.aspx?p=' + str(i)
    print('Get ' + url)
    req = requests.get(url, headers = headers)
    html = BeautifulSoup(req.text, 'lxml')

    for i in html.find_all('tr')[2:-1]:
        
        data.append([i.text.split()[0]] + i.text.split()[1:5] + ['QG'])
        data.append([i.text.split()[0]] + i.text.split()[5:9] + ['CS'])
        data.append([i.text.split()[0]] + i.text.split()[9:13] + ['NC'])
        

final = pandas.DataFrame(data, columns= ['月份', '类型', '当月值', '同比增长', '环比增长', '累计'])
final.to_csv('CPI_FromEastMoney.csv')
