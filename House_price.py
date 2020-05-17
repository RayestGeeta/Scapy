'''
爬取房天下数据
'''
import requests
import re
from lxml import etree
import csv
import time

fp=open('fangtianxia.csv','w',newline='',encoding='utf-8')
writer=csv.writer(fp)
writer.writerow(('city','name','loc','size','area','price','price_sum','dire','floor','buildtime','advantage'))
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
city_list=[]

def get_info(city_url):
    i=re.search('house/i3(.*?)/',city_url).group(1)
    city_name=re.search('//(.*?).esf',city_url).group(1)
    print('正爬取{}第{}页'.format(city_name,i))
    #requests.packages.urllib3.disable_warnings()
    response=requests.get(city_url,headers=headers,timeout=None,verify=False)
    selector=etree.HTML(response.text)
    infos = selector.xpath('//dl[@dataflag="bg"]')
    try:
        for info in infos:
            name = info.xpath('dd/p[2]/a/@title')
            name = name[0] if len(name) != 0 else ' '
            loc = info.xpath('dd/p[2]/span/text()')[0]
            size = info.xpath('dd/p/text()[1]')[0].strip()
            area = info.xpath('dd/p/text()[2]')[0].strip()[:-2]
            dire = info.xpath('dd/p/text()[4]')[0].strip()
            floor = info.xpath('dd/p/text()[3]')[0].strip()
            buildtime = info.xpath('dd/p/text()[5]')
            buildtime = buildtime[0].strip() if len(buildtime) != 0 else '未知'
            price = info.xpath('dd[2]/span[2]/text()')[0].strip()[:-4]
            pricesum = info.xpath('dd[2]/span/b/text()')[0].strip()
            advantage = info.xpath('dd/p[3]')
            advantage = advantage[0].xpath('string(.)').strip()#获取连续多个标签的文本
            advantage = advantage if len(advantage) != 0 else '无'
            #print(city_name,name,loc,size,area,dire,floor,buildtime,price,pricesum,advantage)
            writer.writerow((city_name,name, loc, size, area, price, pricesum, dire, floor, buildtime, advantage))
    except IndexError:
        pass

if __name__=='__main__':
    city_name = ['sz']
    urls = ['https://{}.esf.fang.com'.format(city) for city in city_name]
    #print(urls)
    try:
        for url in urls:
            response = requests.get(url,headers=headers,timeout=None)
            page = re.findall('<p>共(.*?)页</p>', response.text)[0]
            #print(page)
            city_urls = [url +'/house/i3' + str(i) + '/' for i in range(1, int(page) + 1)]
            #print(city_urls)
            for city_url in city_urls:
                city_list.append(city_url)

    except IndexError:
        pass


    for city_ in city_list:
        try:
            get_info(city_)
        except:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            time.sleep(5)
            print("now let me continue...")
            continue

fp.close()