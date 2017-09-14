#!usr/bin/env python
#_*_ coding: utf-8 _*_

import requests
import urllib
import urllib2
import threading
from bs4 import BeautifulSoup
from lxml import etree #解析网页
import os #文件操作
import cookielib #cookie操作
import re

def getUrl():
  filename = 'cookie.txt'
  cookie = cookielib.MozillaCookieJar(filename)
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
  postdata = urllib.urlencode({
    'username':'17682339730',
    'password':'admin.123'
  })
  loginUrl = 'https://passport.lagou.com/login/login.html'
  result = opener.open(loginUrl, postdata)
  cookie.save(ignore_discard=True, ignore_expires=True)
  dataUrl = 'https://www.lagou.com/mycenter/collections.html?pageNo=2'
  result = opener.open(dataUrl)
  return result.url

def getHtml(url): 
  header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3107.4 Safari/537.36',
    'cookie':'user_trace_token=20170601194534-7364751b7aeb41d6b04a76184f19e2cd; LGUID=20170601194534-d2bfe997-46bf-11e7-8c7b-525400f775ce; JSESSIONID=ABAAABAAADEAAFIDDFF59CC92D58290373C9CB15448E28F; index_location_city=%E6%9D%AD%E5%B7%9E; TG-TRACK-CODE=jobs_code; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1505094908,1505180138,1505283398,1505351459; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1505379394; _gid=GA1.2.1508216302.1504967615; _gat=1; _ga=GA1.2.686392921.1496317550; LGSID=20170914165539-7b8de16c-992a-11e7-9256-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fjobs%2F2416257.html; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2F2416257.html; LGRID=20170914165539-7b8de2e3-992a-11e7-9256-525400f775ce; _putrc=F09C81F422A5F3C9; login=true; unick=%E5%BC%A0%E5%85%89%E8%BE%89; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=86'
  }
  req = requests.get(url = url, headers = header)
  #req = urllib2.Request('https://www.lagou.com/mycenter/collections.html?pageNo=2')
  res = req.content
  return res

def getGroupList(html):
  soup = BeautifulSoup(html, 'lxml') #实例化soup
  allPosition = soup.find_all('div', 'co_item') #获取所有职位链接
  groupList = [] #职位列表
  for link in allPosition:
    position_title = link.find('h2')['title'] #职位名称
    position_link = link.find('a')['href'] #职位链接
    company_name = link.find('div', 'co_cate').text #公司名称
    position_html = getHtml(position_link) #获取每个职位详情的源码
    position_soup = BeautifulSoup(position_html, 'lxml')
    positionAddr = position_soup.find_all('div','work_addr') #获取详情中的地址
    position_html = re.findall(r'\bwork_addr.*?</div>', position_html, re.S)
    positionGroup = {'title': imgGroup_title, 'html': img_html}
    groupList.append(imgGroup)
  return groupList

#获取图片地址
def getImgSrc(groupList):
  for group in groupList:
    groupTitle = group['title']
    groupHtml = group['html']
    #创建文件夹
    groupPath = 'H:\doutu2\\' + groupTitle
    groupPath.translate("|\\?*<\":>+[]/'")
    if not(os.path.exists(groupPath)):
      os.makedirs(groupPath)
    soup = etree.HTML(groupHtml)
    items = soup.xpath('//div[@class="artile_des"]')
    for item in items:
      imgUrlList = item.xpath('table/tbody/tr/td/a/img/@src')
      imgTitle = item.xpath('table/tbody/tr/td/a/img/@alt')
      startSaveImg(groupTitle,imgUrlList, imgTitle)
    

def saveImg(imgUrl, imgTitle, groupTitle):
  #print imgTitle[0]
  #print imgTitle[0].encode('utf-8')
  #imgUrl = imgUrl.split('=')[-1][1:-2].replace('jp','jpg') #提取url
  if imgUrl[0:2] == '//':
   imgUrl = 'http:' + imgUrl
  print('正在下载'  + imgUrl)
  imgContent = requests.get( imgUrl).content
  fileName = 'H:\doutu2\\' + groupTitle + '\\' + imgTitle[0] + '.jpg'
  with open(unicode(fileName), 'wb') as f:
    f.write(imgContent)

def startSaveImg(groupTitle,imgUrlList, imgTitle):
  for i in imgUrlList:
    th = threading.Thread(target=saveImg, args=(i, imgTitle, groupTitle))
    th.start()

def main():
  defaultUrl = 'https://www.lagou.com/mycenter/collections.html?pageNo={}'
  #defaultUrl = getUrl()
  for i in range(1,4):
    startHtml = getHtml(defaultUrl.format(i))
    groupList = getGroupList(startHtml)
    getImgSrc(groupList)

main()
print('爬取结束')