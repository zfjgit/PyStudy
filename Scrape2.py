#coding=gbk
import random
from shlex import join
import requests
import json
import time
from bs4 import BeautifulSoup

headers = {}
headers["Cookie"] = "Hm_lvt_2de4d2592c7d7a7193a646ad89b38990=1710946024,1710984476,1711012647,1711081291; Hm_lpvt_2de4d2592c7d7a7193a646ad89b38990=1711081291"
headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
headers["Accept-Encoding"] = "gzip, deflate, br"
headers["Accept-Language"] = "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"

keys = ['公司名称','公司网站','法人代表','注册资本','成立时间', '公司地址', '公司简介'];

def scrape():
  url = "http://www.zk71.com/2qiye/page";
  
  list_url = ''
  
  companies_data = []
  
  for i in range(16, 21):
    list_url = url + str(i)
    
    response = ''
    try:
      response = requests.get(list_url, headers=headers)
      if(response is None or response.status_code != 200):
        continue 
    except:
      continue;

    # 解析HTML内容
    soup = BeautifulSoup(response.text, 'html.parser')
    
    print(f'load page success: {list_url}')
    
    # 找到所有的公司列表项
    div = soup.find('div', class_='hy_lb_b');

    for item in div.find_all('li'):
        company = {}
    
        # 获取公司名称和链接
        company['公司名称'] = item.find('a').text.strip()
        company['公司网站'] = 'http://www.zk71.com' + item.find('a')['href']
    
        # 获取法定代表人、注册资本和成立时间
        details = item.find('div', class_='hy_em').find_all('em')
        company['法人代表'] = details[0].text.split('：')[1].strip()
        company['注册资本'] = details[1].text.split('：')[1].strip()
        company['成立时间'] = details[2].text.split('：')[1].strip()

        # 获取地址
        prag = item.find('div', class_='hy_em').find_all('p')
        company['公司地址'] = prag[0].text.replace('地址：', '').split('\n')[0].strip()
        company['公司简介'] = prag[1].text.split('\n')[0].strip()

        c_str = '';
        for key in keys:
          if key not in company:
            c_str += ','
          else:
            c_str += company[key].replace(',', ' ') + ','
           
        companies_data.append(c_str)
        
    time.sleep(random.randint(5, 10)) # sleep 5-10s
  
  print(f'scrape success, data in total: {len(companies_data)}')
  
  if(len(companies_data) <= 0):
     return;
  
  # 将数据转换为JSON格式
  #json_data = json.dumps(companies_data, ensure_ascii=False, separators=[',\n', ':'])

  # 输出或保存JSON数据
  #print(json_data)
  # 或者保存到文件
  file = f'company/companies-zk71-{i}.csv'
  d_str = ','.join(keys) + '\n' + '\n'.join(companies_data)
  with open(file, 'w', encoding='gb18030') as f:
      f.write(d_str)
  
  print(f'save success: {file}')    
      
scrape()