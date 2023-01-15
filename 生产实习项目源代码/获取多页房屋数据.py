import time
import pandas as pd
import requests
from bs4 import BeautifulSoup

# lxml
# openpyxl
# xlrd
# xlwt
# xlrd版本高，导致无法读xlsx，故保存为xls

url_lj = "https://tj.lianjia.com/ershoufang/pg{}/"
file_name = r'F:/PyCharm/scsx/static/链家二手房tj多页数据.xls'
sleep_time = 1
title_list = []
post_list = []
house_list = []
follow_list = []
price_list = []
u_price_list = []

for page in range(1, 101):
    url = url_lj.format(page)
    res = requests.get(url,
                       headers={
                           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 '
                                         '(KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36)'
                       }
                       #                   proxies=proxies
                       )

    # print(res.status_code)
    # print(res.text)
    soup = BeautifulSoup(res.text, 'lxml')
    # 点名道姓的查找
    title_html = soup.find_all(name='a', attrs={'data-el': "ershoufang"})
    for i in title_html:
        if i.text:  # 如果i.text非空
            title_list.append(i.text)
    # print(title_list)
    # print(len(title_list))

    post_html = soup.find_all(name='div', class_="positionInfo")
    for i in post_html:
        if i.text:
            post_list.append(i.text)
    # print(post_list)
    # print(len(post_list))

    house_html = soup.find_all(name='div', class_="houseInfo")
    for i in house_html:
        if i.text:
            house_list.append(i.text)
    # print(house_list)
    # print(len(house_list))

    follow_html = soup.find_all(name='div', class_="tag")
    for i in follow_html:
        # if i.text:
        follow_list.append(i.text)
    # print(follow_list)
    # print(len(follow_list))

    price_html = soup.find_all(name='div', class_="totalPrice totalPrice2")
    for i in price_html:
        if i.text:
            price_list.append(i.text)
    # print(price_list)
    # print(len(price_list))

    u_price_html = soup.find_all(name='div', class_="unitPrice")
    for i in u_price_html:
        if i.text:
            u_price_list.append(i.text)
    # print(u_price_list)
    # print(len(price_list))
d = {
    '房屋标题': title_list,
    '房屋区域': post_list,
    '房屋信息': house_list,
    '房屋评价': follow_list,
    '房屋总价': price_list,
    '房屋单价': u_price_list
}

df = pd.DataFrame(d)
df.to_excel(file_name)
time.sleep(sleep_time)
