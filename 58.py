import random

import requests
from lxml import html
import time
import re

import csv
etree = html.etree

fp = open('58nj.csv', 'a+', encoding='utf-8-sig',newline='')
csv_writer = csv.writer(fp, dialect='excel')
csv_writer.writerow(["标题", "总价（万）", "单价", "小区", "区域", "房间数", "大小",  "朝向","建造时间","标签"])

for i in range(1,50):
    time.sleep(random.randint(3,7))
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                      '87.0.4280.141 Safari/537.36',
    }
    url ='https://nj.58.com/ershoufang/p{}?'.format(i)

    page_text = requests.get(url=url,headers=headers).text

    tree = etree.HTML(page_text)
    li_list = tree.xpath('//section[@class="list"][1]/div')

    for li in li_list:
        title = li.xpath('normalize-space(./a/div[2]/div/div/h3/text())')
        price_count = li.xpath('normalize-space(./a/div[2]/div[2]/p[1]/span[1]/text())')
        price = li.xpath('./a/div[2]/div[2]/p[2]/text()')
        xiaoqu = li.xpath('normalize-space(./a/div[2]/div/section/div[2]/p/text())')
        quyu = li.xpath('normalize-space(./a/div[2]/div/section/div[2]/p[2]/span[1]/text())')
        home_num = li.xpath('normalize-space(./a/div[2]/div/section/div/p/span[1]/text())')
        size = li.xpath('normalize-space(./a/div[2]/div/section/div/p[2]/text())').replace(' ','')
        chaoxiang = li.xpath('normalize-space(./a/div[2]/div/section/div/p[3]/text())')
        jianzao = li.xpath('normalize-space(./a/div[2]/div[1]/section/div[1]/p[5]/text())')
        tags = li.xpath('./a/div[2]/div[1]/section/div[3]//text()')
        csv_writer.writerow([title, price_count, price[0], xiaoqu, quyu, home_num, size,chaoxiang, jianzao,tags])

        # filename.close()
fp.close()
print("over")


