#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020-11-08 21:16:07
# @Author  : Muxiaoxiong
# @email   : xiongweinie@foxmail.com

"""
蛋壳公寓房屋信息爬取
总共有267页
"""

import requests
from lxml import etree
from bs4 import BeautifulSoup
import random
import time
from tqdm import tqdm
import csv


#这里增加了很多user_agent
#能一定程度能保护爬虫
user_agent = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)"]


def get_info():
    #武汉地区总共有267页
    csvheader=['价格','面积','编号','户型','楼层','朝向','位置1','位置2','小区','地铁']
    with open('wuhan_danke.csv', 'a+', newline='') as csvfile:
        writer  = csv.writer(csvfile)
        writer.writerow(csvheader)
        for i in tqdm(range(1,268)):  #总共有267页
            timelist=[1,2]
            time.sleep(random.choice(timelist))   #休息2-5秒，防止给对方服务器过大的压力！！！
            url='https://www.danke.com/room/wh?search=1&search_text=&from=home&page={}'.format(i)
            headers = {'User-Agent': random.choice(user_agent)}
            r = requests.get(url, headers=headers)
            r.encoding = r.apparent_encoding
            soup = BeautifulSoup(r.text, 'lxml')
            all_info = soup.find_all('div', class_='r_lbx_cena')
            for info in all_info:
                href = info.find('a')
                if href !=None:
                    href=href['href']
                    house_info=get_house_info(href)
                    writer.writerow(house_info)
def get_house_info(href):
    #得到房屋的信息
    time.sleep(1)
    headers = {'User-Agent': random.choice(user_agent)}
    response = requests.get(url=href, headers=headers)
    response=response.content.decode('utf-8', 'ignore')
    div = etree.HTML(response)
    print(div)
    room_price=div.xpath("/html/body/div[3]/div[1]/div[2]/div[2]/div[3]/div[2]/div/span/div/text()")[0]
    room_area=div.xpath("/html/body/div[3]/div[1]/div[2]/div[2]/div[4]/div[1]/div[1]/label/text()")[0].replace('建筑面积：约','').replace('㎡（以现场勘察为准）','')
    room_id=div.xpath("/html/body/div[3]/div[1]/div[2]/div[2]/div[4]/div[1]/div[2]/label/text()")[0].replace('编号：','')
    room_type=div.xpath("/html/body/div[3]/div[1]/div[2]/div[2]/div[4]/div[1]/div[3]/label/text()")[0].replace('\n','').replace(' ','').replace('户型：','')
    room_floor=div.xpath("/html/body/div[3]/div[1]/div[2]/div[2]/div[4]/div[2]/div[3]/label/text()")[0].replace('楼层：','')
    room_dir=div.xpath("/html/body/div[3]/div[1]/div[2]/div[2]/div[4]/div[2]/div[1]/label/text()")[0].replace("朝向：","")
    room_postion_1=div.xpath("/html/body/div[3]/div[1]/div[2]/div[2]/div[4]/div[2]/div[4]/label/div/a[1]/text()")[0]
    room_postion_2=div.xpath("/html/body/div[3]/div[1]/div[2]/div[2]/div[4]/div[2]/div[4]/label/div/a[2]/text()")[0]
    room_postion_3=div.xpath("/html/body/div[3]/div[1]/div[2]/div[2]/div[4]/div[2]/div[4]/label/div/a[3]/text()")[0]
    room_subway=div.xpath("/html/body/div[3]/div[1]/div[2]/div[2]/div[4]/div[2]/div[5]/label/text()")[0]
    room_info=[room_price,room_area,room_id,room_type,room_floor,room_dir,room_postion_1,room_postion_2,room_postion_3,room_subway]
    return room_info
if __name__ == '__main__':
    get_info()
