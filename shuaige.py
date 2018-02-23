import requests
from bs4 import BeautifulSoup
import os
Hostreferer = {
    'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Referer':'http://www.mzitu.com'
               }
Picrefere = {
    'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0',
    'Referer':'http://i.meizitu.net'
}
url = 'http://www.mzitu.com/'
html1 = requests.get(url, headers = Hostreferer)
path = '/home/shihao-z/lian1/'
soup = BeautifulSoup(html1.text, 'html.parser')
a11_a = soup.find('div',class_ = 'postlist').find_all('a',target = '_blank')
for a in a11_a:
    title = a.get_text()
    if(title != ''):
        print('准备盗取：'+title)
        if(os.path.exists(path+title.strip().replace('?',''))):
            flag = 1
        else:
            os.makedirs(path+title.strip().replace('?',''))
            flag = 0
        os.chdir(path + title.strip().replace('?',''))
        href = a['href']
        html2 = requests.get(href,headers = Hostreferer)
        soup2 = BeautifulSoup(html2.text,'lxml')
        pmax = soup2.find_all('span')[10].text
        if(flag == 1 and len(os.listdir(path+title.strip().replace('?',''))) >= int(pmax)):
            print('已经盗取完毕，跳过')
            continue
        for num in range(1, int(pmax)):
            pic = href + '/' +str(num)
            html3 = requests.get(pic, headers = Hostreferer)
            soup3 = BeautifulSoup(html3.text, 'lxml')
            img = soup3.find('img',alt = title)
            print(img['src'])
            html1 = requests.get(img['src'],headers = Picrefere)
            file_name = img['src'].split(r'/')[-1]
            f = open(file_name,'wb')
            f.write(html1.content)
            f.close()
        print('完成')
print('本页完成')
