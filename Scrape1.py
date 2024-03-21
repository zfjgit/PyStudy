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
      if(txt.find("����") != -1 or txt.find("����") != -1 or txt.find("����") != -1 or txt.find("����") != -1 or txt.find("���￪��") != -1 or txt.find("����Ƽ�") != -1 or txt.find("ʯ��") != -1 or txt.find("��Ȼ��") != -1 or txt.find("����") != -1 or txt.find("��Դ") != -1):
        if(txt.find("װ��") != -1 or txt.find("����") != -1 or txt.find("ά��") != -1 or txt.find("�ҵ�") != -1 or txt.find("����") != -1 or txt.find("�Ļ�") != -1 or txt.find("Ӫҵ") != -1 or txt.find("����") != -1 or txt.find("�̳�") != -1 or txt.find("ҽԺ") != -1 or txt.find("ʵҵ") != -1 or txt.find("�ӹ���") != -1):
          continue;
        company = {};  
        a = div.contents[0].next;
        company['��˾����'] = a.text;
      
        if len(div.contents) > 1:
          company['��Ӫҵ��'] = div.contents[1].text;
        if len(div.contents) > 2:
          company['��˾��ַ'] = div.contents[2].text;
        if len(div.contents) > 3:
          company['ע���ʱ�'] = div.contents[3].text;
        if len(div.contents) > 4:
          company['����ʱ��'] = div.contents[4].text;  
        
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
  company['��˾���'] = detailsoup.find("div", id="aboutuscontent").text
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
      dt_name = child.text.replace("��", "")
      company[dt_name] = child.nextSibling.text
        
  legal = detailsoup.find("div", id="gongshang");   
  tb = legal.findChild('table', class_="codl");
  for child in tb.children:
    if(child.name == 'tr'):
      tds = child.find_all("td")
      td_name = tds[0].text.replace("��", "")
    if(td_name == "˳�����" or td_name == '��������' or td_name == '��ȡ����'):
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
    json.dump(companys, f, ensure_ascii= False, separators=[',\n', ':']) # ensure_ascii=False ��ת����ascii���룬����ת����unicode
    
  print("save success: " + file)


def json_to_csv():
  json_list = []
  file = 'C:/Users/zfjem/Desktop/companys/companys-1.json'
  with open(file, 'r', encoding='utf-8') as f:
    json_str = f.read()
    json_list = json.decoder.JSONDecoder().decode(json_str)
  
  keys = ['��˾����','��Ӫҵ��','��˾��ַ','ע���ʱ�','��˾���','�̶��绰','����������','�����ֻ�','�����ʼ�','��ȡ����','��������','��������','���','��Ҫ��Ӫ��Ʒ','��Ӫ��Χ','Ӫҵִ�պ���','��֤����','��Ӫ״̬','��Ӫģʽ','����ʱ��','ְԱ����','��˾����','��������','����']
  csv_str = '��˾����,��Ӫҵ��,��˾��ַ,ע���ʱ�,��˾���,�̶��绰,����������,�����ֻ�,�����ʼ�,��ȡ����,��������,��������,���,��Ҫ��Ӫ��Ʒ,��Ӫ��Χ,Ӫҵִ�պ���,��֤����,��Ӫ״̬,��Ӫģʽ,����ʱ��,ְԱ����,��˾����,��������,����\n';
  for obj in json_list:
    #print(obj['��˾����'])
    if obj['��Ӫ״̬'] is None or (obj['��Ӫ״̬'] != '��ҵ' and obj['��Ӫ״̬'] != '����'):
      continue
    for key in keys:
      if key in obj:
        val = obj[key]
        if(key == '��Ӫҵ��'): 
          val = val.replace('��Ӫ��Ʒ��', '')
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
  companys.append({'��˾����': 'test1','��ַ': 'test1','�绰': 'test1'})
  companys.append({'��˾����': 'test2'})
  save(companys, 1)


def test_range():
  for i in range(1, 2):
    print(i)
    



json_to_csv()