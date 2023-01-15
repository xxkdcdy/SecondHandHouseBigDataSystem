import sqlite3
import pandas as pd
import os

'''
作者：cdy
组件：保存全局变量和配置的工具类
'''


path = os.getcwd() + "/bs_shHouse.db"  # 数据库存储路径，当前保存在运行路径下
base_url = 'https://zj.58.com/ershoufang/p'  # 镇江二手房网，镇江房产网，镇江二手房买卖出售交易信息-镇江58同城
page_size = 10  # 每一页数据的行数
font_size = 11  # 绘制图形的字体大小
# DataFrame所有的列名
cols = ['id', '标题', 'url', '总价', '均价', '位置1', '位置2', '小区名', '小区均价', '物业费', '容积率', '绿化率']


# 获取数据库里的所有数据
def select_all():
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute('SELECT * FROM shHouse')
    res = cur.fetchall()
    cur.close()
    con.close()
    return res


# 将数据标准化处理
def std_data():
    values = select_all()
    data = pd.DataFrame(data=values, columns=cols)
    data = data.drop(columns=['标题', 'url', '位置2'])
    data = data.dropna()
    data.drop(data.index[(data['物业费'] == '暂无')], inplace=True)    # 删除物业费为暂无的行
    data.drop(data.index[(data['容积率'] == '暂无')], inplace=True)    # 删除容积率为暂无的行
    data.drop(data.index[(data['绿化率'] == '暂无')], inplace=True)    # 删除绿化率为暂无的行

    # 将非字符数据恢复成float，方便计算
    data['均价'] = data['均价'].apply(lambda x: float(x.split('元')[0]))
    data['小区均价'] = data['小区均价'].apply(
        lambda x: float(x.split('元')[0]))
    data['物业费'] = data['物业费'].apply(
        lambda x: float(x.split('元')[0]))
    data['绿化率'] = data['绿化率'].str.replace("%", "").apply(float)
    data['总价'] = data['总价'].str.replace("万", "").apply(float)

    return data
