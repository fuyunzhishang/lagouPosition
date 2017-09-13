#!usr/bin/env python
#_*_ coding: utf-8 _*_

import requests
import urllib2
import threading
from bs4 import BeautifulSoup
from lxml import etree #解析网页
import os #文件操作


def getHtml(url): 
  header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3107.4 Safari/537.36'}
  #req = requests.get(url = url, headers = header)
  req = urllib2.Request(url)
  res = urllib2.urlopen(req).read()
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
  for i in range(1,4):
    startHtml = getHtml(defaultUrl.format(i))
    groupList = getGroupList(startHtml)
    getImgSrc(groupList)

main()
print('爬取结束')