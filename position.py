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
import xlsxwriter
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def getUrl():
  filename = 'cookie.txt'
  cookie = cookielib.MozillaCookieJar(filename)
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
  postdata = urllib.urlencode({
    'username':'',
    'password':''
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
    'cookie':'user_trace_token=20170601194534-7364751b7aeb41d6b04a76184f19e2cd; LGUID=20170601194534-d2bfe997-46bf-11e7-8c7b-525400f775ce; JSESSIONID=ABAAABAAAIAACBI18AD37E5ADB6206CE4554823FB6C8496; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=100; _putrc=F09C81F422A5F3C9; login=true; unick=%E5%BC%A0%E5%85%89%E8%BE%89; _gid=GA1.2.1508216302.1504967615; _ga=GA1.2.686392921.1496317550; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1505553300,1505607302,1505657254,1505697051; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1505704164; LGRID=20170918110818-9eae6daf-9c1e-11e7-965a-525400f775ce; TG-TRACK-CODE=search_code; SEARCH_ID=8af6dded22d545078c0ae6e39fcf76d8; index_location_city=%E6%9D%AD%E5%B7%9E'
  }
  req = requests.get(url = url, headers = header)
  #req = urllib2.Request('https://www.lagou.com/mycenter/collections.html?pageNo=2')
  res = req.content
  return res

def getGroupList(html):
  soup = BeautifulSoup(html, 'lxml') #实例化soup
  allPosition = soup.find_all('div', 'co_item') #获取所有职位链接
  positionList = [] #职位列表
  for link in allPosition:
    position_title = link.find('h2')['title'] #职位名称
    position_link = link.find('a')['href'] #职位链接
    company_name = link.find('div', 'co_cate').text #公司名称
    position_html = getHtml(position_link) #获取每个职位详情的源码
    position_soup = BeautifulSoup(position_html, 'lxml')
    positionAddr = position_soup.find('div','work_addr') #获取详情中的地址
    #position_html = re.findall(r'\bwork_addr.*?</div>', position_html, re.S)
    position_addr_str = str(positionAddr.get_text(strip=True))
    rule = re.compile(r'查看地图')
    result = rule.sub('',position_addr_str)
    position_info = []
    position_info.append(position_title)
    position_info.append(company_name)
    position_info.append(position_link)
    position_info.append(result)
    #positionGroup = {'title': imgGroup_title, 'html': img_html}
    positionList.append(position_info)
  return positionList

#保存到Excel
def saveToXls(groupList):
  book = xlsxwriter.Workbook(r'E:\positions\favorite-position.xls')
  tmp = book.add_worksheet()
  row_num = len(groupList)
  for i in range(1, row_num):
    if i == 1:
      tag_pos = "A%s" % i
      tmp.write_row(tag_pos, ['职位名称', '公司名称', '职位链接', '详细地址'])
    else:
      con_pos = 'A%s' % i
      k_v = groupList[i-2]
      tmp.write_row(con_pos, k_v)
  book.close()


def main():
  defaultUrl = 'https://www.lagou.com/mycenter/collections.html?pageNo={}'
  groupList = []
  for i in range(1,4):
    startHtml = getHtml(defaultUrl.format(i))
    groupList.extend(getGroupList(startHtml))
  saveToXls(groupList)
main()
print('爬取结束')