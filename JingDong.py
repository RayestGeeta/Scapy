from bs4 import BeautifulSoup
import requests
import requests
import json
import os
# url = "https://search.jd.com/s_new.php?keyword=%E6%B4%97%E8%A1%A3%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E6%B4%97%E8%A1%A3%E6%9C%BA&psort=4&stock=1&page=6&s=151&scrolling=y&log_id=1582378905.85688&tpl=1_M&show_items=27389460145,61524715713,32146213301,60426496373,29822226862,22847584447,100006190620,13674506843,8262713,100005633422,22602257123,27136800042,39879969657,27136800041,32645404714,51558739033,51558739034,51558739035,27916347498,10712342805,6305527,7766495,26877037333,26877037335,26877037334,2302819,100007255984,3560448,28694326734,64894952662"
url = 'https://search.jd.com/s_new.php?keyword=%E6%B4%97%E8%A1%A3%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E6%B4%97%E8%A1%A3%E6%9C%BA&psort=4&stock=1&page=6&s=151&scrolling=y&log_id=1582378905.85688&tpl=1_M'
headers = {
    'Accept': '*/*',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'Referer':"https://item.jd.com/100000177760.html#comment"}
r = requests.get(url,headers=headers)



soup = BeautifulSoup(r, 'lxml')
for shop in soup.find_all('li', class_='gl-item')[:]:
    #print(shop['data-sku'])

    base_news = shop.text.split()[:-3]

    infos = ['价格', '产品名字', '产品id', '产品信息', '选购指数', '商家名字', '其他']
    process_news = {}
    process_news[infos[0]] = base_news[0]   
    process_news[infos[1]] = shop.find_all('em')[1].text
    process_news[infos[2]] = shop.find('div', class_='p-icons')['id']
    process_news[infos[3]] = shop.find('a')['title']
    if len(shop.find_all('em')) >= 3:
        process_news[infos[4]] = shop.find_all('em')[2].text   
    process_news[infos[5]] = shop.find('span', class_ = 'J_im_icon').text  
    print(process_news['产品名字'] + ' start.', end = '\t')
    if not os.path.exists(process_news['产品名字']):
        os.makedirs(process_news['产品名字'])

        with open(process_news['产品名字'] + '/base_infos.txt', 'w') as f:
            f.write(str(process_news))

    for page in range(50):
        for score in [1,2]:
            url = "https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId={}&score={}&sortType=5&page={}&pageSize=10&isShadowSku=0&fold=1".format(shop['data-sku'], str(score),str(page))
            r = requests.get(url,headers=headers)

            r.enconding = 'gb2312'

            comment = json.loads(r.text[20:-2])

            with open(process_news['产品名字'] + '/productCommentSummary.txt', 'w') as f:
                f.write(str(comment['productCommentSummary']))

            with open(process_news['产品名字'] + '/hotCommentTagStatistics.txt', 'w') as f:
                f.write(str(comment['hotCommentTagStatistics']))


            for com in comment['comments']:

                if ('replies' in com) and len(com['replies']) > 0:

                    if not os.path.exists(process_news['产品名字'] + '/' + str(com['id'])):
                        os.mkdir(process_news['产品名字'] + '/' + str(com['id']))

                        with open(process_news['产品名字'] + '/' + str(com['id']) + '/comment+replies.txt', 'w+')as f:
                            try:
                                f.write('content:\n')
                                f.write(com['content'])
                                f.write('\n\n')
                                f.write('replies:\n')
                                f.write(com['replies'][0]['content'])
                            except:
                                print('UnicodeEncodeError')
                        with open(process_news['产品名字'] + '/' + str(com['id']) + '/otherinfos.txt', 'w+') as f:
                            try:
                                f.write(str(com))
                            except:
                                print('UnicodeEncodeError')

    print('over')