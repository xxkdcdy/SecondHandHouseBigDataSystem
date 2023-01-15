from selenium import webdriver
from bs4 import BeautifulSoup
import time
import random
import datetime
import sqlite3
import os
import Constraint as constraint

'''
作者：cdy
组件：爬虫工具，直接运行就可以爬取数据
'''


# 根据url获取Html界面的方法
def parse_url(url):
    chrome_options = webdriver.ChromeOptions()  # driver设置
    chrome_options.headless = True  # 不需要图形界面
    chrome = webdriver.Chrome(options=chrome_options)  # 新建一个Chrome实例
    chrome.get(url)  # Get请求
    html = chrome.page_source  # 返回Html文本
    page = BeautifulSoup(html, 'html.parser')  # 生成BeautifulSoup对象
    print(page.title.string)
    return page


# 获取基础信息
def get_base_info(_page_url):
    page = parse_url(_page_url)
    msgs = page.find_all('div', attrs={'class': 'property'})
    base_info = []
    for msg in msgs:
        ele_title = msg.findNext('div', attrs={'class': 'property-content-title'}).findNext('h3')  # 标题
        ele_url = msg.findNext('a')['href']  # url
        ele_total_num = msg.findNext('span', attrs={'class': 'property-price-total-num'})  # 总价数字
        ele_total_text = msg.findNext('span', attrs={'class': 'property-price-total-text'})  # 总价单位
        ele_unit_price = msg.findNext('p', attrs={'class': 'property-price-average'})  # 单价
        # 信息不全的就跳过
        if ele_title is None or ele_url.__class__ is None or \
                ele_total_num is None or ele_total_text is None or \
                ele_unit_price is None:
            continue
        _info = {'title': ele_title.text,
                 'url': ele_url.split('?')[0],
                 'total_price': ele_total_num.text + ele_total_text.text,
                 'unit_price': ele_unit_price.text}
        # print(_info)
        base_info.append(_info)
    return base_info


# 进入详情页获取更多信息
def get_extra_info(_info):
    info_url = _info['url']
    html = parse_url(info_url)
    ele_region = html.find('span', attrs={'class': 'maininfo-community-item-name'})  # 格式为 [城区 区域]
    ele_village_name = html.find('div', attrs={'class': 'community-title'})  # 小区名字
    ele_village_money = html.find('span', attrs={'class': 'monthchange-money'})  # 小区均价
    ele_village_info = html.findAll('p', attrs={'class': 'community-info-td-value'})  # 小区信息
    # 城区和区域
    if ele_region is None:
        _info['location1'] = ""
        _info['location2'] = ""
    else:
        _info['location1'] = ele_region.text.split()[0]
        _info['location2'] = ele_region.text.split()[1]
    # 小区名字
    if ele_village_name is None:
        _info['xiaoqu_name'] = ""
    else:
        _info['xiaoqu_name'] = ele_village_name.text.split()[0]
    # 小区均价
    if ele_village_money is None:
        _info['xiaoqu_price'] = ""
    else:
        _info['xiaoqu_price'] = ele_village_money.text.strip(' \t\n')
    if ele_village_info is not None:
        # 物业费用
        if len(ele_village_info) >= 2:
            _info['property_costs'] = ele_village_info[1].text.strip(' \t\n')
        else:
            _info['property_costs'] = ""
        # 容积率
        if len(ele_village_info) >= 3:
            _info['area_ratio'] = ele_village_info[2].text.strip(' \t\n')
        else:
            _info['area_ratio'] = ""
        # 绿化率
        if len(ele_village_info) >= 4:
            _info['green_ratio'] = ele_village_info[3].text.strip(' \t\n')
        else:
            _info['green_ratio'] = ""
    return _info


# 将具体信息放入数据库的过程
def Run(_conn, _result):
    _result = get_extra_info(_result)
    # 被反爬了，就没有抓到小区名字信息
    if _result['xiaoqu_name'] == "":
        return False
    _cursor = _conn.cursor()
    cursor.execute('INSERT INTO shHouse (title, url, total_price, unit_price, location1, location2, xiaoqu_name,'
                   ' xiaoqu_price, property_costs, area_ratio, green_ratio) '
                   'VALUES (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')'
                   .format(_result['title'], _result['url'],
                           _result['total_price'], _result['unit_price'],
                           _result['location1'], _result['location2'],
                           _result['xiaoqu_name'], _result['xiaoqu_price'],
                           _result['property_costs'], _result['area_ratio'],
                           _result['green_ratio']))
    _conn.commit()
    _cursor.close()
    return True


# 将具体信息放入数据库的过程
def is_exist(_conn, _result):
    _cursor = _conn.cursor()
    _cursor.execute('SELECT * FROM shHouse WHERE url = \'{}\' LIMIT 1'.format(_result['url']))
    if len(_cursor.fetchall()) == 1:
        _cursor.close()
        return True
    else:
        _cursor.close()
        return False


# 创建数据库的操作
def create_db():
    print('hello!')
    _conn = sqlite3.connect(constraint.path)
    _cursor = _conn.cursor()
    _cursor.execute('create table shHouse'
                    ' (_id integer primary key autoincrement,title varchar,url varchar,total_price varchar,'
                    'unit_price varchar,location1 varchar,location2 varchar,xiaoqu_name varchar,xiaoqu_price varchar,'
                    'property_costs varchar,area_ratio varchar,green_ratio varchar)')
    _cursor.close()
    return _conn


if __name__ == '__main__':
    # 获取当前时间
    now = datetime.datetime.now()
    _time = now.strftime("%Y-%m-%d %H:%M:%S")
    print(_time)

    if not os.path.exists(constraint.path):
        conn = create_db()  # 如果数据库文件不存在，就执行建表操作
    else:
        conn = sqlite3.connect(constraint.path)  # 否则就连接数据库
    cursor = conn.cursor()

    # 爬取第[x, y)页的数据
    for i in range(10, 12):
        time.sleep(random.randint(80, 120))  # 设置休息时间应对反爬
        page_url = constraint.base_url + str(i)
        results = get_base_info(page_url)
        for result in results:
            if is_exist(conn, result):
                print("{}：该数据已经存在！".format(result['url']))
            else:
                time.sleep(random.randint(80, 120))  # 设置休息时间应对反爬
                if Run(conn, result):
                    print("{}：插入一条数据！".format(result['url']))
                else:
                    print("{}：插入异常！".format(result['url']))
        print(f'爬取页面{i}的基础信息成功！')
