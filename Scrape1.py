# coding=gbk
import time
import json
import random
import requests
from bs4 import BeautifulSoup as bs


def list():
  url = "https://b2b.11467.com/search/40-";
  #urls = ["https://b2b.11467.com/search/40-14.htm", ""]

  list_url = ''
  for i in range(11, 21):
    list_url = url + str(i) + ".htm"
    
    response = ''
    try:
      response = requests.get(list_url)
    except:
      continue;
    
    #print(response.text)
    soup = bs(response.text, "html.parser")

    j = 0
    companys = []
    # Extract data from the page
    divs = soup.find_all("div", class_="f_l")
    #print(divs)
    for div in divs:
      #if(j > 0):
        # break;
      j += 1
      
      txt = div.text
      #print(txt)
      if(txt.find("采油") != -1 or txt.find("井下") != -1 or txt.find("海上") != -1 or txt.find("海洋") != -1 or txt.find("油田开发") != -1 or txt.find("油田科技") != -1 or txt.find("石油") != -1 or txt.find("天然气") != -1 or txt.find("开采") != -1 or txt.find("能源") != -1):
        if(txt.find("装修") != -1 or txt.find("餐饮") != -1 or txt.find("维修") != -1 or txt.find("家电") != -1 or txt.find("娱乐") != -1 or txt.find("文化") != -1 or txt.find("营业") != -1 or txt.find("银行") != -1 or txt.find("商场") != -1 or txt.find("医院") != -1 or txt.find("实业") != -1 or txt.find("加工厂") != -1):
          continue;
        company = {};  
        a = div.contents[0].next;
        company['公司名称'] = a.text;
      
        if len(div.contents) > 1:
          company['主营业务'] = div.contents[1].text;
        if len(div.contents) > 2:
          company['公司地址'] = div.contents[2].text;
        if len(div.contents) > 3:
          company['注册资本'] = div.contents[3].text;
        if len(div.contents) > 4:
          company['成立时间'] = div.contents[4].text;  
        
        try:
          company = detail(company, a.attrs['href'], j + 1);
        except : 
          pass
        
        if company is not None:
          companys.append(company)
      
    print('list success: ' + str(i) + '  ' + list_url)
    save(companys, i);
    
    time.sleep(random.randint(5, 10)) # sleep 5-10s
  
    
def detail(company, url, j):
  #print("Hello, detail!")
      
  headers = {}
  headers["Cookie"] = "Hm_lvt_819e30d55b0d1cf6f2c4563aa3c36208=1710811427,1710907149; Hm_lvt_291f91f93e981298bf9f990196e21722=1710811399,1710907192; Hm_lpvt_819e30d55b0d1cf6f2c4563aa3c36208=1710909924; Hm_lpvt_291f91f93e981298bf9f990196e21722=1710921133"
  headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
  headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
  headers["Accept-Encoding"] = "gzip, deflate, br"
  headers["Accept-Language"] = "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"
      
  #print(url)
  
  detail = ''
  try:
    detail = requests.get(url, headers = headers)
  except :
      return company
  
  detailsoup = bs(detail.text, "html.parser")
      
  #print(detailsoup.text)
  company['公司简介'] = detailsoup.find("div", id="aboutuscontent").text
  contactdiv = detailsoup.find("div", id="contact");
  #print(contactdiv)
  if(contactdiv is None):
    return company;
        
  dl = contactdiv.findChild('dl', class_='codl');
  for child in dl.children:
    #print(child.name)
    if(child.name == 'dd'):
      continue
    if(child.name == 'dt'):
      dt_name = child.text.replace("：", "")
      company[dt_name] = child.nextSibling.text
        
  legal = detailsoup.find("div", id="gongshang");   
  tb = legal.findChild('table', class_="codl");
  for child in tb.children:
    if(child.name == 'tr'):
      tds = child.find_all("td")
      td_name = tds[0].text.replace("：", "")
    if(td_name == "顺企编码" or td_name == '所属城市' or td_name == '获取报价'):
      continue
    company[td_name] = tds[1].text 
        
  print('detail success: ' + str(j) + '  ' + url)
  
  time.sleep(random.randint(5, 10)) # sleep 5-10s
  return company
    
def save(companys, i):
  if(len(companys) == 0):
    return;

  file = 'company/companies-11467-' + str(i) + '.json'
  with open(file, 'w', encoding='utf-8') as f:
    json.dump(companys, f, ensure_ascii= False, separators=[',\n', ':']) # ensure_ascii=False 不转换成ascii编码，即不转换成unicode
    
  print("save success: " + file)


def json_to_csv():
  json_list = []
  file = 'C:/Users/zfjem/Desktop/companys/companys-1.json'
  with open(file, 'r', encoding='utf-8') as f:
    json_str = f.read()
    json_list = json.decoder.JSONDecoder().decode(json_str)
  
  keys = ['公司名称','主营业务','公司地址','注册资本','公司简介','固定电话','法定代表人','经理手机','电子邮件','获取报价','邮政编码','法人名称','简称','主要经营产品','经营范围','营业执照号码','发证机关','经营状态','经营模式','成立时间','职员人数','公司官网','所属分类','类型']
  csv_str = '公司名称,主营业务,公司地址,注册资本,公司简介,固定电话,法定代表人,经理手机,电子邮件,获取报价,邮政编码,法人名称,简称,主要经营产品,经营范围,营业执照号码,发证机关,经营状态,经营模式,成立时间,职员人数,公司官网,所属分类,类型\n';
  for obj in json_list:
    #print(obj['公司名称'])
    if obj['经营状态'] is None or (obj['经营状态'] != '在业' and obj['经营状态'] != '存续'):
      continue
    for key in keys:
      if key in obj:
        val = obj[key]
        if(key == '主营业务'): 
          val = val.replace('主营产品：', '')
        csv_str += val.replace(',', ' ') + ','
      else:
        csv_str += ','
    csv_str += '\n'
  
  file = 'company/companies-11467-1.csv'
  with open(file, 'w', encoding='gb18030') as f:
    f.write(csv_str)
  print("save csv success: " + file)


def test_detail():
  print("Hello, test_detail!")  
  json = {}
  json = detail(json, 'https://www.11467.com/putian/co/51692.htm', 1);
  print(json)
  


def test_save():
  print("Hello, test_save!")
  companys = []
  companys.append({'公司名称': 'test1','地址': 'test1','电话': 'test1'})
  companys.append({'公司名称': 'test2'})
  save(companys, 1)


def test_range():
  for i in range(1, 2):
    print(i)
    



json_to_csv()