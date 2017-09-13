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
    'cookie':'user_trace_token=20170913211153-18c5fcea-db55-4cab-8179-60ff170bf9a9; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1505308378; LGUID=20170913211154-1d5e76b6-9885-11e7-916c-525400f775ce; _ga=GA1.2.508912555.1505308378; _gid=GA1.2.1369602333.1505308381; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=86; JSESSIONID=ABAAABAAAIAACBI152563A0F847949B8CEE0EE69CD607A1; X_HTTP_TOKEN=b43bc3b8df94b280deececc67b57024d; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1505317340; LGRID=20170913234117-fb70335d-9899-11e7-9173-5254005c3644; _putrc=F09C81F422A5F3C9; login=true; unick=%E5%BC%A0%E5%85%89%E8%BE%89; _gat=1; LGSID=20170913234117-fb703021-9899-11e7-9173-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fmycenter%2Fcollections.html%3FpageNo%3D3'
  }
  req = requests.get(url = url, headers = header)
  #req = urllib2.Request('https://www.lagou.com/mycenter/collections.html?pageNo=2')
  res = req.content
  return res

def getGroupList(html):
  soup = BeautifulSoup(html, 'lxml') #实例化soup
  allPosition = soup.find_all('a', class_='target') #获取所有职位链接
  groupList = [] #套图列表
  for link in allImg:
    img_html = getHtml(link['href']) #获取每个套图详情的源码
    imgGroup_title = link.find_all('div', class_='random_title')[0].contents[0]
    imgGroup = {'title': imgGroup_title, 'html': img_html}
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