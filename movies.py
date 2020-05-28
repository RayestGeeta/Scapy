# 导入包
# 请求网站包
import requests
# 解析网站包
from bs4 import BeautifulSoup
# 保存数据用的包
import pandas
# 进度条 方便观看爬取进度
from tqdm import tqdm


data = []
# 国内电影一共126页
for u in tqdm(range(1,126)):
    
    # 构建url
    url = 'https://dytt8.net/html/gndy/china/list_4_'+str(u)+'.html'
    # 请求访问
    req = requests.get(url, timeout = 10000)
    # 编码改为gb2312（网站编码）
    req.encoding = 'gb2312'
    # 解析网站
    soup = BeautifulSoup(req.text, 'lxml')
    
    # 查找每部电影的信息标签
    for i in range(len(soup.find_all('table', class_="tbspan"))):
        #print(soup.find_all('table', class_="tbspan")[i].find_all('a')[1].text[:4])
        
        # 判断是否是2020年的电影
        if soup.find_all('table', class_="tbspan")[i].find_all('a')[1].text[:4] == '2020':
            # 将电影名字 年份 内容保存在数据中
            data.append([soup.find_all('table', class_="tbspan")[i].find_all('a')[1].text, '2020', soup.find_all('table', class_="tbspan")[i].find('td', style="padding-left:3px", colspan="2").text])
            
        # 判断是否是2010年的电影
        if soup.find_all('table', class_="tbspan")[i].find('font').text.split()[0].split('：')[1].split('-')[0] == '2010':
            # 将电影名字 年份 内容保存在数据中
            data.append([soup.find_all('table', class_="tbspan")[i].find_all('a')[1].text, '2010', soup.find_all('table', class_="tbspan")[i].find('td', style="padding-left:3px", colspan="2").text])
            
# 保存为csv文件
pandas.DataFrame(data).to_csv('data.csv')
