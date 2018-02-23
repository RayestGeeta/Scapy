import os
import requests
from bs4 import BeautifulSoup
url = 'http://www.shuaigepic.com/'
headers1 = {
    'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0',
    'Host':'www.shuaigepic.com'
}
html1 = requests.get(url,headers = headers1)
soup1 = BeautifulSoup(html1.text,'lxml')
path = '/home/shihao-z/lian1/'
all_a = soup1.find('div',class_='w960 mg picBox').find_all('a',target='_blank')
all_a.pop(0)
for a in all_a:
    url = 'http://www.shuaigepic.com/'+a['href']
    html = requests.get(url,headers = headers1)
    soup = BeautifulSoup(html.text,'lxml')
    title = soup.find('dt').text
    if(title !=''):
        print('开始盗取:'+title)
        if(os.path.exists(path+title.strip().replace('?',''))):
            flag = 1
        else:
            os.makedirs(path+title.strip().replace('?',''))
            flag = 0
        os.chdir(path + title.strip().replace('?',''))
        if(flag == 1 and len(os.listdir(path+title.strip().replace('?',''))) >= 5):
            print('已经盗取完毕，跳过')
            continue
        for i in range(1,7):
            url_n = '{}{}.{}'.format('_',str(i),'html')
            url1 = 'htt' + url.strip('.html')+url_n
            html = requests.get(url1,headers = headers1)
            soup = BeautifulSoup(html.text,'lxml')
            img = soup.find('img',id = 'bigimg')
            position = 'http://www.shuaigepic.com' + img['src']
            print(position)
            html =requests.get(position)

            file_name = img['src'].split(r'/')[-1]
            f = open(file_name,'wb')
            f.write(html.content)
            f.close()
            print('完成')
    print('本页完成')




            